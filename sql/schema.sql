CREATE TABLE repositories (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    language VARCHAR(100),
    stars INTEGER,
    forks INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);