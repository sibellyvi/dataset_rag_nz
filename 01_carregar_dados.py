import json


# Abre o arquivo de documentos e transforma
# cada linha JSON em um objeto Python.
with open("documentos.jsonl", "r", encoding="utf-8") as arquivo:

    documentos = []

    for linha in arquivo:
        documentos.append(json.loads(linha))


print("Quantidade de documentos:", len(documentos))


# Mostra o primeiro documento para verificarmos
# se os dados foram carregados corretamente.
print("\nPrimeiro documento:")
print(documentos[0])