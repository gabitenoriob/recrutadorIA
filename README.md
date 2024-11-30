# Analisador de Currículos com Similaridade e Avaliação de Qualidade

Este projeto é um sistema desenvolvido em Python usando Flask, spaCy e a biblioteca Sentence-Transformers para análise de currículos. Ele permite fazer o upload de arquivos PDF de currículos, extrair seu conteúdo, calcular a similaridade com uma descrição de vaga e avaliar a qualidade do currículo com base em critérios pré-definidos.

## Funcionalidades

- **Upload de arquivos PDF**: Permite o upload de currículos em formato PDF.
- **Extração de texto**: Extrai o texto dos arquivos PDF utilizando a biblioteca `fitz` (PyMuPDF).
- **Processamento de texto**: Usa o modelo `spaCy` para processar o texto dos currículos e extrair informações como qualificações, experiência, empresa, educação e habilidades.
- **Cálculo de similaridade**: Compara o currículo com uma descrição de vaga usando o modelo `SentenceTransformer` e calcula a similaridade com base nos embeddings de cada texto.
- **Avaliação de currículo**: Classifica o currículo com base na pontuação de similaridade: "Aprovado", "Aprovado Parcialmente" ou "Reprovado".
- **API Flask**: Exposição de endpoints para upload de arquivos e consulta dos resultados da análise.

## Tecnologias Usadas

- **Flask**: Framework web para criar a API e renderizar o front-end.
- **spaCy**: Biblioteca de processamento de linguagem natural (NLP) para extrair entidades do texto.
- **Sentence-Transformers**: Para gerar embeddings e calcular similaridade entre textos.
- **fitz (PyMuPDF)**: Para extrair texto de arquivos PDF.

## Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina. Você também precisará instalar as seguintes bibliotecas:

- Flask
- spaCy
- Sentence-Transformers
- fitz (PyMuPDF)
- scikit-learn

### Instalar as dependências

Execute o comando abaixo para instalar as dependências necessárias:

```bash
pip install flask spacy sentence-transformers pymupdf scikit-learn
```

Além disso, você precisará baixar o modelo do spaCy 

```bash
python -m spacy download en_core_web_sm
```
### Como Usar
Inicie o servidor Flask:

Para rodar o servidor, execute o seguinte comando:

```bash
python app.py
```

Acesse o aplicativo:
O aplicativo estará disponível em http://127.0.0.1:5000/. Você pode acessar a página inicial e enviar currículos em formato PDF através do formulário.

### Observações
A base de dados que usei está em ingles e os cúrriculos são na área de TI, logo há uma descrição de vaga FIXA usada para comparar a similaridade dentro do contexto dessa base de dados. 