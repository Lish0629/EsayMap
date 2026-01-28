
---
# EsayMap Geo-Analytic Agent System 🌍🤖  

> **基于大模型 (LLM) 与 GeoScene 的新一代地理空间分析平台**
> *Integrating Geospatial Analysis with Generative AI using FastAPI, Vue.js, and GeoScene Server.*

## 📖 项目简介 (Introduction)

本项目是一个集成了地理空间数据处理与大模型能力的 Web 应用。系统利用 **FastAPI** 和 **Vue.js** 构建高性能的前后端分离架构，并通过 **GeoScene** 进行地理分析。

核心创新在于深度集成了 **GeoScene 平台** 与 **阿里云百炼大模型**。通过 **RAG (检索增强生成)** 和 **MCP (模型上下文协议)** 技术，系统实现了“自然语言驱动”的地理要素构建与复杂空间几何分析，解决了传统 GIS 软件操作门槛高的问题 。

---

## 🏗️ 系统架构 (System Architecture)

系统采用典型的三层架构，并扩展了 AI Agent 层：

```mermaid
graph TD
    User[用户 (Browser)] -->|HTTP/80| Nginx[Nginx 反向代理]
    
    subgraph "Web Server"
        Nginx -->|/ (Static)| Vue[Vue 前端 (Dist)]
        Nginx -->|/api| API[FastAPI 后端 (:8000)]
        Nginx -->|/data| FS[本地文件系统 (GeoJSON)]
    end
    
    subgraph "AI Core (Aliyun Bailian)"
        API <-->|Request| Agent1[创建要素智能体 (MCP)]
        API <-->|Request| Agent2[地理分析智能体 (RAG)]
        Agent1 <--> Tool1[DataV Atlas (Geocoding/Routing)]
        Agent2 <--> KB[GeoScene 知识库]
    end
    
    subgraph "GIS Engine"
        Agent2 -.->|生成参数| API
        API -->|执行分析| GS[GeoScene Geometry Service]
    end

```

### 技术栈 (Tech Stack)

| 领域 | 技术/工具 | 说明 |
| --- | --- | --- |
| **Frontend** | Vue.js, Node.js 16+ | 现代响应式 UI，负责地图渲染与交互  |
| **Backend** | Python 3.8+, FastAPI | 高性能异步 API，处理业务逻辑与文件流  |
| **GIS** | GeoScene Server | 提供专业的 Geometry Service (Buffer, Union 等)  |
| **AI LLM** | 通义千问-Plus (Qwen) | 语义理解与逻辑推理核心  |
| **AI Pattern** | RAG & MCP | 知识库检索增强与标准化工具调用 |
---

## 🧠 AI 与 GeoScene 集成方案 (AI Integration)

本系统不直接“微调”模型，而是采用 **Agentic Workflow** 模式。

### 1. 地理分析智能体 (Analytics Agent) - 基于 RAG

通过 RAG 技术，让通用大模型学会使用 GeoScene 的专业工具。

* **机制**: 挂载 "GeoScene Server" 知识库，包含 `Buffer`, `Union`, `Simplify` 等 API 文档 。
* **流程**: 用户提问  Agent 检索文档 (e.g., `05_Buffer`)  生成符合 GeoScene 规范的 JSON 参数  后端调用 GeoScene 服务。
* **知识库内容**: 包含 `02_Geometry_Service`, `21_Simplify`, `15_Label_Points` 等核心几何操作说明 。



### 2. 创建要素智能体 (Creation Agent) - 基于 MCP

* **机制**: 使用 MCP 协议连接 DataV Atlas 地理服务 。
* **能力**: 负责从自然语言中提取地理信息并生成数据。
* **GeoCoding**: 地址转坐标（"杭州西站在哪"） 。
* **Routing**: 路径规划（"生成从西站到东站的行车路径"） 。

---

## 🚀 部署指南 (Deployment)

### 前置要求

* OS: Ubuntu 22.04 或 Windows 

* Env: Python 3.8+, Node.js 16+, Nginx 

* GIS: 能够访问 GeoScene Portal/Server 


### 第一步：后端部署 (FastAPI)

1. 进入后端目录并创建虚拟环境：
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 安装依赖并创建数据目录：
```bash
pip install -r requirements.txt
mkdir -p data  # 用于存放上传的 GeoJSON
```

3. 启动服务（开发模式）：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


### 第二步：前端部署 (Vue)

1. 安装依赖并构建：
```bash
cd frontend
npm install
npm run build
```


2. 部署到 Web 目录：
```bash
sudo cp -r dist/* /var/www/html/
```


### 第三步：Nginx 配置

编辑配置文件 `/etc/nginx/sites-available/default`，添加反向代理规则以解决跨域并整合服务 ：

```nginx
server {
    listen 80;
    
    # 1. 前端静态页面
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }
    
    # 2. 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
    }
    
    # 3. GeoJSON 数据文件直链
    location /data {
        alias /path/to/backend/data;  # ⚠️ 修改为实际后端路径
    }
}
```



重启 Nginx 生效：

```bash
sudo nginx -t && sudo systemctl reload nginx
```



### 第四步：GeoScene 设置

* 在 Portal 中找到 **Geometry Service**。
* 将服务共享权限设置为 **Everyone (所有人)**，确保后端 API 可以无障碍调用几何计算能力 。

---

## ✅ 验证 (Verification)

部署完成后，请依次检查以下接口状态：

| 检查项 | URL | 预期结果 |
| --- | --- | --- |
| **Web 首页** | `http://<IP>` | 前端页面正常加载，地图组件初始化  |
| **API 状态** | `http://<IP>:8000` | 返回 JSON `{"message": "running"}` |
| **文件上传** | `http://<IP>/api/upload-geojson` | 接口响应正常，支持前端上传文件 |

---

## 🛠️ 维护 (Maintenance)

* **数据清理**: 定期检查 `/backend/data` 目录，清理过期的临时 GeoJSON 文件。
* **日志监控**:
* Nginx: `/var/log/nginx/error.log`
* FastAPI: 控制台输出或配置 loguru 记录文件。



---

## 📄 License

此项目仅供学习与演示使用。具体代码协议请参阅 LICENSE 文件。
