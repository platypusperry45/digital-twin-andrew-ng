from backend.rag import Retriever

retriever = Retriever()

response = retriever.retrieve(
    "Who is Andrew Ng?"
)

print()

print(response)

print()

for item in response.results:

    print("=" * 60)

    print(item.score)

    print(item.text)

    print(item.filename)