import os

from langchain.schema import Document
from gigachatAPI.process_files.split_dita_docs import get_dita_docs
from gigachatAPI.process_files.split_other_docs import get_text_docs_list


async def get_result_docs_list(file_path: str, operation: str) -> list[Document]:
    """
    Функция получает путь к файлу и создает список документов, разбивая на части содержимое файла.
    Используются разные методы предварительной обработки и разные параметры разбиения, в зависимости
    от типа файла и операции, в которой в дальнейшем будут использоваться выходные данные.

    :param file_path: Путь к файлу
    :param operation: Операция
    :return: Список документов (отрывков содержимого)
    """
    if os.path.isdir(file_path):
        if operation in ('answer_questions', 'initialize_chroma'):
            split_docs = await get_dita_docs(file_path, chunk_size=10000)
        else:
            split_docs = await get_dita_docs(file_path, min_doc_length=1000, max_doc_length=7000)
    else:
        if operation in ('answer_questions', 'initialize_chroma'):
            split_docs = await get_text_docs_list(file_path, separator='\n', chunk_size=10000)
        else:
            split_docs = await get_text_docs_list(file_path+'.txt', chunk_size=7000)
    return split_docs
