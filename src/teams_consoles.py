import sys
import os
from pathlib import Path
from agno.agent import Agent
from huggingface_hub import whoami
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from rich.pretty import pprint


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

# Import agent creation functions
from src.agents.personal_info_agent import create_personal_info_agent
from src.agents.tech_env_agent import create_tech_env_agent
from src.agents.dev_tools_agent import create_dev_tools_agent
from src.agents.project_agent import create_project_agent
from src.agents.server_agent import create_server_agent
from src.agents.ai_terms_agent import create_ai_terms_agent
from src.agents.reasoning_agent import create_reasoning_agent
from src.agents.knowledge_agent import create_knowledge_agent

# 创建各个专业Agent
personal_info_agent = create_personal_info_agent(ds_model)
tech_env_agent = create_tech_env_agent(ds_model)
dev_tools_agent = create_dev_tools_agent(ds_model)
project_agent = create_project_agent(ds_model)
server_agent = create_server_agent(ds_model)
ai_terms_agent = create_ai_terms_agent(ds_model)
reasoning_agent = create_reasoning_agent(ds_model)
knowledge_agent = create_knowledge_agent(ds_model)

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

        # Print metrics per message
        if lemonhall_assistant.run_response.messages:
            for message in lemonhall_assistant.run_response.messages:
                if message.role == "assistant":
                    if message.content:
                        print(f"Message: {message.content}")
                    elif message.tool_calls:
                        print(f"Tool calls: {message.tool_calls}")
                    print("---" * 5, "Metrics", "---" * 5)
                    pprint(message.metrics)
                    print("---" * 20)

        # Print the aggregated metrics for the whole run
        print("---" * 5, "Collected Metrics", "---" * 5)
        pprint(lemonhall_assistant.run_response.metrics)
    
