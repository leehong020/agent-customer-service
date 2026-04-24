import yaml
from path_tool import get_abs_path

def load_rag_config(config_path:str=get_abs_path("config/rag.yaml"),encoding:str='utf-8') -> dict:
    """
    加载RAG配置文件
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    



def load_chroma_config(config_path:str=get_abs_path("config/chroma.yaml"),encoding:str='utf-8') -> dict:
    """
    加载chroma配置文件
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    


def load_prompts_config(config_path:str=get_abs_path("config/prompts.yaml"),encoding:str='utf-8') -> dict:
    """
    加载Prompts配置文件
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    

def load_agent_config(config_path:str=get_abs_path("config/agent.yaml"),encoding:str='utf-8') -> dict:
    """
    加载Agent配置文件
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()


if __name__ == "__main__":
    print(rag_conf["chat_model_name"])
    print(rag_conf["embedding_model_name"])