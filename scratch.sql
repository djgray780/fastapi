CREATE TABLE IF NOT EXISTS posts (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR (255) NOT NULL,
    content VARCHAR (255) NOT NULL,
    published BOOLEAN DEFAULT True NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO posts(title, content)
VALUES ('first post', 'some stuff');