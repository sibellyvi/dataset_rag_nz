import json


# Carrega os documentos
with open("documentos.jsonl", "r", encoding="utf-8") as arquivo:
    documentos = []

    for linha in arquivo:
        documentos.append(json.loads(linha))


# Vamos dividir cada documento em pedaços
# de aproximadamente 100 palavras.
chunks = []

for documento in documentos:

    palavras = documento["text"].split()

    for i in range(0, len(palavras), 100):

        trecho = " ".join(palavras[i:i + 100])

        chunks.append({
            "id": documento["id"],
            "chunk": trecho
        })


print("Quantidade de chunks:", len(chunks))

print("\nQuarto chunk:")
print(chunks[3]["chunk"])