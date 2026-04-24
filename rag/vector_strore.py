from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from model.factory import embedding_model   
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils.path_tool import get_abs_path    
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from langchain_core.documents import Document 


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            persist_directory=chroma_conf["persist_directory"],
            embedding_function = embedding_model,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function = len
            )
        

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})
    
    def load_document(self, documents:list[str] | None = None):
        """
        从数据文件夹里面读取数据文件，转为向量存入向量数据库
        要计算文件的md5值，判断是否已经存入过向量数据库，避免重复存储
        ：return None
        """
        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                #文件不存在，创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), 'w', encoding='utf-8').close()
                return False
            
            with open(get_abs_path(chroma_conf["md5_hex_store"]), 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True # md5值已经存在，说明文件已经存储过向量数据库了 
                return False # md5值不存在，说明文件没有存储过向量数据库，需要存储
            

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), 'a', encoding='utf-8') as f:
                f.write(md5_for_check + '\n')

        def get_file_documents(file_path: str):
            if file_path.endswith(".pdf"):
                return pdf_loader(file_path)
            elif file_path.endswith(".txt"):
                return txt_loader(file_path)
            else:
                logger.error(f"不支持的文件类型: {file_path}")
                return []
            
        allowed_files_path: list[str] = listdir_with_allowed_type(
            chroma_conf["data_path"],
            tuple(chroma_conf["allow_konwledge_file_type"])
        )
        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"文件已经存储过向量数据库了，跳过文件: {path}")
                continue
            # documents = get_file_documents(path)
            # if not documents:
            #     logger.warning(f"文件没有解析出文档，跳过文件: {path}")
            #     continue
            # self.vector_store.add_documents(documents)
            # save_md5_hex(md5_hex)
            # logger.info(f"成功将文件存储到向量数据库: {path}")

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"文件没有解析出文档，跳过文件: {path}")
                    continue

                split_document: list[Document] = self.spliter.split_documents(documents)

                if(not split_document):
                    logger.warning(f"文件没有解析出分块文档，跳过文件: {path}")
                    continue
                # 将内容存入向量数据库
                self.vector_store.add_documents(split_document)

                # 保存文件的md5值，避免重复存储
                save_md5_hex(md5_hex)

                logger.info(f"成功将文件存储到向量数据库: {path}")
            except Exception as e:
                #exc_info=True可以打印出完整的错误堆栈信息，方便调试
                logger.error(f"处理文件失败: {path}, 错误信息: {str(e)}",exc_info=True)



if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)