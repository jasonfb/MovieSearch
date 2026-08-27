CREATE DATABASE moviesearch;

\c moviesearch

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    plt TEXT NOT NULL,
    embedding vector(384)
)