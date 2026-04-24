"""
为整个工程提供统一的绝对路径
""" 
import os

def get_project_root() -> str:
    """
    获取项目根目录的绝对路径
    """

    # 获取当前文件的绝对路径，向上两级目录，即项目根目录
    current_file = os.path.abspath(__file__)
    # 获取项目根目录,获取文件所在的文件夹的绝对路径
    current_dir = os.path.dirname(current_file)
    # 获取项目根目录,获取文件所在的文件夹的父级目录的绝对路径
    project_root = os.path.dirname(current_dir)
    return project_root

def get_abs_path(relative_path: str) -> str:
    """
    将相对路径转换为绝对路径
    """
    project_root = get_project_root()
    abs_path = os.path.join(project_root, relative_path)
    return abs_path

if __name__ == "__main__":
    # 测试函数
    # print(get_project_root())
    print(get_abs_path("data/sample_data.csv"))
