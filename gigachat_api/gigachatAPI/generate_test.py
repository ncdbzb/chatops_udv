import os
import time
from typing import Any
from random import sample
from langchain.chat_models.gigachat import GigaChat
from gigachatAPI.config_data.config_data import *
from gigachatAPI.config_data.config import load_config, Config
from gigachatAPI.prompts.create_prompts import create_prompt
from gigachatAPI.process_files.split_long_elements import change_chunk_size
from gigachatAPI.utils.output_parser import parse_output
from gigachatAPI.utils.help_methods import get_tokens, len_yaml
from gigachatAPI.process_files.get_result_docs_list import get_result_docs_list
from gigachatAPI.logs.logs import logger_info


async def generate_test(filename: str, cur_que_num: int) -> str:
    config: Config = await load_config()

    giga: GigaChat = GigaChat(credentials=config.GIGA_CREDENTIALS, verify_ssl_certs=False)

    start_time = time.time()

    path_for_splitting = os.path.join('gigachatAPI', 'data', filename)
    split_docs = await get_result_docs_list(path_for_splitting, 'generate_test')

    data_process_time = time.time() - start_time

    prompt = await create_prompt(gen_que_sys_prompt_path, gen_que_usr_prompt_path)

    chain = prompt | giga

    document_length = sum(len(i.page_content) for i in split_docs)
    max_part_doc_len = max(len(i.page_content) for i in split_docs)

    total_que_num = cur_que_num

    logger_info.info(f'Вопросов нужно: {total_que_num} | Общая длина загруженного документа: {document_length}')
    logger_info.debug(f'Кол-во частей документа: {len(split_docs)} | Максимальная длина части документа: {max_part_doc_len}\n')
    logger_info.info(f'Время обработки данных: {data_process_time} секунд\n')

    # if document_length > 39000:
    if len(split_docs) < cur_que_num:
        if document_length // cur_que_num >= 1000:
            split_docs = await change_chunk_size(split_docs, chunk_size=(document_length // cur_que_num - 100))
            logger_info.debug(f'Кол-во частей после перерасчета: {len(split_docs)}')
        else:
            return 'Слишком много вопросов или слишком маленький документ для такого количества вопросов!'
    final_result = ''
    token_result = 0
    gigachat_start_time = time.time()
    while True:
        for doc_part in sample(split_docs, cur_que_num):
            result = await chain.ainvoke({"text": doc_part})
            final_result += result.content + '\n'
            token_result += len(doc_part.page_content)
        final_result, cur_que_num = await parse_output(final_result, cur_que_num, total_que_num)
        if cur_que_num:
            logger_info.debug(f'Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
            logger_info.debug(f'Генерирую еще {cur_que_num} вопросов\n')
            continue
        logger_info.debug(f'Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
        tokens = await get_tokens(len(final_result),
                                  total_que_num * await len_yaml(gen_que_sys_prompt_path),
                                  token_result)
        logger_info.info(f'Токенов потрачено: {tokens}\n')
        logger_info.info(f'Время работы GigaChat: {time.time() - gigachat_start_time} секунд')
        logger_info.info(f'Общее время: {time.time() - start_time} секунд')
        return final_result
    # else:
    #     final_result = ''
    #     iterations = 0
    #     gigachat_start_time = time.time()
    #     while True:
    #         iterations += 1
    #         final_result += await chain.ainvoke({"text": split_docs})
    #         final_result, cur_que_num = await parse_output(final_result, cur_que_num, total_que_num)
    #         if cur_que_num:
    #             logger_info.debug(f'Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
    #             logger_info.debug(f'Генерирую еще {cur_que_num} вопросов\n')
    #             continue
    #         logger_info.debug(f'Успешно сгенерировано {total_que_num - cur_que_num} вопросов')
    #         tokens = await get_tokens(len(final_result),
    #                                   iterations * await len_yaml(gen_que_sys_prompt_path),
    #                                   iterations * document_length)
    #         logger_info.info(f'Токенов потрачено: {tokens}\n\n')
    #         logger_info.info(f'Время работы GigaChat: {time.time() - gigachat_start_time} секунд')
    #         logger_info.info(f'Общее время: {time.time() - start_time} секунд')
    #         return final_result
