import httpx


async def send_file_to_llm(file_path: str):
    async with httpx.AsyncClient() as client:
        url = "http://localhost:8001/process_doc"
        with open(file_path, "rb") as file:
            files = {"file": ('name', file, "application/octet-stream")}
            response = await client.post(url, files=files)
            print(response.text)
            return response.json()
