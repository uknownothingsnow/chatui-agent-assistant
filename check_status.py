#!/usr/bin/env python3
"""
柠檬叔个人助手状态检查脚本
"""

import os
import sys
from pathlib import Path

def main():
    print("🍋 柠檬叔个人助手状态检查")
    print("=" * 40)
    
    # 检查虚拟环境
    if Path(".venv").exists():
        print("✅ 虚拟环境存在")
    else:
        print("❌ 虚拟环境不存在")
        return
    
    # 检查环境变量
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key:
        print("✅ DEEPSEEK_API_KEY 已设置")
    else:
        print("⚠️  DEEPSEEK_API_KEY 未设置")
    
    # 检查关键文件
    files = [
        "src/teams_consoles.py",
        "src/api_server.py", 
        "frontend/index.html",
        "start_server.sh",
        "requirements.txt"
    ]
    
    print("\n📁 文件检查:")
    for file in files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
    
    print("\n🚀 启动命令:")
    print("  ./start_server.sh")
    print("\n🌐 访问地址:")
    print("  http://localhost:8000")

if __name__ == "__main__":
    main() 