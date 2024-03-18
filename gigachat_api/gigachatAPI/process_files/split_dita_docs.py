import asyncio
import fnmatch
import os
import xml.etree.ElementTree as Et

from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter

from gigachatAPI.process_files.split_long_elements import split_long_elements
from gigachatAPI.utils.help_methods import get_doc_length


async def get_dita_docs(
    dita_path: str, chunk_size: int = 0,
    min_doc_length: int = 0, max_doc_length: int = 0
) -> list[Document]:

    async def get_dita_paths(directory_path: str) -> dict[str | bytes, int]:
        dit = {}
        for root, dirs, files in os.walk(directory_path):
            for file in fnmatch.filter(files, '*.dita'):
                file_path = os.path.join(root, file)
                dit[file_path] = await get_doc_length(file_path)
        return dit

    dita_dict = await get_dita_paths(dita_path)
    path_list_larger = [i for i, j in dita_dict.items() if j > min_doc_length]

    if chunk_size:
        very_long_string = ''.join(await asyncio.gather(*(extract_text_from_xml(path) for path in path_list_larger)))
        document = [Document(page_content=very_long_string)]
        docs = (CharacterTextSplitter(separator='\n', chunk_size=chunk_size, chunk_overlap=0)
                .split_documents(document))
    else:
        result_list = await asyncio.gather(*(extract_text_from_xml(path) for path in path_list_larger))

        docs = [
            Document(
                page_content=split,
            )
            for split in result_list
        ]

    if max_doc_length:
        max_part_doc_len = max(len(i.page_content) for i in docs)
        if max_part_doc_len > max_doc_length:
            docs = await split_long_elements(docs, max_doc_length)

    return docs


async def extract_text_from_xml(xml_file_path: str) -> str:
    tree = Et.parse(xml_file_path)
    root = tree.getroot()

    def get_text(element) -> str:
        extracted_text = element.text if element.text else ''
        for child in element:
            extracted_text += get_text(child)
            if child.tail:
                extracted_text += child.tail
        return extracted_text

    text = get_text(root)
    return text
