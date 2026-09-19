from sentence_transformers import SentenceTransformer


# Carrega o modelo que transforma texto em vetores
modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


texto = "A Nova Zelândia é um país insular localizado no Oceano Pacífico."


# Transforma o texto em um vetor
embedding = modelo.encode(texto)


print("Texto:")
print(texto)

print("\nEmbedding:")
print(embedding)

print("\nQuantidade de números no vetor:")
print(len(embedding))