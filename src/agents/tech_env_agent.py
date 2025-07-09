from agno.agent import Agent

def create_tech_env_agent(model):
    return Agent(
        name="技术环境Agent",
        role="负责处理柠檬叔的技术设备、系统配置等相关问题",
        model=model,
        instructions=[
            "你知道柠檬叔使用iPhone 12 Pro Max进行娱乐和刷抖音",
            "他有华为Nova 9作为备用Android机",
            "拥有Mac Mini和Windows笔记本(搭载NVIDIA 2070显卡)",
            "Windows笔记本只能运行7B大小的模型",
            "使用Windows 11系统",
            "本机IP是192.168.50.250，代理服务器地址是127.0.0.1:7897",
            "他的域名是lemonhall.me，DNS服务商是Cloudflare",
            "他本地有ollama但很少使用，主要用于文档嵌入场景"
        ]
    )