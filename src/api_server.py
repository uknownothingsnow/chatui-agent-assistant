import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# --- Add project root to sys.path (same logic as in teams_consoles.py) ---
# This ensures that 'src.' imports work correctly when running with uvicorn
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
# --- End of dynamic path addition ---

# Import the pre-configured team instance from the console script
# This reuses the same agents, memory, and model setup
try:
    from src.teams_consoles import lemonhall_assistant
except ImportError as e:
    print(f"Error importing lemonhall_assistant: {e}")
    print("Ensure you are running this from the project root directory or sys.path is correctly configured.")
    sys.exit(1)

# --- Define Request Body Model ---
class QueryRequest(BaseModel):
    query: str

app = FastAPI(
    title="柠檬叔个人助手 API",
    description="通过 HTTP API 与柠檬叔的 agno Agent 团队交互。",
    version="0.1.0",
)

# Change GET to POST and accept request body
@app.post("/ask", tags=["Agent Interaction"])
async def ask_agent(request: QueryRequest):
    """
    向柠檬叔个人助手团队发送查询并获取响应 (使用 POST 请求体)。
    
    - **Request Body**:
        - `query` (str): 你想问的问题或指令。
    """
    query = request.query
    if not query:
        return {"error": "Query in request body cannot be empty."}
    
    print(f"Received query via POST: {query}")
    try:
        # IMPORTANT: Use stream=False for API calls to get the full response content
        response = lemonhall_assistant.run(query, stream=False)
        print(f"Agent response content: {response.content}")
        return {"response": response.content}
    except Exception as e:
        print(f"Error during agent run: {e}")
        # In a real app, you might want more specific error handling and status codes
        return {"error": f"An error occurred: {e}"}

# Add a simple root endpoint for health check or info
@app.get("/", tags=["General"])
async def read_root():
    return {"message": "柠檬叔个人助手 API 正在运行。访问 /docs 查看 API 文档。"}

if __name__ == "__main__":
    print("Starting Uvicorn server...")
    # Run the FastAPI app using Uvicorn
    # Use reload=True for development to automatically reload on code changes
    uvicorn.run("src.api_server:app", host="0.0.0.0", port=8000, reload=True) 