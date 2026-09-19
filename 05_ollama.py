from ollama import chat


resposta = chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Qual é a capital da Nova Zelândia?"
        }
    ]
)


print(resposta.message.content)