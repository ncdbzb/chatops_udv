import asyncio
import os
import time

from aiohttp import web

from gigachatAPI.answer_questions import get_answer
from gigachatAPI.generate_test import generate_test
from gigachatAPI.process_files.process_paths import process_and_take_path
from gigachatAPI.chromadb.chromadb_handler import initialize_chroma
from gigachatAPI.process_files.get_result_docs_list import get_result_docs_list


async def handle_doc(request):
    start_time = time.time()
    data = await request.post()
    file = data['file']
    save_path = os.path.join('gigachatAPI', 'data', file.filename)
    with open(save_path, 'wb') as file_object:
        file_object.write(file.file.read())
    print(f'saved {file.filename} with timeL {time.time() - start_time}')
    path = await process_and_take_path(file.filename, save_path)

    split_docs = await get_result_docs_list(path, 'initialize_chroma')

    await initialize_chroma(split_docs, path.split('/')[-1])
    print(f'time: {time.time() - start_time}')

    return web.json_response({"result": "File was received"})


async def handle_test(request):
    data = await request.json()
    print("Received data:", data)
    result = await generate_test(data['filename'], data['que_num'])
    print("Responsed data:", result)
    return web.json_response({"result": result})


async def handle_questions(request):
    data = await request.json()
    print("Received data:", data)
    result = await get_answer(data['filename'], [data['question']])
    print("Responsed data:", result)
    return web.json_response({"result": result})


async def main():
    app = web.Application(client_max_size=100*1024*1024)
    app.router.add_post('/process_data', handle_test)
    app.router.add_post('/process_questions', handle_questions)
    app.router.add_post('/process_doc', handle_doc)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '0.0.0.0', 8001)
    await site.start()

    print("gigachatAPI started")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
