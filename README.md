# Search-2api 🚀 - 将实时网络搜索能力融入你的 AI 应用

<p align="center">
  <a href="https://github.com/lzA6/Search-2api/blob/main/LICENSE"><img src="https://img.shields.io/github/license/lzA6/Search-2api?color=blue" alt="License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/Framework-FastAPI-green.svg" alt="Framework"></a>
  <a href="https://www.nginx.com/"><img src="https://img.shields.io/badge/Proxy-Nginx-purple.svg" alt="Proxy"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Deployment-Docker-blueviolet.svg" alt="Deployment"></a>
</p>

**一份宣言 📜 | 一份蓝图 🗺️ | 一份深度报告 🔬 | 一份保姆级教程 🧑‍🏫 | 一份协议书 ⚖️ | 一份邀请函 ✨**

---

### **一份宣言：我们不创造信息，我们只是信息的“灵魂摆渡人”** 📜

在这个信息爆炸的时代，我们常常被困在过时数据的孤岛上。大语言模型（LLM）拥有渊博的知识，但它们的时间胶囊，永远停留在了训练数据截止的那一刻。

`Search-2api` 的诞生，源于一个纯粹而强大的哲学：**让 AI 睁开双眼，拥抱此刻的互联网。**

我们相信，真正的智能，是融合了历史智慧与实时信息的能力。本项目不是要创造另一个搜索引擎，而是要成为一座桥梁，一个“灵魂摆渡人”，将 <sup>1</sup> [<sup>1</sup>](https://search.sh/) 强大的实时搜索与总结能力，优雅地摆渡到任何遵循 OpenAI API 标准的浩瀚生态之中。

这不仅仅是一个开源项目，这是我们对“信息自由”与“技术普惠”的一次致敬。我们相信，通过动手实践（Learning by Doing），每个人都能成为驾驭信息洪流的船长。这份文档，就是你的第一张海图。它将毫无保留地为你揭示所有秘密，我们希望它能点燃你的好奇心，让你在探索中收获愉悦，并最终发出感叹：**“原来如此，我来我也行！”**

---

### **✨ 项目带来了什么？—— 核心价值与权衡**

#### **👍 好处与作用 (Benefits & Effects)**

1.  **实时性（Real-time）**: 赋予你的 AI 应用连接现实世界的能力，无论是查询今天的新闻、最新的产品价格，还是刚刚发布的技术文档，都能得到即时、准确的回答。
2.  **高兼容性（High Compatibility）**: 无缝接入任何支持 OpenAI API 的第三方客户端或应用生态（如 NextChat, LobeChat, Vercel AI SDK 等），无需修改任何客户端代码。
3.  **零成本（Zero Cost）**: 充分利用 `search.sh` 提供的免费服务，让你在个人项目或原型验证阶段，无需承担昂贵的搜索 API 调用费用。
4.  **高性能与稳定性（High Performance & Stability）**: 采用经过生产环境验证的 `Nginx + FastAPI` 黄金架构，确保了高并发处理能力和服务的稳定性。
5.  **隐私与自主可控（Privacy & Control）**: 所有服务均在你的本地或你自己的服务器上运行，数据流转完全透明，无需担心隐私泄露。

#### **👎 缺点与权衡 (Drawbacks & Trade-offs)**

1.  **依赖上游服务**: 本项目本质上是一个适配器，其稳定性和服务质量完全依赖于 `search.sh`。如果上游服务发生变更、中断或增加限制，本项目可能会受到影响。
2.  **认证信息的维护**: `Cookie` 是与 `search.sh` 保持会话的关键，它通常有有效期。过期后，需要用户手动重新获取并更新 `.env` 文件，这带来了一定的维护成本。
3.  **非官方支持**: 这是一个基于逆向工程的社区项目，无法获得 `search.sh` 官方的技术支持。

---

### **🗺️ 架构蓝图：它是如何工作的？**

为了让小白和 AI 都能轻松理解，我们把 `Search-2api` 想象成一家高效的“信息处理餐厅”。

```mermaid
graph TD
    A[👨‍💻 你的应用<br>(如 Cherry Studio)] -- "点一份'西红柿炒鸡蛋怎么做？'"<br>POST /v1/chat/completions --> B{🚪 Nginx 前台<br>(端口: 8080)};
    B -- "将菜单递给8000号房间" --> C[🏢 FastAPI 办公室<br>(端口: 8000)];
    C -- "收到菜单，交给专家处理" --> D[🕵️‍♂️ SearchProvider 专家];
    D -- "查阅菜谱(访问 search.sh)" --> E[🌐 search.sh API];
    E -- "实时反馈: '正在找锅...'"<br>"'正在打鸡蛋...'"<br>"'西...红...柿...'" --> D;
    D -- "将专家的反馈实时翻译成顾客能懂的话" --> C;
    C -- "服务员实时传话" --> B;
    B -- "前台实时广播给顾客" --> A;
```

**数据流转详解：**

1.  **顾客点餐 (Your App)**: 你的应用（客户端）向 `http://localhost:8080/v1/chat/completions` 发送一个标准的 OpenAI 请求。
2.  **前台接待 (Nginx)**: `Nginx` 作为餐厅的唯一入口，在 `8080` 端口接待了你。它看了一眼你的“会员卡”（Cookie），确保你每次来都由同一个“服务员”接待（**粘性会话**），然后将你的请求转交给内部的 `8000` 端口。
3.  **办公室处理 (FastAPI)**: `FastAPI` 应用接收到请求，它只做一件事：把请求原封不动地交给最专业的 `SearchProvider` 专家。
4.  **专家工作 (SearchProvider)**:
    *   它将你的问题（"西红柿炒鸡蛋怎么做？"）打包成 `search.sh` API 能听懂的格式。
    *   它向 `search.sh` 发起请求，并开始**实时监听**对方的“工作汇报”。
    *   当 `search.sh` 汇报“正在搜索...”时，`SearchProvider` 立刻将这个状态翻译成 OpenAI 格式的流式数据块。
    *   当 `search.sh` 开始逐字汇报“西...红...柿...”时，`SearchProvider` 也实时地将这些字翻译成流式数据块。
5.  **实时上菜 (StreamingResponse)**: 所有翻译好的数据块，通过 `StreamingResponse` 被实时地、一块一块地送回你的应用，最终在你的屏幕上呈现出流畅的打字效果和状态更新。

---

### **🧑‍🏫 保姆级教程：三分钟，让你的 AI 睁开双眼！**

#### **第一步：获取“飞船” - 克隆本项目**

打开你的命令行工具（CMD 或 PowerShell），进入你喜欢的工作目录，然后运行：

```bash
git clone https://github.com/lzA6/Search-2api.git
cd Search-2api
```

#### **第二步：伪造“通行证” - 获取 Cookie**

这是最关键的一步，我们需要从浏览器那里“借”来一张临时通行证。

1.  **打开开发者工具**: 在你的 Chrome/Edge 浏览器中，访问 <sup>1</sup> [<sup>1</sup>](https://search.sh/)，然后按 `F12` 打开开发者工具。
2.  **找到网络请求**: 点击 "Network" (网络) 标签页。在 `search.sh` 的搜索框里随便输入点什么（比如 "hello"）并回车。
3.  **定位关键请求**: 在网络请求列表中，找到一个名为 `search` 的请求。点击它。
4.  **复制 Cookie 值**: 在右侧弹出的窗口中，向下滚动到 **"Request Headers"** (请求标头) 部分。找到 `cookie:` 字段，右键点击它的完整值，选择 "Copy value"。

    !抓取 Cookie 教程图 [<sup>2</sup>](https://raw.githubusercontent.com/lzA6/Search-2api/main/assets/how-to-get-cookie.png)

#### **第三步：配置“引擎” - 设置 `.env` 文件**

1.  在项目根目录，将 `.env.example` 文件复制一份，并重命名为 `.env`。
2.  用文本编辑器打开 `.env` 文件。
3.  将你刚刚复制的**完整 Cookie 字符串**粘贴到 `SEARCH_SH_COOKIE="..."` 的引号中。
4.  **⚠️ 高能预警！** 检查你粘贴的 Cookie 值里是否有美元符号 `$`。如果有，必须将**每一个 `$` 都替换成两个 `$$`**。这是为了防止 Docker 把 `$` 当成变量而导致解析错误。
    *   **例如**: `...Cc$oyk...` 必须改为 `...Cc$$oyk...`
5.  （可选）如果你想为你的 API 设置密码，可以在 `API_MASTER_KEY="..."` 中填入你的密码。

#### **第四步：点火！- 启动服务**

确保你已经安装了 Docker Desktop <sup>2</sup> [<sup>3</sup>](https://www.docker.com/products/docker-desktop/)。然后在项目根目录的命令行中，运行：

```bash
docker-compose up -d --build
```

看到 `done` 的提示后，你的 `Search-2api` 飞船就已经在 `http://localhost:8080` 港口待命了！

#### **第五步：验证航线 - 使用 CMD 测试**

打开一个新的 CMD 窗口，复制并运行以下指令（假设你的密钥是 `1`）：

```cmd
curl http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer 1" -d "{\"model\": \"search-sh-ai\", \"messages\": [{\"role\": \"user\", \"content\": \"你好，请问西红柿炒鸡蛋怎么做？\"}], \"stream\": true}"
```

如果你看到一连串 `data:` 开头的数据在屏幕上滚动，那么恭喜你，舰长！我们成功了！

---

### **🛋️ 懒人福音：一键部署到 Hugging Face**

不想在本地折腾？没问题！你可以将此项目免费部署到 Hugging Face Spaces。

1.  **Fork 本仓库**: 在 GitHub 页面右上角，点击 "Fork"，将此项目复制到你自己的 GitHub 账户下。
2.  **创建 Space**: 前往 Hugging Face <sup>3</sup> [<sup>4</sup>](https://huggingface.co/new-space)，选择 "Docker" -> "Docker from Hub"。
3.  **配置 Space**:
    *   **Space name**: 给你项目起个酷炫的名字。
    *   **Docker template**: 选择 `Nginx server from a Dockerfile`。
    *   **Secrets**: 在 "Repository secrets" 中，点击 "New secret"，添加以下两个秘密：
        *   `SEARCH_SH_COOKIE`: 值为你获取并**转义 `$` 符号后**的完整 Cookie 字符串。
        *   `API_MASTER_KEY`: 值为你想要设置的 API 密钥。
4.  **创建！**: 点击 "Create Space"。Hugging Face 会自动为你构建并部署应用。稍等片刻，你将拥有一个公网可以访问的 `Search-2api` 服务！

---

### **🔬 深度报告：技术、算法与哲学**

#### **1. Nginx：餐厅的“金牌迎宾” (★★☆☆☆)**

*   **技术点**: 反向代理 (Reverse Proxy)、负载均衡 (Load Balancing)、粘性会话 (Sticky Sessions)。
*   **大白话解释**: Nginx 就像餐厅的迎宾。它站在 `8080` 这个大门口，所有客人都先经过它。
    *   `proxy_pass http://search_backend;`: 它把客人的点餐单（请求）递给后厨（我们的 FastAPI 应用）。
    *   `hash $http_cookie consistent;`: 这是它的“超强记忆力”。它会记住你的“会员卡”（Cookie），确保你每次来都由同一个服务员接待，避免了因换人导致的服务混乱（这对于需要保持登录状态的应用至关重要）。
    *   `proxy_buffering off;`: 这是它的“实时传话”能力。后厨每做好一道菜（一个数据块），它就立刻端给你，而不是等所有菜都做完再一起上。这就是实现“打字机效果”的关键。
*   **技术来源**: 这是 Web 服务部署的经典“黄金搭档”模式，任何关于 Nginx + uvicorn 的教程（如 DigitalOcean, Vultr 的博客）都会介绍。

#### **2. FastAPI & CORS：办公室的“高效秘书”与“开放政策” (★☆☆☆☆)**

*   **技术点**: 异步 I/O (Async IO), Pydantic, CORS 中间件。
*   **大白话解释**: FastAPI 是我们办公室里那位极其高效的秘书。
    *   **异步 (Async)**: 当它把任务交给 `SearchProvider` 专家后，它不会傻等，而是会去处理其他杂事（比如接待新请求）。这使得我们的“办公室”能同时处理很多客人的需求，效率极高。
    *   **CORS 中间件**: 这是我们办公室的“开放日政策”。它告诉所有来自不同地方（不同域）的访客（客户端软件）：“欢迎光临！你们可以带任何行李（请求头），也可以用任何方式（GET, POST）来访问我们。” 这彻底解决了第三方软件因“跨域”安全策略而被拒绝访问的问题。
*   **技术来源**: FastAPI 官方文档是学习这些概念的最佳起点，清晰易懂。

#### **3. SearchProvider：唯一的“全能专家” (★★★☆☆)**

*   **技术点**: 状态化流解析 (Stateful Stream Parsing), 责任分离 (Separation of Concerns), 适配器模式 (Adapter Pattern)。
*   **大白话解释**: 这是我们整个项目的“灵魂人物”。
    *   **适配器模式**: 它就像一个“万能翻译官”，把 OpenAI 的“普通话”翻译成 `search.sh` 的“方言”，再把 `search.sh` 的“方言”实时翻译回 OpenAI 的“普通话”。
    *   **状态化流解析**: 这是它最高级的技能。`search.sh` 在汇报工作时，会说：“我找到了：A... 我找到了：AB... 我找到了：ABC...”。如果我们直接转发，客户端就会看到 "A, AB, ABC"，内容大量重复。我们的专家拥有“记忆”，它会记住上次已经说过的 "AB"，当收到 "ABC" 时，它只告诉你新增的那个 "C"。这就是将“累积流”转换为“增量流”的核心算法，确保了流畅的打字机效果。
    *   **责任分离**: 在最终版本中，我们把所有“脏活累活”（判断流式、打包响应、处理错误）都交给了它，让 `main.py` 只负责“引路”。这让代码结构更清晰，更容易维护和扩展。
*   **技术来源**: 这种流处理模式在处理各类 SSE (Server-Sent Events) API 时非常常见，是高级后端开发的必备技能。

---

### **🔭 未来蓝图：我们的征途是星辰大海**

`Search-2api` 已经完成了从 0 到 1 的关键一步，但它的潜力远不止于此。

#### **✅ 现阶段已完成 (v9.0)**

*   [x] **核心代理功能**: 实现了 `search.sh` 到 OpenAI API 的完整转换。
*   [x] **流式与非流式支持**: 兼容两种请求模式。
*   [x] **黄金标准架构**: 采用 `Nginx + FastAPI` 稳定架构。
*   [x] **终极兼容性**: 通过 CORS 和公开模型列表，兼容绝大多数第三方客户端。
*   [x] **实时状态反馈**: 解决了初始等待焦虑，提供了优秀的用户体验。
*   [x] **完善的部署方案**: 提供 Docker 和 Hugging Face 一键部署。

#### **🚀 未来落地与完整实现计划**

1.  **【待实现】自动化 Cookie 续期 (★★★★☆)**
    *   **问题**: 当前 `Cookie` 需要手动更新。
    *   **技术路径**: 集成 `Playwright` 或 `Selenium` 等浏览器自动化库。在 Docker 容器中运行一个无头浏览器，定期模拟登录 `search.sh` 以获取最新的 `Cookie`，并自动更新到配置中。这将实现“一次配置，永久运行”的终极便利性。

2.  **【待实现】多账号轮询与负载均衡 (★★★☆☆)**
    *   **问题**: 当前只支持单个 `Cookie`，如果请求量大，容易被上游限制。
    *   **技术路径**:
        *   在 `.env` 和 `config.py` 中支持配置多个账号（`SEARCH_SH_COOKIE_1`, `SEARCH_SH_COOKIE_2`...）。
        *   在 `SearchProvider` 中实现一个轮询（Round-robin）或随机选择策略，将请求分发到不同的账号上，分摊压力。

3.  **【待实现】更精细的状态解析与工具调用 (★★★★☆)**
    *   **问题**: 当前我们将“Searching...”、“Summarizing...”等状态作为普通内容输出，虽然有效，但不够优雅。
    *   **技术路径**: 探索使用 OpenAI 的 `tool_calls` 功能。将这些状态信息包装成一个名为 `search_status` 的工具调用，而不是直接输出。这需要客户端的支持，但代表了更先进、更结构化的交互方式。

4.  **【待实现】支持图片搜索结果 (★★★★★)**
    *   **问题**: `search.sh` 可能会返回图片搜索结果，我们目前忽略了它们。
    *   **技术路径**: 解析 API 响应中可能包含的图片链接，并将其以 Markdown 格式 (`!alt <sup>1</sup> [<sup>5</sup>](url)`) 插入到最终的回答中，实现真正的图文并茂。

#### **🤝 邀请你成为“共建者”**

这个项目属于每一个热爱探索、乐于分享的你。如果你对以上任何一个方向感兴趣，或者有更酷的想法，我们热烈欢迎你通过 **Pull Request** 或 **Issue** 的方式，为这艘“飞船”添砖加瓦。

---

### **🏗️ 项目文件结构**

为了方便你或 AI 快速理解项目全貌，这是我们的“飞船设计图”：

```
Search-2api/
│
├── .env                # 你的私人配置文件，存放密钥（不提交到Git）
├── .env.example        # 配置文件的模板
├── .gitignore          # 告诉Git哪些文件不需要追踪
├── docker-compose.yml  # Docker“总指挥”，一键启动所有服务
├── Dockerfile          # FastAPI应用的“建造说明书”
├── main.py             # 项目的“主入口”，负责路由和认证
├── nginx.conf          # Nginx的“行为准则”，负责网络代理和性能优化
├── README.md           # 你正在阅读的这份“史诗级文档”
├── requirements.txt    # Python依赖库清单
│
└─ app/                 # 核心应用代码目录
   ├── __init__.py
   │
   ├── core/            # 核心配置模块
   │   ├── __init__.py
   │   └── config.py    # Pydantic配置模型
   │
   └── providers/       # 真正的“专家”工作区
       ├── __init__.py
       └── search_provider.py # 负责与search.sh交互的所有逻辑
```

---

### **⚖️ 开源协议：Apache License 2.0**

本项目遵循 Apache License 2.0 开源协议。

您可以自由地：

*   **共享** — 在任何媒介以任何形式复制、发行本作品
*   **演绎** — 修改、转换或以本作品为基础进行创作
*   在任何用途下，甚至商业目的。

只要你遵守以下条款：

*   **署名** — 您必须给出适当的署名，提供指向本许可协议的链接，同时标明是否（对原始作品）作了修改。您可以用任何合理的方式来署名，但不得以任何方式暗示许可人为您或您的使用背书。
*   **没有附加限制** — 您不得适用法律术语或者技术措施从而限制其他人做许可协议允许的事情。

完整的协议文本请参考 Apache License 2.0 <sup>1</sup> [<sup>6</sup>](https://www.apache.org/licenses/LICENSE-2.0)。

---

**再次感谢你的探索精神，舰长！现在，去创造吧！**
