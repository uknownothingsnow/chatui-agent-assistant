#!/usr/bin/env python3
"""
柠檬叔个人助手项目设置测试脚本
"""

import sys
import os
from pathlib import Path

def test_imports():
    """测试所有必要的依赖是否能正确导入"""
    print("🔍 测试依赖导入...")
    
    try:
        import agno
        print("✅ agno 导入成功")
    except ImportError as e:
        print(f"❌ agno 导入失败: {e}")
        return False
    
    try:
        import fastapi
        print("✅ fastapi 导入成功")
    except ImportError as e:
        print(f"❌ fastapi 导入失败: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ uvicorn 导入成功")
    except ImportError as e:
        print(f"❌ uvicorn 导入失败: {e}")
        return False
    
    try:
        import openai
        print("✅ openai 导入成功")
    except ImportError as e:
        print(f"❌ openai 导入失败: {e}")
        return False
    
    try:
        import httpx
        print("✅ httpx 导入成功")
    except ImportError as e:
        print(f"❌ httpx 导入失败: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ sqlalchemy 导入成功")
    except ImportError as e:
        print(f"❌ sqlalchemy 导入失败: {e}")
        return False
    
    return True

def test_project_files():
    """测试项目文件是否存在"""
    print("\n📁 测试项目文件...")
    
    required_files = [
        "src/__init__.py",
        "src/teams_consoles.py",
        "src/api_server.py",
        "src/volcengine_provider.py",
        "frontend/index.html",
        "frontend/assets/avatars/user.svg",
        "frontend/assets/avatars/assistant.svg",
        "pyproject.toml",
        "requirements.txt"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
            all_exist = False
    
    return all_exist

def test_environment():
    """测试环境变量设置"""
    print("\n🔑 测试环境变量...")
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key:
        print("✅ DEEPSEEK_API_KEY 已设置")
        return True
    else:
        print("⚠️  DEEPSEEK_API_KEY 未设置")
        print("   请设置环境变量: export DEEPSEEK_API_KEY=\"your_api_key\"")
        return False

def test_model_provider():
    """测试模型提供者是否能正常初始化"""
    print("\n🤖 测试模型提供者...")
    
    try:
        # 添加项目根目录到路径
        project_root = Path(__file__).resolve().parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        from src.volcengine_provider import VolcEngineModelProvider
        
        # 创建提供者实例（不实际初始化模型，避免API调用）
        provider = VolcEngineModelProvider()
        print("✅ VolcEngineModelProvider 创建成功")
        
        # 检查属性
        if hasattr(provider, 'V3') and hasattr(provider, 'R1'):
            print("✅ 模型ID常量定义正确")
        else:
            print("❌ 模型ID常量缺失")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 模型提供者测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🍋 柠檬叔个人助手项目设置测试")
    print("=" * 50)
    
    tests = [
        ("依赖导入", test_imports),
        ("项目文件", test_project_files),
        ("环境变量", test_environment),
        ("模型提供者", test_model_provider)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！项目设置完成。")
        print("\n🚀 启动服务器:")
        print("  Linux/macOS: ./start_server.sh")
        print("  Windows: start_server.bat")
        print("  手动启动: uvicorn src.api_server:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("⚠️  部分测试失败，请检查上述问题并重新设置。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 