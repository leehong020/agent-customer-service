import os,hashlib
from path_tool import get_abs_path
from logger_handler import logger
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain_core.document import Document    
def get_file_md5_hex(file_path: str):
    if not os.path.exists(file_path):
        logger.error(f"md5计算文件不存在: {file_path}")

    if not os.path.isfile(file_path):
        logger.error(f"md5计算路径不是文件: {file_path}")
    md5 = hashlib.md5()

    #文档分块读取，避免大文件占用过多内存
    chunk_size = 4096
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size)
                md5_obj.update(chunk)
            """
            chunk = f.read(chunk_size)
            while chunk:
                md5.update(chunk)
                chunk = f.read(chunk_size)
            """
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件md5失败: {file_path}, 错误信息: {str(e)}")
        return None



def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """
    列出指定路径下的所有文件，过滤掉不允许的文件类型
    """
    files = []
    if not os.path.isdir(path):
        logger.error(f"路径不是一个目录: {path}")
        return allowed_types
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
    return tuples(files)

def pdf_loader(file_path:str,passwd = None) -> list[Document]:
    return PyPDFLoader(file_path, passwd).load()

def txt_loader(file_path:str,passwd = None) -> list[Document]:
    return TextLoader(file_path,passwd).load()

