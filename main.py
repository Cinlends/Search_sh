from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
import traceback

# 导入 CORS 中间件，这是兼容所有客户端的基础
from fastapi.middleware.cors import CORSMiddleware

# 从 app 包导入模块
from app.providers.search_provider import SearchProvider
from app.core.config import settings

# 初始化 FastAPI 应用
app = FastAPI(
    title="Search-2api",
    version="7.0.0-final-compatibility",
    description="一个采用黄金标准架构，并为最大化客户端兼容性而优化的 API 代理。"
)

# --- 配置 CORS 中间件 ---
# 解决所有第三方客户端的跨域请求问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],      # 允许所有方法 (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],      # 允许所有请求头 (包括 Authorization)
)

# 实例化全能的 Provider
search_provider = SearchProvider()

# --- 认证依赖项 (只用于需要保护的接口) ---
async def verify_api_key(authorization: Optional[str] = Header(None)):
    """
    检查 API 密钥的依赖项。
    如果 .env 文件中设置了 API_MASTER_KEY，则请求头必须包含正确的密钥。
    """
    if settings.API_MASTER_KEY:
        if authorization is None:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized: Missing Authorization header.",
            )
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer" or token != settings.API_MASTER_KEY:
                raise ValueError("Invalid scheme or token")
        except ValueError:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: Invalid API Key or authentication scheme.",
            )

# --- 核心聊天接口 (严格认证) ---
@app.post("/v1/chat/completions", dependencies=[Depends(verify_api_key)])
async def chat_completions(request: Request):
    """
    处理聊天请求的核心接口。
    此接口受 verify_api_key 保护，必须提供正确的密钥才能访问。
    """
    try:
        request_data = await request.json()
        # 全权委托给 Provider，由 Provider 返回最终的 Response 对象
        return await search_provider.handle_chat_completion(request_data)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"主路由发生内部服务器错误: {str(e)}")

# --- 模型列表接口 (终极修正：公开访问) ---
@app.get("/v1/models")
async def list_models():
    """
    模型列表接口，全权委托给 Provider 处理。
    关键修正：此接口不进行认证 (移除了 dependencies)，以响应客户端的 OPTIONS 预检请求，
    并允许所有客户端自由获取模型列表，实现最大化兼容。
    """
    try:
        return await search_provider.handle_list_models()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取模型列表时发生内部服务器错误: {str(e)}")

# --- 根路由 (用于健康检查) ---
@app.get("/")
def root():
    """根路由，提供服务基本信息，无需认证。"""
    return {"message": f"Welcome to {app.title}", "version": app.version}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
