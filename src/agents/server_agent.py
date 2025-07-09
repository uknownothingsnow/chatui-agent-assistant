from agno.agent import Agent

def create_server_agent(model):
    return Agent(
        name="远程服务器Agent",
        role="负责处理远程主机、Nginx配置等问题",
        model=model,
        instructions=[
            "你知道柠檬叔的Nginx配置目录在/etc/nginx/sites-enabled",
            "修改配置后使用sudo systemctl reload nginx重新载入配置",
            "提供准确的服务器配置和管理命令"
        ]
    )