import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("MODEL_API_KEY")
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Привет! Ответь одним словом: работает?",
    )
    print("Успех! Ответ:")
    print(response.text)
except Exception as e:
    print(f"Ошибка при запросе: {e}")
