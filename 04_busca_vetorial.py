import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


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


# Carrega o modelo
modelo = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)


# Gera os embeddings dos chunks
textos = [chunk["chunk"] for chunk in chunks]

embeddings_chunks = modelo.encode(textos)


# Pergunta
pergunta = "Em qual continente fica a Nova Zelândia?"


# Gera o embedding da pergunta
embedding_pergunta = modelo.encode([pergunta])


# Calcula a similaridade
similaridades = cosine_similarity(
    embedding_pergunta,
    embeddings_chunks
)[0]


# Recupera os 3 chunks mais relevantes
top_k = 3

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