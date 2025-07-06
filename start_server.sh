#!/bin/bash

# 柠檬叔个人助手启动脚本

echo "🍋 柠檬叔个人助手启动脚本"
echo "================================"

# 检查虚拟环境是否存在
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: uv venv"
    exit 1
fi

# 检查环境变量
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  警告: DEEPSEEK_API_KEY 环境变量未设置"
    echo "请设置你的火山引擎 DeepSeek API Key:"
    echo "export DEEPSEEK_API_KEY=\"your_api_key_here\""
    echo ""
    echo "或者临时设置（仅当前会话有效）:"
    read -p "请输入你的 DEEPSEEK_API_KEY: " api_key
    if [ -n "$api_key" ]; then
        export DEEPSEEK_API_KEY="$api_key"
        echo "✅ API Key 已临时设置"
    else
        echo "❌ 未提供 API Key，无法启动服务器"
        exit 1
    fi
else
    echo "✅ DEEPSEEK_API_KEY 已设置"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source .venv/bin/activate

# 检查依赖是否安装
echo "📦 检查依赖..."
python -c "import agno, fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 依赖未安装，正在安装..."
    uv pip install agno fastapi "uvicorn[standard]" openai httpx python-multipart aiofiles sqlalchemy
fi

echo "🚀 启动服务器..."
echo "📱 前端界面: http://localhost:8000"
echo "📚 API 文档: http://localhost:8000/docs"
echo "🔍 API 状态: http://localhost:8000/api-status"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================"

# 启动服务器
uvicorn src.api_server:app --host 0.0.0.0 --port 8000 --reload 