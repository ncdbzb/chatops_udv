import httpx


async def send_file_to_llm(file_path: str):
    async with httpx.AsyncClient() as client:
        url = "http://gigachat_api:8080/process_doc"
        with open(file_path, "rb") as file:
            files = {"file": (file.name.split('/')[-1], file, "application/octet-stream")}
            response = await client.post(url, files=files, timeout=30)
            print(response.text)
            return response.json()
