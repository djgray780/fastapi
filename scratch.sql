-- @conn fastapi_db
CREATE TABLE IF NOT EXISTS posts (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER,
    title VARCHAR (255) NOT NULL,
    content VARCHAR (255) NOT NULL,
    published BOOLEAN DEFAULT True NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT posts_users_fkey FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE NO ACTION
);
-- @block alter posts to add foreign key constraint for users
DROP TABLE posts;
INSERT INTO posts (id, user_id, title, content)
VALUES (2, 3, 'My Post', 'My Contents') -- @block delete from posts
DELETE FROM posts;
-- @block insert into posts
INSERT INTO posts (id, user_id, title, content)
VALUES (7, 15, 'My Post3', 'My Contents4')