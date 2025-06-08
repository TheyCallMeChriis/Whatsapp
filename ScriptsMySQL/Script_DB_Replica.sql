CREATE DATABASE MensajeriaReplica;
USE MensajeriaReplica;

CREATE TABLE Usuario (
    UsuarioID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Contrasenna VARBINARY(128) NOT NULL,
    Correo VARCHAR(100) NOT NULL UNIQUE,
    Estado BOOLEAN DEFAULT 0, -- 0 = activo, 1 = eliminado
    NumeroTelefono VARCHAR(100) NOT NULL UNIQUE,
    Actualizado DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Mensaje (
    MensajeID INT PRIMARY KEY AUTO_INCREMENT,
    EmisorID INT NOT NULL,
    ReceptorID INT NOT NULL,
    MensajeEncriptado VARBINARY(128) NOT NULL,
    FechaEnvio DATETIME DEFAULT CURRENT_TIMESTAMP,
    Actualizado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EmisorID) REFERENCES Usuario(UsuarioID),
    FOREIGN KEY (ReceptorID) REFERENCES Usuario(UsuarioID)
);

CREATE TABLE Sesion (
    SesionID INT PRIMARY KEY AUTO_INCREMENT,
    UsuarioID INT NOT NULL,
    Token VARCHAR(255) NOT NULL UNIQUE,
    FechaInicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FechaFin DATETIME NULL,
    Activa BOOLEAN DEFAULT 1,
    FOREIGN KEY (UsuarioID) REFERENCES Usuario(UsuarioID)
);

select * from usuario;
select * from mensaje;
