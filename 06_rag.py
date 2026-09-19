import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ollama import chat


# =========================
# 1. CARREGAR DOCUMENTOS
# =========================

with open("documentos.jsonl", "r", encoding="utf-8") as arquivo:
    documentos = []

    for linha in arquivo:
        documentos.append(json.loads(linha))


# =========================
# 2. CRIAR CHUNKS
# =========================

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

        inicio += tamanho_chunk - overlap


# =========================
# 3. GERAR EMBEDDINGS
# =========================

modelo = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

textos = [chunk["chunk"] for chunk in chunks]

embeddings_chunks = modelo.encode(textos)


# =========================
# 4. PERGUNTA
# =========================

pergunta = "Em qual continente fica a Nova Zelândia?"

embedding_pergunta = modelo.encode([pergunta])


# =========================
# 5. BUSCA DOS CHUNKS
# =========================

similaridades = cosine_similarity(
    embedding_pergunta,
    embeddings_chunks
)[0]

top_k = 3

indices = similaridades.argsort()[::-1][:top_k]


# =========================
# 6. CRIAR O CONTEXTO
# =========================

contexto = ""

for indice in indices:

    contexto += chunks[indice]["chunk"]
    contexto += "\n\n"


# =========================
# 7. ENVIAR CONTEXTO AO LLM
# =========================

prompt = f"""
Responda à pergunta utilizando somente as informações
fornecidas no contexto abaixo.

Contexto:
{contexto}

Pergunta:
{pergunta}
"""


resposta = chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# =========================
# 8. MOSTRAR RESULTADO
# =========================

print("Pergunta:")
print(pergunta)

print("\nResposta do RAG:")
print(resposta.message.content)