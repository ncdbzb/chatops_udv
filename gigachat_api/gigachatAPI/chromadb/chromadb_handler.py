from typing import Any
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Chroma


async def initialize_chroma(split_docs: list[Document], filename: str) -> None:
    persist_directory = f"gigachatAPI/data/chroma/{filename}"
    Chroma.from_documents(documents=split_docs,
                          embedding=SentenceTransformerEmbeddings(),
                          persist_directory=persist_directory)
    print(f'chroma initialized at {persist_directory}\n')
    return


async def get_chroma(filename: str) -> Any:
    persist_directory = f"gigachatAPI/data/chroma/{filename}"
    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=SentenceTransformerEmbeddings())
    return vectordb
