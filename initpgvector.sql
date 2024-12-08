CREATE EXTENSION vector;

CREATE TABLE items (
    id bigserial PRIMARY KEY,
    text text,
    article_title text,
    embedding vector
);