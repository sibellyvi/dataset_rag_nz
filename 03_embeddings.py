import json
from sentence_transformers import SentenceTransformer


# Carrega os documentos
with open("documentos.jsonl", "r", encoding="utf-8") as arquivo:
    documentos = []

    for linha in arquivo:
        documentos.append(json.loads(linha))


# Configurações dos chunks
tamanho_chunk = 100
overlap = 20

chunks = []


# Cria os chunks com overlap
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

        inicio += tamanho_chunk - overlap


# Carrega o modelo de embeddings
modelo = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)


# Gera um embedding para cada chunk
textos = [chunk["chunk"] for chunk in chunks]

embeddings = modelo.encode(textos)


print("Quantidade de chunks:", len(chunks))
print("Quantidade de embeddings:", len(embeddings))
print("Tamanho de cada embedding:", len(embeddings[0]))