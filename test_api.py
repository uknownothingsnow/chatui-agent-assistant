#!/usr/bin/env python3
"""
API配置测试脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_api_key():
    """测试API Key配置"""
    print("🔑 API Key 配置测试")
    print("=" * 40)
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ DEEPSEEK_API_KEY 环境变量未设置")
        print("\n请设置API Key:")
        print("export DEEPSEEK_API_KEY=\"your_api_key_here\"")
        return False
    
    print(f"✅ API Key 已设置 (长度: {len(api_key)})")
    print(f"   前缀: {api_key[:10]}...")
    
    # 检查API Key格式
    if api_key.startswith("sk-"):
        print("✅ API Key 格式正确 (以 'sk-' 开头)")
    else:
        print("⚠️  API Key 格式可能不正确 (应该以 'sk-' 开头)")
    
    return True

def test_model_initialization():
    """测试模型初始化"""
    print("\n🤖 模型初始化测试")
    print("=" * 40)
    
    try:
        from src.volcengine_provider import VolcEngineModelProvider
        
        print("✅ VolcEngineModelProvider 导入成功")
        
        # 创建提供者实例
        provider = VolcEngineModelProvider()
        print(f"✅ 提供者创建成功")
        print(f"   模型ID: {provider.model_id}")
        print(f"   基础URL: {provider.base_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型提供者创建失败: {e}")
        return False

def test_deepseek_model():
    """测试DeepSeek模型"""
    print("\n🔧 DeepSeek模型测试")
    print("=" * 40)
    
    try:
        from agno.models.deepseek import DeepSeek
        
        print("✅ DeepSeek 模型类导入成功")
        
        # 检查环境变量
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print("❌ 无法测试模型初始化 - API Key 未设置")
            return False
        
        # 尝试创建模型实例（不进行实际API调用）
        model = DeepSeek(
            id="ep-20250204220334-l2q5g",
            base_url="https://ark.cn-beijing.volces.com/api/v3/"
        )
        
        print("✅ DeepSeek 模型实例创建成功")
        print(f"   模型ID: {model.id}")
        print(f"   基础URL: {model.base_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek 模型测试失败: {e}")
        return False

def test_simple_query():
    """测试简单查询（需要有效的API Key）"""
    print("\n💬 简单查询测试")
    print("=" * 40)
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 无法进行查询测试 - API Key 未设置")
        return False
    
    try:
        from agno.models.deepseek import DeepSeek
        
        model = DeepSeek(
            id="ep-20250204220334-l2q5g",
            base_url="https://ark.cn-beijing.volces.com/api/v3/"
        )
        
        print("🔄 发送测试查询...")
        response = model.complete("你好，请回复'测试成功'")
        
        print("✅ 查询成功!")
        print(f"   响应: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ 查询测试失败: {e}")
        
        # 分析错误类型
        error_str = str(e).lower()
        if "403" in error_str or "access denied" in error_str:
            print("\n🔍 错误分析:")
            print("   这可能是API Key权限问题:")
            print("   1. API Key 可能无效或已过期")
            print("   2. API Key 可能没有访问该模型的权限")
            print("   3. 可能需要检查火山引擎控制台的配额设置")
        elif "401" in error_str or "unauthorized" in error_str:
            print("\n🔍 错误分析:")
            print("   这可能是API Key认证问题:")
            print("   1. API Key 格式不正确")
            print("   2. API Key 可能被错误设置")
        
        return False

def main():
    """主测试函数"""
    print("🍋 柠檬叔个人助手 API 配置测试")
    print("=" * 50)
    
    tests = [
        ("API Key 配置", test_api_key),
        ("模型提供者", test_model_initialization),
        ("DeepSeek 模型", test_deepseek_model),
    ]
    
    # 先运行基础测试
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 如果基础测试都通过，尝试查询测试
    if all(result for _, result in results):
        print("\n" + "=" * 50)
        print("🚀 基础测试通过，尝试查询测试...")
        
        try:
            query_result = test_simple_query()
            results.append(("简单查询", query_result))
        except Exception as e:
            print(f"❌ 查询测试异常: {e}")
            results.append(("简单查询", False))
    
    # 输出结果
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
        print("🎉 所有测试通过！API配置正确。")
    else:
        print("⚠️  部分测试失败，请检查上述问题。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 