import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Import StaticFiles
from fastapi.responses import FileResponse # Import FileResponse

# --- Add project root to sys.path (same logic as in teams_consoles.py) ---
# This ensures that 'src.' imports work correctly when running with uvicorn
project_root = Path(__file__).resolve().parent.parent
frontend_dir = project_root / "frontend" # Define path to frontend directory
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

# --- Agent ID to Name mapping removed, no longer needed with the new approach --- 

# --- Define Request Body Model ---
class QueryRequest(BaseModel):
    query: str

app = FastAPI(
    title="柠檬叔个人助手 API",
    description="通过 HTTP API 与柠檬叔的 agno Agent 团队交互，并提供前端界面。", # Updated description
    version="0.1.0",
)

# --- CORS Configuration --- 
# Allow requests from typical frontend development ports and file origins
origins = [
    "http://localhost",
    "http://localhost:8000", # Add the app's own origin
    "http://localhost:3000", # Common React dev port
    "http://localhost:5173", # Common Vite dev port
    "http://127.0.0.1",
    "http://127.0.0.1:8000", # Add the app's own origin
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    # "null", # Remove null origin as we are serving the file now
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)
# --- End CORS Configuration ---

# --- API Endpoints --- 

@app.post("/ask", tags=["Agent Interaction"])
async def ask_agent(request: QueryRequest): # Accept QueryRequest model as body
    """
    向柠檬叔个人助手团队发送查询并获取响应 (使用 POST 请求体)。
    
    - **Request Body**:
        - `query` (str): 你想问的问题或指令。
    """
    query = request.query # Extract query from the request body object
    if not query:
        # Although Pydantic might handle empty validation, explicit check is fine
        return {"error": "Query in request body cannot be empty."}
    
    print(f"Received query via POST: {query}")
    handling_agent_name = "Unknown / Team Orchestrator" # Default value
    response_content = ""
    try:
        # IMPORTANT: Use stream=False for API calls to get the full response content
        response = lemonhall_assistant.run(query, stream=False)
        
        # --- Log and extract handling agent info from tool calls in messages --- 
        response_content = response.content
        
        # Search messages for the forward_task_to_member tool call
        if hasattr(response, 'messages') and isinstance(response.messages, list):
            found_forward = False
            for msg in reversed(response.messages): # Search backwards, likely faster
                if msg.role == 'tool' and msg.tool_name == 'forward_task_to_member':
                    if hasattr(msg, 'tool_args') and isinstance(msg.tool_args, dict):
                        # The 'member_id' in tool_args seems to hold the agent NAME
                        agent_name_from_tool = msg.tool_args.get('member_id') 
                        if agent_name_from_tool:
                            handling_agent_name = agent_name_from_tool
                            found_forward = True
                            break # Found the most recent forward
            if not found_forward:
                 print("Could not find 'forward_task_to_member' tool call in messages to determine handler.")
        else:
            print("'messages' attribute not found or not a list in the response object.")
            
        print(f"Query handled by: {handling_agent_name}")
        print(f"Agent response content: {response_content}")
        # --- End of logging --- 
        
        return {
            "handling_agent": handling_agent_name,
            "response": response_content
        }
    except Exception as e:
        print(f"Error during agent run: {e}")
        # In a real app, you might want more specific error handling and status codes
        return {
            "handling_agent": handling_agent_name, # Still return name even on error if known before fail
            "error": f"An error occurred: {e}",
            "response": response_content # Include any partial content if available before error
        }

# Renamed the old root endpoint
@app.get("/api-status", tags=["General"])
async def api_status():
    return {"message": "柠檬叔个人助手 API 正在运行。"}

# --- Frontend Serving --- 

# Serve the index.html at the root path
@app.get("/", include_in_schema=False) # Exclude from OpenAPI docs
async def read_index():
    index_path = frontend_dir / "index.html"
    if not index_path.is_file():
        return {"error": "Frontend index.html not found!"}, 404
    return FileResponse(str(index_path))

# Mount the rest of the frontend directory for static files (CSS, JS, images etc. if added later)
# This needs to be mounted AFTER the specific root route for index.html
# The path="/" means files in frontend/ will be accessible directly, e.g., /styles.css if frontend/styles.css exists
app.mount("/", StaticFiles(directory=frontend_dir), name="frontend")

# --- Main execution block --- 

if __name__ == "__main__":
    print(f"API server starting...")
    print(f"Frontend directory set to: {frontend_dir}")
    print(f"Attempting to serve index.html from: {frontend_dir / 'index.html'}")
    # Run the FastAPI app using Uvicorn
    # Use reload=True for development to automatically reload on code changes
    uvicorn.run("src.api_server:app", host="0.0.0.0", port=8000, reload=True) 