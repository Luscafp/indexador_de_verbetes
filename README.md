Este projeto é útil para quem precisa realizar buscas eficientes em grandes volumes de dados textuais, como verbetes de enciclopédias ou documentos similares. Foi um trabalho feito para disciplina de Hipérmidia na curso de Ciência da Computação da UFMA.

Este repositório contém dois scripts Python (`buscador.py` e `indexador.py`) que trabalham juntos para indexar e pesquisar conteúdo em um arquivo XML contendo verbetes da Wikipedia. Abaixo está uma breve explicação de cada parte do projeto:

### `indexador.py`
- **Função `indexar(arquivo)`**: Esta função lê um arquivo XML (`verbetesWikipedia.xml`) e cria um índice invertido. O índice invertido mapeia palavras (com pelo menos 4 caracteres) para os IDs dos documentos onde elas aparecem, tanto no título quanto no texto. Além disso, a função também armazena os dados completos de cada página (ID, título e texto) em um dicionário chamado `pages`.
- **Função `search(title, index, pages)`**: Esta função realiza uma pesquisa no índice invertido criado pela função `indexar`. Ela retorna os documentos que contêm a palavra pesquisada, juntamente com a relevância de cada documento. A relevância é calculada com base na frequência da palavra no texto e no título (palavras no título têm peso maior).

### `buscador.py`
- **Função `indexador(arquivo)`**: Similar à função `indexar` do `indexador.py`, esta função também cria um índice invertido e armazena os dados das páginas.
- **Função `pesquisa(title, index, pages)`**: Esta função realiza a pesquisa no índice invertido, similar à função `search` do `indexador.py`. Ela retorna os documentos relevantes ordenados por relevância.

### Como usar
1. **Indexação**: Execute o script `indexador.py` para criar o índice invertido e armazenar os dados das páginas.
2. **Pesquisa**: Execute o script `buscador.py` para pesquisar por uma palavra ou termo. O script retornará os documentos relevantes, ordenados por relevância, exibindo o ID, a relevância, as informações de frequência e o título de cada documento.

### Exemplo de uso
```bash
python indexador.py
python buscador.py
```
Quando solicitado, insira o termo que deseja pesquisar, por exemplo, "power". O programa retornará os documentos relevantes com base na relevância calculada.

### Requisitos
- Python 3.x
- Arquivo XML (`verbetesWikipedia.xml`) contendo os dados dos verbetes da Wikipedia.

