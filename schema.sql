CREATE DATABASE moviesearch;

\c moviesearch

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    plot TEXT NOT NULL,
    embedding vector(384)
);

CREATE INDEX movies_embedding_hnsw_idx 
ON movies 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);