from .user_messages import Usuario, message_bank
import asyncio
import aiohttp  # Necesario para solicitudes HTTP asíncronas
import random

endpoint = "http://localhost:7071/api/Learnia_whatsapp"
# endpoint="https://chatbot-webhooks.azurewebsites.net/api/Learnia_whatsapp"

n_users = 5
n_iterations = 5


# Simulación asíncrona


async def send_message_async(session, user, message, delay):
    # Simular tiempo antes del envío
    await asyncio.sleep(delay)
    json_message = user.create_message(message)
    async with session.post(endpoint, json=json_message) as response:
        print(
            f"Status Code: {response.status}, User: {user.name}, Message: {message}, Delay: {delay}"
        )


async def simulate_users_messages_async(session, num_users, num_iterations):
    users = [
        Usuario(f"Usuario_Ficticio_{i}", f"57300555000{i}") for i in range(num_users)
    ]
    tasks = []

    Delay = [0 for _ in range(num_users)]

    for _ in range(num_iterations):
        Delay = [d + random.uniform(2.0, 4.0) for d in Delay]
        print(Delay)
        for i, user in enumerate(users):
            message = random.choice(message_bank)
            delay = Delay[i]
            # Programar la tarea sin esperar a que termine
            task = send_message_async(session, user, message, delay)
            tasks.append(asyncio.create_task(task))

    # Esperar a que todas las tareas programadas se completen
    await asyncio.gather(*tasks)


async def main():
    async with aiohttp.ClientSession() as session:
        await simulate_users_messages_async(session, n_users, n_iterations)


asyncio.run(main())
