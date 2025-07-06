#!/bin/bash

# 柠檬叔个人助手 API Key 设置脚本

echo "🍋 柠檬叔个人助手 API Key 设置"
echo "================================"

# 检查是否已经有API Key
if [ -n "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  检测到已设置的 DEEPSEEK_API_KEY"
    echo "   当前值: ${DEEPSEEK_API_KEY:0:10}..."
    read -p "是否要重新设置? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ 保持现有API Key"
        exit 0
    fi
fi

echo ""
echo "📝 请输入你的火山引擎 DeepSeek API Key"
echo "   获取地址: https://console.volcengine.com/"
echo "   格式: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
echo ""

# 读取API Key
read -p "API Key: " api_key

# 验证API Key格式
if [[ -z "$api_key" ]]; then
    echo "❌ API Key 不能为空"
    exit 1
fi

if [[ ! "$api_key" =~ ^sk-[a-zA-Z0-9]{32,}$ ]]; then
    echo "⚠️  API Key 格式可能不正确"
    echo "   应该以 'sk-' 开头，后跟32位以上的字母数字"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 设置环境变量
export DEEPSEEK_API_KEY="$api_key"
echo "✅ API Key 已临时设置"

# 询问是否永久保存
read -p "是否永久保存到 ~/.bashrc? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 检查是否已经存在
    if grep -q "DEEPSEEK_API_KEY" ~/.bashrc; then
        echo "⚠️  检测到 ~/.bashrc 中已有 DEEPSEEK_API_KEY 设置"
        read -p "是否覆盖? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # 删除旧的设置
            sed -i '/DEEPSEEK_API_KEY/d' ~/.bashrc
        else
            echo "✅ 保持现有设置"
            exit 0
        fi
    fi
    
    # 添加新的设置
    echo "export DEEPSEEK_API_KEY=\"$api_key\"" >> ~/.bashrc
    echo "✅ API Key 已永久保存到 ~/.bashrc"
    echo "   请运行 'source ~/.bashrc' 或重新打开终端使设置生效"
fi

echo ""
echo "🧪 测试API Key..."
if python test_api.py; then
    echo ""
    echo "🎉 API Key 设置成功！"
    echo "🚀 现在可以启动服务器: ./start_server.sh"
else
    echo ""
    echo "⚠️  API Key 测试失败，请检查:"
    echo "   1. API Key 是否正确"
    echo "   2. 是否有足够的配额"
    echo "   3. 网络连接是否正常"
fi 