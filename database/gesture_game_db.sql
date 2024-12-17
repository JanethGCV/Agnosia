CREATE DATABASE gesture_game_db;
USE gesture_game_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL  -- Para hash SHA-256
);

CREATE TABLE partidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    puntuacion INT,
    fecha DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);