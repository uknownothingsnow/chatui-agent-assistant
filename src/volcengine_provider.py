from agno.models.deepseek import DeepSeek
from agno.models.base import Model
from src.config import V3_MODEL_ID, R1_MODEL_ID, DEFAULT_VOLCENGINE_BASE_URL

#litellm初始化火山引擎的方法
#V3的模型
# llm = LLM(model="volcengine/ep-20250204220334-l2q5g", 
#           api_key=huoshan_key,temperature=0)

#R1的模型
# llm = LLM(model="volcengine/ep-20250204215316-p8rqb", 
#           api_key=huoshan_key,temperature=0)


# 使用 PowerShell
# 打开 PowerShell（在 "开始" 菜单中搜索 "PowerShell" 并打开）。
# 要为当前用户设置环境变量，可以使用
# $env:SILICONFLOW_API_KEY = "your_api_key"
# 命令。
# 同样，将"your_api_key"替换为实际的 API 密钥。不过，这种方式设置的环境变量只在当前 PowerShell 会话中有效。

# 要永久设置环境变量（对于当前用户），可以使用
# [Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY","your_api_key","User")。
# 如果要设置系统级别的环境变量（需要管理员权限），可以将最后一个参数改为"Machine"，
# 例如
# [Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY","your_api_key","Machine")。
# Set up SILICONFLOW API key
# 记得使用以上方法后，需要关闭vscode后重启vscode，之后点击F5运行python脚本的时候才能生效

# --- Model and Path Setup ---
# Instantiate the model provider and get the model instance
# Use V3 by default, adjust model_id if needed (e.g., VolcEngineModelProvider.R1)
# 使用方法：
# model_provider = VolcEngineModelProvider(model_id=VolcEngineModelProvider.V3)
# ds_model = model_provider.get_model() # Get the actual model instance

# --- Encapsulation for VolcEngine DeepSeek Model ---
class VolcEngineModelProvider:
    """Manages the initialization of DeepSeek models via VolcEngine."""

    V3 = V3_MODEL_ID
    R1 = R1_MODEL_ID
    DEFAULT_BASE_URL = DEFAULT_VOLCENGINE_BASE_URL

    def __init__(self, model_id: str = V3, base_url: str = DEFAULT_BASE_URL):
        """
        Initializes the VolcEngineModel provider.

        Args:
            model_id: The specific model ID to use (e.g., V3 or R1). Defaults to V3.
            base_url: The base URL for the VolcEngine API.
        """
        self.model_id = model_id
        self.base_url = base_url
        self._model_instance: Model | None = None  # Type hint for the instance variable

    def get_model(self) -> Model:
        """Returns an initialized DeepSeek model instance."""
        if self._model_instance is None:
            # DeepSeek class reads DEEPSEEK_API_KEY from environment variables automatically
            self._model_instance = DeepSeek(id=self.model_id, base_url=self.base_url)
            print(f"Initialized DeepSeek model: {self.model_id} via {self.base_url}")
        return self._model_instance 

if __name__ == "__main__":
    print("Demonstrating VolcEngineModelProvider usage...")
    
    # 1. Initialize the provider (using default V3 model)
    print("\nInitializing provider with default settings (V3 model)...")
    provider_v3 = VolcEngineModelProvider()
    model_v3 = provider_v3.get_model()
    print(f"Got model instance: {model_v3}")
    # Attempting to get the model again should return the cached instance
    model_v3_cached = provider_v3.get_model()
    print(f"Got model instance again (cached): {model_v3_cached}")
    assert model_v3 is model_v3_cached # Verify it's the same instance
    print("Verified that subsequent calls return the cached instance.")

    # 2. Initialize the provider with a different model (R1)
    print("\nInitializing provider with R1 model...")
    provider_r1 = VolcEngineModelProvider(model_id=VolcEngineModelProvider.R1)
    model_r1 = provider_r1.get_model()
    print(f"Got model instance: {model_r1}")

    # Note: This demonstration assumes the DEEPSEEK_API_KEY environment variable is set.
    # If not set, the DeepSeek() initialization within get_model() might fail or use a default key.
    print("\nDemonstration complete.") 