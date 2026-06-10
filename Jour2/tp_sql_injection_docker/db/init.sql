DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(30)
);

INSERT INTO users(username, password_hash, email, role) VALUES
('admin', '$2b$12$rK6E8nhDTycLJzV3P7zW7.dQzNUX.Jk8VDj9A56HuikMpwLIz2AW6', 'admin@entreprise.com', 'ADMIN'),
('yassine', '$2b$12$V37wqDBwBR55CLY4/lKeTewdTDG2E0TO13ylt01xAWC8JcO1dfn7y', 'yassine@mail.com', 'USER'),
('user1', '$2b$12$nqkkYaJ9k4nCXtZ71Q8oeucHL/mqky/fACi3LxjTWGk8WVnRoAAuS', 'user1@mail.com', 'USER');