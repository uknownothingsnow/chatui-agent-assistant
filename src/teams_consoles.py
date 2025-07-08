import sys
import os
from pathlib import Path
from agno.agent import Agent, AgentKnowledge
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.knowledge.url import UrlKnowledge
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.storage.sqlite import SqliteStorage
from agno.vectordb.mongodb import MongoDb
from agno.vectordb.search import SearchType
from agno.embedder.huggingface import HuggingfaceCustomEmbedder
from huggingface_hub import whoami
from agno.embedder.ollama import OllamaEmbedder
from pymongo import MongoClient
from agno.vectordb.mongodb import MongoDb
from sentence_transformers import SentenceTransformer


# --- Dynamically add project root to sys.path ---
# This allows running the script directly (python src/...) 
# while still using absolute imports like 'from src.module import ...'
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
# --- End of dynamic path addition ---

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
# Import the provider from the new file using absolute import
from src.volcengine_provider import VolcEngineModelProvider

model_provider = VolcEngineModelProvider(model_id=VolcEngineModelProvider.V3)
ds_model = model_provider.get_model() # Get the actual model instance

# 设置路径
cwd = Path(__file__).parent
memory_db_path = cwd.joinpath("lemonhall_memory.db")

# 创建持久化记忆
memory_db = SqliteMemoryDb(table_name="lemonhall_memory", db_file=str(memory_db_path))
memory = Memory(db=memory_db)

# 创建各个专业Agent
personal_info_agent = Agent(
    name="个人背景Agent",
    role="负责处理柠檬叔个人信息、生活习惯、背景等相关问题",
    model=ds_model,
    instructions=[
        "你知道柠檬叔是42岁的IT工作者，住在西安雁塔区，单身未婚",
        "你知道他自称为柠檬叔",
        "你知道现在是2025年4月下旬，西安天气变热，接近25-30度",
        "他喜欢上B站看视频",
        "使用中文回答关于个人信息的问题"
    ]
)

tech_env_agent = Agent(
    name="技术环境Agent",
    role="负责处理柠檬叔的技术设备、系统配置等相关问题",
    model=ds_model,
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

dev_tools_agent = Agent(
    name="开发工具Agent",
    role="负责处理编程工具、IDE和命令行相关的问题",
    model=ds_model,
    instructions=[
        "你知道柠檬叔主要使用VS Code和Cursor作为IDE",
        "他使用PowerShell，需要用分号分隔命令(如 cd .. ; ls)",
        "他使用uv系统进行Python包管理",
        "默认Python版本是3.12",
        "提供准确的PowerShell命令和开发工具使用建议"
    ]
)

project_agent = Agent(
    name="项目管理Agent",
    role="负责项目创建、管理和配置相关的问题",
    model=ds_model,
    instructions=[
        "你知道柠檬叔把个人代码项目放在E:\\development目录下",
        "使用mkdir创建项目目录，uv init初始化项目，uv venv构建Python虚拟环境",
        "可以使用uv python list列出已安装的Python版本",
        "他习惯使用agno作为agent写作框架",
        "当被要求创建新项目时，直接提供完整的命令序列，包括目录创建、环境初始化等",
        "项目名称如无特别指定，应根据项目性质自动生成一个合适的名称"
    ]
)

server_agent = Agent(
    name="远程服务器Agent",
    role="负责处理远程主机、Nginx配置等问题",
    model=ds_model,
    instructions=[
        "你知道柠檬叔的Nginx配置目录在/etc/nginx/sites-enabled",
        "修改配置后使用sudo systemctl reload nginx重新载入配置",
        "提供准确的服务器配置和管理命令"
    ]
)

ai_terms_agent = Agent(
    name="AI术语Agent",
    role="负责处理AI/ML专业术语翻译和解释",
    model=ds_model,
    instructions=[
        "你知道柠檬叔对AI术语有特定的翻译偏好",
        "agent不翻译或翻译为智能体",
        "MCP指模型上下文协议(Model Context Protocol)",
        "sft指模型微调，rft指强化微调",
        "使用提供的术语对照表正确翻译专业术语"
    ]
)

reasoning_agent = Agent(
    model=ds_model,
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True),
    ],
    instructions="Use tables to display data.",
    markdown=True,
)

# Load Agno documentation in a knowledge base
# You can also use `https://docs.agno.com/llms-full.txt` for the full documentation


knowledge = UrlKnowledge(
    urls=["https://docs.agno.com/introduction/agents.md"], # "https://docs.agno.com/llms-full.txt"],
    vector_db=MongoDb(
        db_url="mongodb://localhost:27017/?directConnection=true&serverSelectionTimeoutMS=2000",
        collection_name="agno_docs",
        search_type=SearchType.hybrid,
        search_index_name="agno_docs",
        embedder=OllamaEmbedder(),
    ),
)

knowledge.load(recreate=True)

# knowledge_base = PDFUrlKnowledgeBase(
#     urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
#     vector_db=MongoDb(
#         collection_name="recipes",
#         db_url="mongodb://localhost:27017/?directConnection=true&serverSelectionTimeoutMS=2000",
#         embedder=OllamaEmbedder(),
#     ),
# )
# knowledge_base.load(recreate=True)

# Store agent sessions in a SQLite database
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

knowledge_agent = Agent(
    name="Agno Assist",
    model=ds_model,
    instructions=[
        "Search your knowledge before answering the question.",
        "Only include the output in your response. No other text.",
    ],
    knowledge=knowledge,
    search_knowledge=True,
    storage=storage,
    add_datetime_to_instructions=True,
    # Add the chat history to the messages
    add_history_to_messages=True,
    # Number of history runs
    num_history_runs=3,
    show_tool_calls=True,
    markdown=True,
)

# 创建团队
lemonhall_assistant = Team(
    name="柠檬叔个人助手团队",
    mode="route",  # 使用路由模式，根据问题内容分发给合适的Agent
    model=ds_model,
    members=[
        knowledge_agent,
        personal_info_agent, 
        tech_env_agent, 
        dev_tools_agent, 
        project_agent, 
        server_agent, 
        ai_terms_agent,
        reasoning_agent,
        
    ],
    show_tool_calls=True,
    markdown=True,
    description="你是柠檬叔的个人助手，根据问题内容分发给最合适的专家Agent处理",
    instructions=[
        "识别用户问题的主题和类别，将其路由到最合适的Agent",
        "如果问题涉及多个领域，可以选择最相关的Agent或交给多个Agent处理",
        "保持中文回答，除非特殊情况",
        "对于创建新项目的请求，生成完整的命令序列并代用户命名",
        "对于文件系统危险操作，先进行确认",
        "给出的回答要简洁明了，避免不必要的解释"
    ],
    show_members_responses=True,
    enable_agentic_context=True,
    memory=memory,
    enable_team_history=True,
    num_of_interactions_from_history=5,
    enable_user_memories=True,
)

if __name__ == "__main__":
    print(whoami())
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print(model.get_sentence_embedding_dimension())
    # Drop the collection
    # client = MongoClient("mongodb://localhost:27017")
    # db = client["agno"]
    # db["agno_docs"].drop()

    print("柠檬叔个人助手已启动，请输入您的问题（输入'exit'退出）")
    while True:
        user_input = input("\n您的问题: ")
        if user_input.lower() == 'exit':
            break
      
        print("\n正在处理...\n")
        for chunk in lemonhall_assistant.run(user_input, stream=True):
            print(chunk.content, end="", flush=True)
        print("\n")

    
