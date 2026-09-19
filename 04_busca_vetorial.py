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


# Descobre qual chunk teve a maior similaridade
indice_melhor_chunk = similaridades.argmax()


print("Pergunta:")
print(pergunta)

print("\nChunk mais parecido:")
print(chunks[indice_melhor_chunk]["chunk"])

print("\nSimilaridade:")
print(similaridades[indice_melhor_chunk])