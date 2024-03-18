import os

from gigachatAPI.utils.help_methods import extract_zip


async def process_and_take_path(filename: str, file_path: str) -> str:

    if filename.split('.')[-1] == 'zip':
        file_name_without_extension = '.'.join(filename.split('.')[:-1])
        unpack_path = f'gigachatAPI/data/{file_name_without_extension}'
        await extract_zip(file_path, unpack_path)
        os.remove(file_path)
        file_path = unpack_path
        print(f'unpacked {filename}')
    return file_path


# def del_if_exist() -> None:
#     folder_path = 'gigachatAPI/data'
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#
#         if filename != "__init__.py":
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#                 print(f'удален файл {filename}')
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#                 print(f'удалена директория {filename}')
