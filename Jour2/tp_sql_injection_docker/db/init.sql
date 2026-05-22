DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(30)
);

INSERT INTO users(username, password, email, role) VALUES
('admin', 'admin123', 'admin@entreprise.com', 'ADMIN'),
('yassine', 'test123', 'yassine@mail.com', 'USER'),
('user1', 'password', 'user1@mail.com', 'USER');
