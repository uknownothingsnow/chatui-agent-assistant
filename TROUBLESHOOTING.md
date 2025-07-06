# 🔧 故障排除指南

## 常见问题及解决方案

### 1. API Key 相关错误

#### 错误信息：
```
Error code: 403 - AccessDenied
The request failed because you do not have access to the requested resource
```

#### 解决方案：

**步骤1: 设置API Key**
```bash
# Linux/macOS
export DEEPSEEK_API_KEY="your_actual_api_key_here"

# Windows PowerShell
$env:DEEPSEEK_API_KEY = "your_actual_api_key_here"

# Windows CMD
set DEEPSEEK_API_KEY=your_actual_api_key_here
```

**步骤2: 获取正确的API Key**
1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 进入 "AI 服务" → "大模型服务"
3. 创建或查看你的API Key
4. 确保API Key有足够的配额和权限

**步骤3: 验证API Key格式**
- API Key应该以 `sk-` 开头
- 长度通常在40-50个字符
- 不包含空格或特殊字符

**步骤4: 永久设置环境变量**

Linux/macOS (添加到 `~/.bashrc` 或 `~/.zshrc`):
```bash
echo 'export DEEPSEEK_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

Windows (系统环境变量):
```powershell
[Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "your_api_key_here", "User")
```

### 2. 依赖安装问题

#### 错误信息：
```
ModuleNotFoundError: No module named 'xxx'
```

#### 解决方案：
```bash
# 重新安装依赖
source .venv/bin/activate
uv pip install -r requirements.txt

# 或者手动安装缺失的包
uv pip install agno fastapi uvicorn sqlalchemy
```

### 3. 端口占用问题

#### 错误信息：
```
Address already in use
```

#### 解决方案：
```bash
# 使用不同端口
uvicorn src.api_server:app --host 0.0.0.0 --port 8001 --reload

# 或者停止占用端口的进程
lsof -ti:8000 | xargs kill -9
```

### 4. 数据库连接问题

#### 错误信息：
```
sqlalchemy.exc.OperationalError
```

#### 解决方案：
```bash
# 检查数据库文件权限
ls -la src/lemonhall_memory.db

# 重新创建数据库文件（如果损坏）
rm src/lemonhall_memory.db
# 重启服务器，会自动创建新的数据库文件
```

## 🔍 诊断工具

### 1. 运行完整测试
```bash
python test_setup.py
```

### 2. 运行API测试
```bash
python test_api.py
```

### 3. 检查项目状态
```bash
python check_status.py
```

### 4. 检查环境变量
```bash
echo $DEEPSEEK_API_KEY
```

## 📞 获取帮助

如果以上解决方案都无法解决问题：

1. **检查日志**: 查看终端输出的详细错误信息
2. **验证配置**: 确保所有配置文件正确
3. **更新依赖**: 确保使用最新版本的依赖包
4. **联系支持**: 如果是火山引擎API问题，联系火山引擎技术支持

## 🚀 快速修复脚本

如果遇到常见问题，可以运行以下脚本：

```bash
# 重新初始化项目
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# 设置API Key（需要手动输入）
read -p "请输入你的DEEPSEEK_API_KEY: " api_key
export DEEPSEEK_API_KEY="$api_key"

# 测试配置
python test_api.py
``` 