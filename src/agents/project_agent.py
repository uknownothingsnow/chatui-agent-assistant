from agno.agent import Agent

def create_project_agent(model):
    return Agent(
        name="项目管理Agent",
        role="负责项目创建、管理和配置相关的问题",
        model=model,
        instructions=[
            "你知道柠檬叔把个人代码项目放在E:\\development目录下",
            "使用mkdir创建项目目录，uv init初始化项目，uv venv构建Python虚拟环境",
            "可以使用uv python list列出已安装的Python版本",
            "他习惯使用agno作为agent写作框架",
            "当被要求创建新项目时，直接提供完整的命令序列，包括目录创建、环境初始化等",
            "项目名称如无特别指定，应根据项目性质自动生成一个合适的名称"
        ]
    )