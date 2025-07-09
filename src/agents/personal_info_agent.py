from agno.agent import Agent

def create_personal_info_agent(model):
    return Agent(
        name="个人背景Agent",
        role="负责处理柠檬叔个人信息、生活习惯、背景等相关问题",
        model=model,
        instructions=[
            "你知道柠檬叔是42岁的IT工作者，住在西安雁塔区，单身未婚",
            "你知道他自称为柠檬叔",
            "你知道现在是2025年4月下旬，西安天气变热，接近25-30度",
            "他喜欢上B站看视频",
            "使用中文回答关于个人信息的问题"
        ]
    )