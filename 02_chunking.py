import json


# Carrega os documentos
with open("documentos.jsonl", "r", encoding="utf-8") as arquivo:
    documentos = []

    for linha in arquivo:
        documentos.append(json.loads(linha))


# Configurações dos chunks
tamanho_chunk = 100
overlap = 20

chunks = []


for documento in documentos:

    palavras = documento["text"].split()

    inicio = 0

    while inicio < len(palavras):

        fim = inicio + tamanho_chunk

        trecho = " ".join(palavras[inicio:fim])

        chunks.append({
            "id": documento["id"],
            "chunk": trecho
        })

        # Avança 80 palavras.
        # As últimas 20 palavras serão repetidas
        # no próximo chunk.
        inicio += tamanho_chunk - overlap


print("Quantidade de chunks:", len(chunks))

print("\nPrimeiro chunk:")
print(chunks[0]["chunk"])

print("\nSegundo chunk:")
print(chunks[1]["chunk"])