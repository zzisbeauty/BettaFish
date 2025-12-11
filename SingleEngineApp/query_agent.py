import sys
from pathlib import Path  
sys.path.insert(0, str(Path(__file__).parent.parent))  

from QueryEngine import DeepSearchAgent, Settings
from config import settings


# agent settings
config = Settings(
    QUERY_ENGINE_API_KEY = "vllm",
    QUERY_ENGINE_BASE_URL = "http://192.168.1.6:1128/v1",
    QUERY_ENGINE_MODEL_NAME = "/localmodels/Qwen3-4B-Thinking-2507",
    QUERY_ENGINE_PROVIDER = "vllm",
    TAVILY_API_KEY = "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",
    OUTPUT_DIR = "./query_result"
)


agent =  DeepSearchAgent(config=config)


# 执行查询  并执行特定 node (step) 的结果
query = "2026年AI发展趋势"  
agent._generate_report_structure(query)  
agent._initial_search_and_summary(0)  
final_report = agent._generate_final_report()  
print(final_report)