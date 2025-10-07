import httpx
import json
import time
import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator, Dict, Any

from fastapi import HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from app.core.config import settings

class SearchProvider:
    """
    Search.sh 全能 Provider (v8.0 - 实时状态版)
    - 新增功能：捕获并转发 search.sh 的实时工作状态，显著改善用户体验。
    - 优化逻辑：在生成器中区分状态信息和内容信息。
    """
    BASE_URL = "https://search.sh/api/search"
    MODEL_NAME = "search-sh-ai"

    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/json",
            "Referer": "https://search.sh/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Cookie": settings.SEARCH_SH_COOKIE,
        }

    # --- 核心处理入口 (保持不变) ---
    async def handle_chat_completion(self, request_data: Dict[str, Any]) -> (StreamingResponse | JSONResponse):
        is_stream = request_data.get("stream", False)
        if is_stream:
            return StreamingResponse(self._stream_generator(request_data), media_type="text/event-stream")
        else:
            return await self._non_stream_generator(request_data)

    async def handle_list_models(self) -> JSONResponse:
        model_data = {
            "object": "list",
            "data": [
                {
                    "id": self.MODEL_NAME,
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "search.sh",
                }
            ],
        }
        return JSONResponse(content=model_data)

    # --- 流式与非流式生成器 (逻辑优化) ---
    async def _stream_generator(self, payload: dict) -> AsyncGenerator[str, None]:
        chat_id = f"chatcmpl-{uuid.uuid4().hex}"
        is_first_content_chunk = True
        
        try:
            # _get_response_stream 现在会产生两种类型的块：'status' 和 'content'
            async for data_piece in self._get_response_stream(payload):
                
                # 如果是状态更新
                if data_piece['type'] == 'status':
                    # 我们将状态信息也作为内容块发送，但格式化得更像一个提示
                    status_content = f"**`{data_piece['content']}`**\n\n"
                    # 对于状态信息，我们不需要发送 role 块
                    content_chunk = self._create_openai_chunk(chat_id, status_content)
                    yield f"data: {json.dumps(content_chunk)}\n\n"

                # 如果是真正的回答内容
                elif data_piece['type'] == 'content':
                    # 仅在第一个内容块前发送角色信息
                    if is_first_content_chunk:
                        role_chunk = self._create_openai_chunk(chat_id, None, role="assistant")
                        yield f"data: {json.dumps(role_chunk)}\n\n"
                        is_first_content_chunk = False
                    
                    content_chunk = self._create_openai_chunk(chat_id, data_piece['content'])
                    yield f"data: {json.dumps(content_chunk)}\n\n"

        except Exception as e:
            print(f"Error in stream generator: {e}")
            error_chunk = self._create_error_chunk(chat_id, str(e))
            yield f"data: {json.dumps(error_chunk)}\n\n"
        
        finally:
            final_chunk = self._create_openai_chunk(chat_id, None, finish_reason="stop")
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data:\n\n"

    async def _non_stream_generator(self, payload: dict) -> JSONResponse:
        full_response = ""
        try:
            # 非流式请求我们只关心最终内容，所以忽略 status 块
            async for data_piece in self._get_response_stream(payload):
                if data_piece['type'] == 'content':
                    full_response += data_piece['content']
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing non-streamed request: {e}")

        # (非流式响应的其余部分保持不变)
        completion_id = f"chatcmpl-{uuid.uuid4().hex}"
        response_data = {
            "id": completion_id, "object": "chat.completion", "created": int(time.time()), "model": self.MODEL_NAME,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": full_response}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": len(full_response), "total_tokens": len(full_response)}
        }
        return JSONResponse(content=response_data)

    # --- 底层 API 请求 (核心升级) ---
    async def _get_response_stream(self, payload: dict) -> AsyncGenerator[Dict[str, Any], None]:
        """
        底层的 API 请求和解析逻辑。
        核心升级：现在会 yield 一个字典，明确区分 'status' 和 'content' 类型的更新。
        """
        query = self._extract_query(payload)
        request_body = {
            "query": query,
            "currentDate": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream("POST", self.BASE_URL, headers=self.headers, json=request_body) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        data_json = json.loads(line)
                        # **新增：捕获并 yield 状态更新**
                        if "progressText" in data_json:
                            yield {"type": "status", "content": data_json["progressText"]}
                        
                        # **保持：捕获并 yield 内容更新**
                        if "summary" in data_json:
                            token = data_json["summary"]
                            if token:
                                yield {"type": "content", "content": token}
                    except (json.JSONDecodeError, KeyError):
                        continue

    # --- 辅助函数 (保持不变) ---
    def _extract_query(self, payload: dict) -> str:
        messages = payload.get("messages", [])
        if not messages: raise HTTPException(status_code=400, detail="No messages found in payload")
        last_user_message = next((msg["content"] for msg in reversed(messages) if msg.get("role") == "user"), None)
        if not last_user_message: raise HTTPException(status_code=400, detail="No user message found in payload")
        return last_user_message

    def _create_openai_chunk(self, chat_id: str, content: str = None, role: str = None, finish_reason: str = None) -> dict:
        delta = {}
        if role: delta['role'] = role
        if content: delta['content'] = content
        return {
            "id": chat_id, "object": "chat.completion.chunk", "created": int(time.time()), "model": self.MODEL_NAME,
            "choices": [{"index": 0, "delta": delta, "finish_reason": finish_reason}]
        }
    
    def _create_error_chunk(self, chat_id: str, message: str) -> dict:
        return {
            "id": chat_id, "object": "chat.completion.chunk", "created": int(time.time()), "model": self.MODEL_NAME,
            "choices": [{"index": 0, "delta": {"content": f"An error occurred: {message}"}, "finish_reason": "error"}]
        }
