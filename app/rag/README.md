# RAG

## Descrição

Nesta pasta contém os primeiros experimentos com os arquivos de rag_basico disponibilizados [nesse link](https://github.com/ricardoaraujo/ppgc_rag/blob/main/rag_basico.zip), onde, o objetivo era aprender a estrutura basica de um sistema de RAG.

Ainda assim essa pasta foi mantida, pois, os arquivos **populate_database.py** e **parser.py** ainda são utilizados para criar os embeddings e armazena-los no banco de dados. Além disso, é na pasta articles que foi criada a estrutura de organização dos artigos que serão parseados e inseridos no banco de dados.

## Funcionamento

### parser.py

Esse arquivo implementa o padrão de projeto chamado Strategy. Esse padrão é util pois nos permite trocar o algoritmo de execução através de uma interface em comum. Além disso, ele permite adicionar novas estratégias de extração de forma muito simples.

Abaixo um diagrama que ilustra o padrão Strategy no contexto desse arquivo.

![Strategy](./strategy.png)

### populate_database.py

Esse arquivo é o responsável por popular o banco de dados, e para isso, ele vai ler todos os arquivos html dentro da pasta articles e utilizando o nome da pasta irá instanciar a função de extração certa para cada arquivo.

Abaixo um diagrama que ilustra o processo de popular o banco de dados.

![Populate Database](./populatedb.png)