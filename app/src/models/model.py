import requests
import json

class MistralModel:
    def __init__(self):
        self.config = json.load(open("models/secrest_config.json"))
        self.api_key = self.config.get("api_key")
        self.url = self.config.get("url")
        self.model = self.config.get("mistral_model")

    def chat(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(self.url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
