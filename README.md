# 🇳🇿 RAG — Perguntas e Respostas sobre a Nova Zelândia

Projeto experimental de **Retrieval-Augmented Generation (RAG)** desenvolvido para compreender, na prática, as principais etapas de um sistema de recuperação e geração de respostas utilizando documentos próprios, embeddings, busca vetorial e um Large Language Model (LLM) executado localmente.

O projeto utiliza um pequeno conjunto de documentos sobre a **Nova Zelândia** como base de conhecimento.

---

## 📌 Sobre o projeto

O objetivo deste projeto é implementar um fluxo simples de RAG, permitindo observar separadamente as etapas de:

1. Carregamento dos documentos;
2. Divisão dos documentos em chunks;
3. Geração de embeddings;
4. Busca vetorial por similaridade;
5. Recuperação dos trechos mais relevantes;
6. Construção do contexto;
7. Geração da resposta utilizando um LLM.

O projeto foi desenvolvido principalmente para fins de **aprendizado e experimentação com RAG**, permitindo visualizar como a recuperação de informações influencia a resposta gerada por um modelo de linguagem.

---

## 🔎 O que é RAG?

**Retrieval-Augmented Generation (RAG)** é uma abordagem que combina a recuperação de informações com a geração de texto por um modelo de linguagem.

Em vez de enviar somente uma pergunta para o LLM, o sistema primeiro procura informações relevantes em uma base de conhecimento e utiliza esses trechos como contexto para gerar a resposta.

Neste projeto, o fluxo é:

```text
Documentos
    ↓
Chunking
    ↓
Embeddings
    ↓
Busca vetorial
    ↓
Chunks relevantes
    ↓
Contexto
    ↓
LLM
    ↓
Resposta
```

Dessa forma, o modelo não depende apenas do conhecimento utilizado durante seu treinamento, pois recebe informações recuperadas da base de documentos.

---

## 🗂️ Estrutura do projeto

```text
Dataset-RAG-NZ/
│
├── documentos.jsonl
├── perguntas.jsonl
│
├── 01_carregar_dados.py
├── 02_chunking.py
├── 03_embeddings.py
├── 04_busca_vetorial.py
├── 05_ollama.py
├── 06_rag.py
│
├── requirements.txt
└── README.md
```

### 📄 Arquivos de dados

#### `documentos.jsonl`

Contém os documentos utilizados como base de conhecimento.

Cada registro possui informações como:

```json
{
  "id": "doc_01",
  "title": "Geografia da Nova Zelândia",
  "text": "..."
}
```

A base contém **20 documentos** sobre diferentes aspectos da Nova Zelândia.

#### `perguntas.jsonl`

Contém **50 perguntas** relacionadas aos documentos da base.

Cada pergunta possui uma identificação e o documento correspondente utilizado como referência.

---

# 🧩 Etapas do projeto

## 1. Carregamento dos documentos

Arquivo:

```text
01_carregar_dados.py
```

Nesta etapa, os documentos armazenados no arquivo `documentos.jsonl` são carregados utilizando Python e a biblioteca `json`.

O primeiro teste confirmou que os **20 documentos** foram carregados corretamente.

```text
Quantidade de documentos: 20
```

---

## 2. Chunking

Arquivo:

```text
02_chunking.py
```

Os documentos são divididos em pequenos trechos chamados **chunks**.

Foi utilizado:

* **100 palavras por chunk**
* **20 palavras de overlap**

O overlap permite que parte do conteúdo de um chunk seja repetida no próximo.

Por exemplo:

```text
Chunk 1:
... informações sobre a Ilha Sul ... enquanto a

Chunk 2:
centro econômico e cultural. A Ilha Sul é conhecida ...
```

Essa sobreposição ajuda a reduzir a perda de contexto quando uma informação importante está próxima do limite entre dois chunks.

Com essa configuração, foram gerados:

```text
Quantidade de chunks: 36
```

---

## 3. Geração dos embeddings

Arquivo:

```text
03_embeddings.py
```

Cada chunk é transformado em um vetor numérico chamado **embedding**.

Para isso foi utilizado o modelo:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

Cada texto é representado por um vetor com:

```text
384 dimensões
```

O processo pode ser representado da seguinte forma:

```text
Texto
  ↓
Modelo de embeddings
  ↓
Vetor numérico
```

Esses vetores permitem comparar semanticamente os diferentes textos.

---

## 4. Busca vetorial

Arquivo:

```text
04_busca_vetorial.py
```

Quando uma pergunta é realizada, ela também é transformada em um embedding.

Depois disso, o embedding da pergunta é comparado com os embeddings dos chunks utilizando **similaridade de cosseno (cosine similarity)**.

O objetivo é encontrar os trechos semanticamente mais próximos da pergunta.

Neste projeto foram recuperados os **3 chunks mais relevantes (Top-K = 3)**.

Exemplo:

```text
Pergunta:
Qual é a capital da Nova Zelândia?

↓
Embedding da pergunta

↓
Comparação com os embeddings

↓
Top 3 chunks mais semelhantes
```

### ⚠️ Observação sobre a similaridade

O valor de similaridade não representa uma porcentagem de certeza.

Por exemplo:

```text
Similaridade: 0.67
```

não significa que o sistema possui **67% de certeza** de que a resposta está correta.

O valor representa apenas o grau de proximidade entre os vetores utilizado pela busca.

---

## 5. Teste do LLM

Arquivo:

```text
05_ollama.py
```

Antes de integrar o modelo ao RAG, foi realizado um teste separado com um LLM local.

Foi utilizado:

```text
Qwen 2.5 3B
```

executado através do **Ollama**.

Exemplo:

```text
Pergunta:
Qual é a capital da Nova Zelândia?

Resposta:
A capital da Nova Zelândia é Wellington.
```

Essa etapa permitiu verificar se o modelo estava funcionando corretamente antes de integrá-lo ao fluxo de RAG.

---

# 🤖 6. RAG completo

Arquivo:

```text
06_rag.py
```

Nesta etapa, todas as partes anteriores foram integradas.

O fluxo completo é:

```text
documentos.jsonl
       ↓
carregamento
       ↓
chunking
       ↓
embeddings
       ↓
embedding da pergunta
       ↓
similaridade de cosseno
       ↓
Top-3 chunks
       ↓
contexto recuperado
       ↓
Qwen 2.5 3B
       ↓
resposta
```

O contexto recuperado é inserido no prompt enviado ao modelo.

O modelo recebe a instrução para responder utilizando somente as informações fornecidas no contexto.

Exemplo:

```text
Responda à pergunta utilizando somente as informações
fornecidas no contexto abaixo.

Contexto:
[trechos recuperados]

Pergunta:
Qual é a capital da Nova Zelândia?
```

Resultado:

```text
Wellington é a capital da Nova Zelândia.
```

---

# 🛠️ Tecnologias utilizadas

| Tecnologia            | Utilização                               |
| --------------------- | ---------------------------------------- |
| Python                | Desenvolvimento do projeto               |
| JSONL                 | Armazenamento dos documentos e perguntas |
| Sentence Transformers | Geração dos embeddings                   |
| MiniLM                | Modelo utilizado para embeddings         |
| Scikit-learn          | Cálculo da similaridade de cosseno       |
| Ollama                | Execução local do LLM                    |
| Qwen 2.5 3B           | Modelo de linguagem                      |
| VS Code               | Ambiente de desenvolvimento              |
| Git/GitHub            | Versionamento e publicação               |

---

# 📦 Instalação

## 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

Depois:

```bash
cd Dataset-RAG-NZ
```

## 2. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

## 3. Instalar o Ollama

O projeto utiliza o Ollama para executar o modelo de linguagem localmente.

Depois de instalar o Ollama, faça o download do modelo:

```bash
ollama pull qwen2.5:3b
```

Para testar o modelo:

```bash
ollama run qwen2.5:3b
```

---

# ▶️ Executando o projeto

As etapas podem ser executadas individualmente para acompanhar o funcionamento do RAG.

### Carregar os documentos

```bash
python 01_carregar_dados.py
```

### Gerar os chunks

```bash
python 02_chunking.py
```

### Gerar os embeddings

```bash
python 03_embeddings.py
```

### Executar a busca vetorial

```bash
python 04_busca_vetorial.py
```

### Testar o LLM

```bash
python 05_ollama.py
```

### Executar o RAG completo

```bash
python 06_rag.py
```

---

# 🧪 Exemplo de execução

Pergunta utilizada:

```text
Qual é a capital da Nova Zelândia?
```

O sistema realiza:

```text
Pergunta
   ↓
Embedding
   ↓
Busca vetorial
   ↓
Top 3 chunks
   ↓
Contexto recuperado
   ↓
Qwen 2.5 3B
```

Resposta obtida:

```text
Wellington é a capital da Nova Zelândia.
```

---

# 🎯 Objetivos de aprendizagem

Este projeto foi desenvolvido para compreender, de forma prática:

* Como funciona um pipeline de RAG;
* O que são chunks;
* Como o overlap influencia a recuperação;
* O que são embeddings;
* Como textos podem ser representados por vetores;
* Como funciona uma busca por similaridade;
* O conceito de Top-K;
* Como o contexto recuperado é enviado para um LLM;
* Como utilizar um LLM local;
* A diferença entre uma consulta direta a um LLM e uma aplicação baseada em RAG.

---

# 🔬 Observações e experimentos

Durante o desenvolvimento, foram observados alguns comportamentos importantes.

### Chunking sem overlap

Quando os documentos foram inicialmente divididos em chunks sem sobreposição, algumas informações acabaram sendo separadas entre dois trechos.

Por exemplo, uma informação poderia terminar em:

```text
... direitos, soberania e uso
```

e o próximo chunk começar com:

```text
das terras.
```

Isso demonstrou, na prática, como a divisão dos documentos pode afetar a qualidade da recuperação.

### Chunking com overlap

Foi então utilizado um overlap de 20 palavras:

```text
Tamanho do chunk: 100 palavras
Overlap: 20 palavras
```

Com isso, parte do conteúdo de um chunk é mantida no seguinte, reduzindo a possibilidade de perder informações importantes nas fronteiras dos chunks.

---

# 📚 Próximos passos

Este projeto representa uma implementação inicial de RAG e pode ser expandido futuramente com:

* Avaliação automática da recuperação;
* Testes utilizando as 50 perguntas do dataset;
* Métricas como Recall@K e MRR;
* Comparação entre diferentes tamanhos de chunks;
* Comparação entre diferentes valores de overlap;
* Inclusão de metadados nos chunks;
* Uso de um banco de dados vetorial;
* Implementação de citações das fontes recuperadas;
* Avaliação de alucinações;
* Comparação entre diferentes modelos de embeddings;
* Comparação entre diferentes LLMs;
* Inclusão de uma etapa de validação das respostas.

---

# 📖 Conclusão

O projeto permitiu implementar um sistema RAG funcional utilizando uma base de documentos própria e um modelo de linguagem executado localmente.

A implementação mostrou, na prática, que o RAG não consiste apenas em utilizar um LLM. Existe uma etapa anterior de **recuperação de informações relevantes**, responsável por selecionar os trechos que serão utilizados como contexto para a geração da resposta.

O experimento também permitiu observar como decisões aparentemente simples, como o **tamanho dos chunks e o uso de overlap**, podem influenciar o processo de recuperação.

O projeto permanece como uma base experimental para estudos posteriores sobre **RAG, recuperação de informação, embeddings, LLMs e avaliação de respostas geradas por inteligência artificial**.
