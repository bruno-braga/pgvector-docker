# pgvector + python

## What do you need to run this project?

- Docker
- A bunch of articles in html format
    - Articles should be in /rag/articles
        - currently you have 3 folders:
            - arxiv
            - ieeexplore
            - scientificdirect

The folders represent the databases each article should be placed in the proper folder so parser.py knows how to read them.

In order to download the html files we opt for an semi automated process. The file download_html.js contains a small script that downloads the html of a page for your.
With that you can:

Open an article(it has to be in one of the databases of the list)
Open your Browser's console(i.e Ctrl + Shift + J to open Chrome's console)
then copy and paste the js script mentioned

For instance if you go to https://ieeexplore.ieee.org/document/7465730 and do the steps above you will download the HTML file. 
After having the HTML file place it in the proper folder, in this case we should put into /rag/articles/ieeexplore


## How to run this

Firstly, clone the repo using the command below

```
git clone https://github.com/bruno-braga/pgvector-docker.git
cd pgvector-docker
cp .env.example .env
```

Don't forget to set the OPENAI_API_KEY environment variable in the .env file


After, inside the folder, do:

```
docker-compose up -d
```

After, the containers are up:

```
docker ps
```

Check the python container id and then:


```
docker exec -it <python_container_id> /bin/bash
cd /app/rag
python populate_database.py
```

(Don't forget to add the articles in the proper folder according ot is database (i.e /articles/scientificdirect))


## Folder structure & System "Architecture"

![System Architecture](./system.png)

```
├── app/
│   ├── rag/
│   │   ├── articles/
│   │   │   └── scientificdirect/
│   │   ├── api.py
│   │   ├── app.py  
│   │   ├── db.py
│   │   ├── parser.py
│   │   ├── populate_database.py
│   │   ├── populatedb.png
│   │   ├── prompt_template.yml
│   │   ├── prompt.py
│   │   ├── README.md
│   │   ├── strategy.png
│   │   └── strategy_png.png
│   └── src/
│       ├── .pytest_cache/
│       ├── database/
│       ├── Http/
│       ├── models/
│       ├── services/
│       │   ├── embedding_service.py
│       │   ├── prompt_service.py
│       │   └── prompt_template.yml
│       ├── static/
│       ├── tests/
│       ├── api.py
│       └── runner.py

```
the /rag folder is where the first experiments have happened. In there right now there are two files there that are being used, they are:

- populate_database.py
- parser.py

populate_database.py is responsible for reading the /articles folder and populate the database.
parser.py is responsible for ready the html files and extract the text from them.

/src is where the project itself lives, which is, a Flask app built with Vuejs for its frontend.

/database returns an db singleton
/Http is our controllers(Blueprints in Flask)
/models is where we have our models
/services is where we have our services
/static is where we have our static files
/api.py is our main entry point
/runner.py is our main runner

## RAG Pipeline

The diagram below illustrates the RAG pipeline as a sequence diagram.

![Strategy](./RAG_pipe.png)

