# 私有数据库信息挖掘


import os  
import sys  
from datetime import datetime  
  
# 添加项目路径  
sys.path.insert(0, os.path.dirname(__file__))  
  
from InsightEngine import DeepSearchAgent, Settings  
from config import settings  
  
def main():  
    """运行 Insight Agent"""  
    # 配置参数  
    query = "武汉大学品牌声誉分析"  # 你的查询内容  
      
    # 创建配置（必须使用大写字段名）  
    config = Settings(  
        INSIGHT_ENGINE_API_KEY=settings.INSIGHT_ENGINE_API_KEY,  
        INSIGHT_ENGINE_BASE_URL=settings.INSIGHT_ENGINE_BASE_URL,  
        INSIGHT_ENGINE_MODEL_NAME=settings.INSIGHT_ENGINE_MODEL_NAME or "kimi-k2-0711-preview",  
        DB_HOST=settings.DB_HOST,  
        DB_USER=settings.DB_USER,  
        DB_PASSWORD=settings.DB_PASSWORD,  
        DB_NAME=settings.DB_NAME,  
        DB_PORT=settings.DB_PORT,  
        DB_CHARSET=settings.DB_CHARSET,  
        DB_DIALECT=settings.DB_DIALECT,  
        MAX_REFLECTIONS=2,  
        MAX_CONTENT_LENGTH=500000,  
        OUTPUT_DIR="insight_engine_reports"  
    )  
      
    # 初始化并运行代理  
    agent = DeepSearchAgent(config)  
      
    # 执行完整研究流程  
    agent._generate_report_structure(query)  
      
    # 处理每个段落  
    for i in range(len(agent.state.paragraphs)):  
        agent._initial_search_and_summary(i)  
        agent._reflection_loop(i)  
        agent.state.paragraphs[i].research.mark_completed()  
      
    # 生成并保存报告  
    final_report = agent._generate_final_report()  
    agent._save_report(final_report)  
      
    print(f"研究完成！报告已保存到: {config.OUTPUT_DIR}")  
    print(f"报告标题: {agent.state.report_title}")  
  
if __name__ == "__main__":  
    main()