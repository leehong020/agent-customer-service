from config_handler import prompts_conf
from path_tool import get_abs_path
from logger_handler import logger
def load_system_prompts():
    """
    加载系统提示词
    """
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"主提示词路径配置缺失: {str(e)}")
        raise e
    
    try:
        return open(system_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"解析系统主提示词失败: {system_prompt_path}, 错误信息: {str(e)}")
        raise e
    


def load_rag_prompts():
    """
    加载RAG提示词
    """
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"RAG提示词路径配置缺失: {str(e)}")
        raise e
    
    try:
        return open(rag_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"解析RAG提示词失败: {rag_prompt_path}, 错误信息: {str(e)}")
        raise e
    

def load_report_prompts():
    """
    加载报告提示词
    """
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"报告提示词路径配置缺失: {str(e)}")
        raise e
    
    try:
        return open(report_prompt_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"解析报告提示词失败: {report_prompt_path}, 错误信息: {str(e)}")
        raise e
        

if __name__ == "__main__":
    print(load_system_prompts())
    print(load_rag_prompts())
    print(load_report_prompts())