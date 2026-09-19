import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Carrega os documentos
with open("documentos.jsonl", "r", encoding="utf-8") as arquivo:
    documentos = []

    for linha in arquivo:
        documentos.append(json.loads(linha))


# Cria os chunks
chunks = []

for documento in documentos:

    palavras = documento["text"].split()

    for i in range(0, len(palavras), 100):

        trecho = " ".join(palavras[i:i + 100])

        chunks.append({
            "id": documento["id"],
            "chunk": trecho
        })


# Carrega o modelo
modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# Gera embeddings dos chunks
textos = [chunk["chunk"] for chunk in chunks]

embeddings_chunks = modelo.encode(textos)


# Pergunta do usuário
pergunta = "Qual é a capital da Nova Zelândia?"


# Gera o embedding da pergunta
embedding_pergunta = modelo.encode([pergunta])


# Compara a pergunta com todos os chunks
similaridades = cosine_similarity(
    embedding_pergunta,
    embeddings_chunks
)[0]


# Define quantos chunks queremos recuperar
top_k = 3


# Ordena os índices dos chunks pela similaridade
indices = similaridades.argsort()[::-1]


print("Pergunta:")
print(pergunta)


print("\n3 chunks mais relevantes:\n")

for posicao in range(top_k):

    indice = indices[posicao]

    print(f"--- Chunk {posicao + 1} ---")
    print("Similaridade:", similaridades[indice])
    print(chunks[indice]["chunk"])
    print()