CREATE TABLE repositories (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    language VARCHAR(100),
    stars INTEGER NOT NULL,
    forks INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    last_activity_days INTEGER NOT NULL,
    popularity VARCHAR(50) NOT NULL
);