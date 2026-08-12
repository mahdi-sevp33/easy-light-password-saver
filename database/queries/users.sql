

CREATE DATABASE  security_vault

USE "security_vault" 

CREATE TABLE system_access (
    id INT PRIMARY KEY,
    access_name VARCHAR(50),
    password_hash VARCHAR(255)
);

CREATE TABLE users(
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(50)
);

