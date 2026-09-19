import json
from sentence_transformers import SentenceTransformer


# Carrega os chunks
with open("documentos.jsonl", "r", encoding="utf-8") as arquivo:
    documentos = []

    for linha in arquivo:
        documentos.append(json.loads(linha))


# Divide os documentos novamente em chunks
chunks = []

for documento in documentos:

    palavras = documento["text"].split()

    for i in range(0, len(palavras), 100):

        trecho = " ".join(palavras[i:i + 100])

        chunks.append({
            "id": documento["id"],
            "chunk": trecho
        })


# Carrega o modelo de embeddings
modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# Gera um embedding para cada chunk
textos = [chunk["chunk"] for chunk in chunks]

embeddings = modelo.encode(textos)


print("Quantidade de chunks:", len(chunks))
print("Quantidade de embeddings:", len(embeddings))
print("Tamanho de cada embedding:", len(embeddings[0]))