from agno.agent import Agent
from agno.knowledge.url import UrlKnowledge
from agno.vectordb.mongodb import MongoDb
from agno.vectordb.search import SearchType
from agno.embedder.ollama import OllamaEmbedder
from agno.storage.sqlite import SqliteStorage

def create_knowledge_agent(model):
    knowledge = UrlKnowledge(
        urls=["https://docs.agno.com/introduction/agents.md"],
        vector_db=MongoDb(
            db_url="mongodb://localhost:27017/?directConnection=true&serverSelectionTimeoutMS=2000",
            collection_name="agno_docs",
            search_type=SearchType.hybrid,
            search_index_name="agno_docs",
            embedder=OllamaEmbedder(),
        ),
        show_tool_calls=True,
    )
    
    knowledge.load(recreate=True)
    
    storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")
    
    return Agent(
        name="Agno Assist",
        model=model,
        instructions=[
            "Search your knowledge before answering the question.",
            "Only include the output in your response. No other text.",
        ],
        knowledge=knowledge,
        search_knowledge=True,
        storage=storage,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_runs=3,
        show_tool_calls=True,
        markdown=True,
    )