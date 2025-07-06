# 🍋 柠檬叔个人助手 - 快速开始

## ✅ 项目初始化完成

所有依赖已安装，项目结构已验证。

**已安装的依赖包括**：
- agno (AI Agent框架)
- fastapi (Web API框架)
- uvicorn (ASGI服务器)
- sqlalchemy (数据库ORM)
- openai, httpx (HTTP客户端)
- python-multipart, aiofiles (文件处理)

## 🚀 启动步骤

### 1. 设置API Key
```bash
export DEEPSEEK_API_KEY="your_api_key_here"
```

### 2. 启动服务器
```bash
./start_server.sh
```

### 3. 访问应用
- 前端: http://localhost:8000
- API文档: http://localhost:8000/docs

## 🧪 测试设置
```bash
python test_setup.py
```

## 📁 项目结构
- `src/` - 后端代码
- `frontend/` - 前端界面  
- `start_server.sh` - 启动脚本
- `test_setup.py` - 测试脚本

详细说明请查看 `README.md` 