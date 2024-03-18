import zipfile
from typing import Optional

import yaml
import os


async def extract_zip(zipfile_path: str, extracted_files_path: str) -> None:
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_files_path)


async def get_doc_length(path_doc: str) -> int:
    with open(path_doc, 'r', encoding='utf-8') as file:
        content = file.read()
        return len(content)


async def get_tokens(s1: int, s2: int, ln: Optional[int] = 0) -> int:
    sm = sum((s1, s2, ln))
    return (sm // 3 + sm // 4) // 2


async def len_yaml(path_yaml: str) -> int:
    with open(path_yaml, encoding='utf-8') as fh:
        dict_data = yaml.safe_load(fh)
        result = sum(map(len, filter(None, dict_data.values())))
        return result
