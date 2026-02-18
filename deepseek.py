import requests
import json
import time
from config import DEEPSEEK_KEY


class DeepSeekClient:
    def __init__(self):
        self.api_key = DEEPSEEK_KEY
        self.url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        print("✅ DeepSeek клиент готов")

    def generate_response(self, prompt):
        try:
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()

            result = response.json()
            answer = result['choices'][0]['message']['content']

            return answer

        except Exception as e:
            print(f"❌ Ошибка при генерации ответа: {e}")
            return "Извините, произошла ошибка при обработке запроса."