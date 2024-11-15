CREATE EXTENSION vector;

CREATE TABLE items (
    id bigserial PRIMARY KEY,
    text text,
    embedding vector
);

INSERT INTO items (text, embedding) VALUES ('Hello', '[1,2,3]'), ('World', '[4,5,6]');

SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

