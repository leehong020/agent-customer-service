from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import random
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path
import os
from utils.logger_handler import logger


rag = RagSummarizeService()
user_ids = ["1001","1002","1003","1004","1005","1006","1007","1008","1009","1010"] # 模拟用户ID列表
moonth_arr = ["2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12"] # 模拟月份列表
external_data = {} # 模拟外部数据存储，格式为{user_id: {month: {"特征": xxx, "效率": xxx}}}


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="获取指定城市的天气信息，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    # 这里可以调用天气API获取天气信息
    return f"{city}的天气是晴天，温度25度。"

@tool(description="获取当前所在城市的名称，以纯字符串的形式返回")
def get_user_location() -> str:
    return random.choice(["北京", "上海", "广州", "深圳"])

@tool(description="获取用户ID，以纯字符串的形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)

@tool(description="获取当前月份，以纯字符串的形式返回")
def get_current_month() -> str:
    return random.choice(moonth_arr)

def generate_external_data():
    """
    组成下面格式的数据：
    {
        "user_id": {
        "month": {"特征“：xxx，”效率":xxx},
        "month": {"特征“：xxx，”效率":xxx},
        "month": {"特征“：xxx，”效率":xxx}
        }
        "user_id": {
        "month": {"特征“：xxx，”效率":xxx},
        "month": {"特征“：xxx，”效率":xxx},
        "month": {"特征“：xxx，”效率":xxx}
        }
        "user_id": {
        "month": {"特征“：xxx，”效率":xxx},
        "month": {"特征“：xxx，”效率":xxx},
        "month": {"特征“：xxx，”效率":xxx}
        }
    }
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])
        
        if not os.path.exists(external_data_path):
            # 模拟生成外部数据文件
            raise FileNotFoundError(f"外部数据文件不存在: {external_data_path}")
        with open(external_data_path, 'r', encoding='utf-8') as f:
            for line in f.readlines()[1:]: # 跳过表头
                arr:list[str] = line.strip().split(",")
                
                user_id: str = arr[0].replace('"', '')
                feature: str = arr[1].replace('"', '')
                efficiency: str = arr[2].replace('"', '')
                consumables: str = arr[3].replace('"', '')
                comparison: str = arr[4].replace('"', '')
                time: str = arr[5].replace('"', '')

                if(user_id not in external_data):
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison
                }
# @tool(description="从外部系统中获取用户的使用记录，以纯字符串的形式返回，如果未检测到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()
    try:
        return external_data[user_id][month]  
    except KeyError:
        logger.warning(f"未检测到用户的使用记录，user_id: {user_id}, month: {month}")
        return ""
    
if __name__ == "__main__":
    print(fetch_external_data("1005", "2025-06"))