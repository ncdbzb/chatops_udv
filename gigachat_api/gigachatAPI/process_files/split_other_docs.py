from langchain.document_loaders import TextLoader
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter


async def get_text_docs_list(file_path: str, separator='\n', chunk_size=10000, chunk_overlap=500) -> list[Document]:
    document = TextLoader(file_path, encoding='utf-8').load()
    split_docs = (CharacterTextSplitter(separator=separator, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                  .split_documents(document))
    return split_docs
