import httpx


BASE_URL = "http://127.0.0.1:8000"  # Замените на фактический URL вашего API

async def create_jwt_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/create_jwt_token", json={"token": token})
        return response.json()

async def signin(phone_number: str, password: str):
    async with httpx.AsyncClient() as client:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = await client.post(
            f"{BASE_URL}/auth/signin",
            json={"phone_number": phone_number, "password": password},
            headers=headers
        )
        return response.json()

async def get_courier_orders(courier_id: int, jwt_token: str):
    """
    Отправляет GET запрос на /order/couriers/{courier_id}/orders
    Параметры:
    - courier_id: int
    Заголовки:
    - Authorization: Bearer {jwt_token}
    Возвращает:
    - list: Список заказов курьера
    """
    async with httpx.AsyncClient() as client:
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {jwt_token}"
        }
        response = await client.get(f"{BASE_URL}/order/couriers/{courier_id}/orders", headers=headers)
        return response.json()

async def mark_order_as_delivered(order_id: int, courier_id: int, jwt_token: str, file_path: str, file_name: str, reason: str):
    async with httpx.AsyncClient() as client:
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {jwt_token}",
        }
        
        url = f"{BASE_URL}/order/orders/{order_id}/deliver"
        
        # Параметры запроса
        params = {
            "courier_id": courier_id,
            "reason": reason
        }
        
        # Открываем файл и готовим его для отправки
        files = {'file': (file_name, open(file_path, 'rb'), 'image/jpeg')}
        
        response = await client.post(url, headers=headers, params=params, files=files)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
        
        return response.json()

async def mark_order_as_undelivered(order_id: int, courier_id: int, reason: str, jwt_token: str):
    async with httpx.AsyncClient() as client:
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {jwt_token}"
        }
        
        url = f"{BASE_URL}/order/orders/{order_id}/undeliver"
        
        # Передаем параметры в виде словаря
        params = {
            "courier_id": courier_id,
            "reason": reason
        }
        
        response = await client.post(url, headers=headers, params=params)
        return response.json()

async def read_barcode(file_path: str, file_name: str):
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}/barcode/read-barcode/"
        headers = {"accept": "application/json"}
        files = {'file': (file_name, open(file_path, 'rb'), 'image/png')}

        response = await client.post(url, headers=headers, files=files)
        result = response.json()

        if result.get("status") == False:
            return {"type": None, "data": None}
        else:
            return {"type": result.get("type"), "data": result.get("data")}
