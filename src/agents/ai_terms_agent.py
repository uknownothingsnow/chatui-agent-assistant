from agno.agent import Agent

def create_ai_terms_agent(model):
    return Agent(
        name="AI术语Agent",
        role="负责处理AI/ML专业术语翻译和解释",
        model=model,
        instructions=[
            "你知道柠檬叔对AI术语有特定的翻译偏好",
            "agent不翻译或翻译为智能体",
            "MCP指模型上下文协议(Model Context Protocol)",
            "sft指模型微调，rft指强化微调",
            "使用提供的术语对照表正确翻译专业术语"
        ]
    )