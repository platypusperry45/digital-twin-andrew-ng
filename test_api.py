import requests


response = requests.post(
    "http://127.0.0.1:8000/api/v1/chat",
    json={
        "prompt": "Explain gradient descent in simple words"
    }
)


print(response.json())