

CREATE DATABASE  security_vault

USE "security_vault" 

CREATE TABLE IF NOT EXISTS system_access (
    id INT PRIMARY KEY,
    access_name VARCHAR(50),
    password_hash VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(50)
);

INSERT INTO system_access (id, access_name, password_hash) 
VALUES (1, 'Admin_Access', '$argon2id$v=19$m=65536,t=3,p=4$ARnhHOlRsjpAzJaWcPcYNw$QRolFHmr2B3o0de+Zb84MTO5Aycu8AhGpEqeQb5z23E');




