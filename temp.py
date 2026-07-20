from backend.llm.gemini_client import GeminiClient
from backend.llm.models import LLMRequest


client = GeminiClient()


request = LLMRequest(
    user_prompt="Explain neural networks in one sentence"
)


response = client.generate(request)


print(response.text)
print(response.model_used)
print(response.latency_ms)