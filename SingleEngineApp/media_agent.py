import asyncio
import os, sys
from pathlib import Path


# 基于文本查询检索多模态数据：Agent 接收文本查询，通过 Bocha 搜索 API 返回包含网页、图片、视频、结构化数据卡片的多模态结果，而不是直接处理图片/视频文件


# 添加项目根目录到 Python 路径  
# project_root = Path(__file__).parent  
# sys.path.insert(0, str(project_root))  
sys.path.insert(0, str(Path(__file__).parent.parent))  


from MediaEngine.agent import DeepSearchAgent  
from MediaEngine.utils.config import Settings  
from loguru import logger  


def test_media_agent():  
    """测试 Media Agent 核心功能"""  
      
    # 配置日志  
    logger.add("media_agent_test.log", rotation="10 MB", level="INFO")  
      
    try:  
        # 1. 初始化配置  
        logger.info("正在初始化 Media Agent 配置...")  
        config = Settings()  
          
        # 2. 创建 Media Agent 实例  
        logger.info("正在创建 Media Agent 实例...")  
        agent = DeepSearchAgent(config)  
          
        # 3. 设置测试查询  
        test_query = "分析近期关于人工智能发展的多模态内容"  
        logger.info(f"测试查询: {test_query}")  
          
        # 4. 生成报告结构  
        logger.info("正在生成报告结构...")  
        agent._generate_report_structure(test_query)  
        logger.info(f"生成了 {len(agent.state.paragraphs)} 个段落")  
          
        # 5. 处理每个段落  
        for i, paragraph in enumerate(agent.state.paragraphs):  
            logger.info(f"正在处理段落 {i+1}: {paragraph.title}")  
              
            # 初始搜索和总结  
            agent._initial_search_and_summary(i)  
              
            # 反思循环（最多3次）  
            agent._reflection_loop(i)  
              
            # 标记段落完成  
            paragraph.research.mark_completed()  
            logger.info(f"段落 {i+1} 处理完成")  
          
        # 6. 生成最终报告  
        logger.info("正在生成最终报告...")  
        final_report = agent._generate_final_report()  
          
        # 7. 保存报告  
        logger.info("正在保存报告...")  
        agent._save_report(final_report)  
          
        # 8. 输出结果摘要  
        print("\n" + "="*50)  
        print("Media Agent 测试完成！")  
        print("="*50)  
        print(f"查询: {test_query}")  
        print(f"报告标题: {agent.state.report_title}")  
        print(f"段落数量: {len(agent.state.paragraphs)}")  
        print(f"报告长度: {len(final_report)} 字符")  
        print(f"报告已保存到: media_engine_streamlit_reports/")  
        print("="*50)  
          
        return True  
          
    except Exception as e:  
        logger.exception(f"测试过程中发生错误: {e}")  
        print(f"错误: {e}")  
        return False  
  
if __name__ == "__main__":  
    # 检查环境变量  
    required_env_vars = [  
        "MEDIA_ENGINE_API_KEY",  
        "MEDIA_ENGINE_BASE_URL",    # LLM server
        "MEDIA_ENGINE_MODEL_NAME",  
        "BOCHA_WEB_SEARCH_API_KEY"  
    ]  
      
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]  
    if missing_vars:  
        print(f"错误: 缺少必需的环境变量: {', '.join(missing_vars)}")  
        print("请确保在 .env 文件中设置了这些变量")  
        sys.exit(1)  
      
    # 运行测试  
    success = test_media_agent()  
    sys.exit(0 if success else 1)