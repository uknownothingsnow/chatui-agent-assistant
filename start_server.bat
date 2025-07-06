@echo off
chcp 65001 >nul

REM 柠檬叔个人助手启动脚本 (Windows)

echo 🍋 柠檬叔个人助手启动脚本
echo ================================

REM 检查虚拟环境是否存在
if not exist ".venv" (
    echo ❌ 虚拟环境不存在，请先运行: uv venv
    pause
    exit /b 1
)

REM 检查环境变量
if "%DEEPSEEK_API_KEY%"=="" (
    echo ⚠️  警告: DEEPSEEK_API_KEY 环境变量未设置
    echo 请设置你的火山引擎 DeepSeek API Key:
    echo set DEEPSEEK_API_KEY=your_api_key_here
    echo.
    echo 或者临时设置（仅当前会话有效）:
    set /p api_key="请输入你的 DEEPSEEK_API_KEY: "
    if not "%api_key%"=="" (
        set DEEPSEEK_API_KEY=%api_key%
        echo ✅ API Key 已临时设置
    ) else (
        echo ❌ 未提供 API Key，无法启动服务器
        pause
        exit /b 1
    )
) else (
    echo ✅ DEEPSEEK_API_KEY 已设置
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 检查依赖是否安装
echo 📦 检查依赖...
python -c "import agno, fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo ❌ 依赖未安装，正在安装...
    uv pip install agno fastapi "uvicorn[standard]" openai httpx python-multipart aiofiles sqlalchemy
)

echo 🚀 启动服务器...
echo 📱 前端界面: http://localhost:8000
echo 📚 API 文档: http://localhost:8000/docs
echo 🔍 API 状态: http://localhost:8000/api-status
echo.
echo 按 Ctrl+C 停止服务器
echo ================================

REM 启动服务器
uvicorn src.api_server:app --host 0.0.0.0 --port 8000 --reload 