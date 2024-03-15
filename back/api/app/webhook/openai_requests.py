import openai
import requests 

class OpenAIRequests:
    def __init__(self):
        openai.api_key = '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'

    def request_gpt(self, query):
        payload =   {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": query}],
            "temperature": 0.7
        }
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {openai.api_key}"},
                                    json=payload)
        return response.json()

