import httpx


async def send_data_to_llm(endpoint: str, data: dict):
    async with httpx.AsyncClient(timeout=30) as client:
        url = f"http://gigachat_api:8080/{endpoint}"
        response = await client.post(url, json=data)
        return response.json()
