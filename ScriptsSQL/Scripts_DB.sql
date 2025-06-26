CREATE DATABASE MensajeriaBD;
GO
USE MensajeriaBD;

-- Tabla Usuario
CREATE TABLE Usuario (
    UsuarioID INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(100) NOT NULL,
    Apellido NVARCHAR(100) NOT NULL,
    Contrasenna VARBINARY(128) NOT NULL,
    Correo NVARCHAR(100) NOT NULL UNIQUE,
    Estado BIT DEFAULT 0, -- 0 = activo, 1 = eliminado
    NumeroTelefono NVARCHAR(100) NOT NULL UNIQUE,
    Actualizado DATETIME DEFAULT GETDATE()
);
GO

-- Tabla Mensaje
CREATE TABLE Mensaje (
    MensajeID INT PRIMARY KEY IDENTITY(1,1),
    EmisorID INT NOT NULL,
    ReceptorID INT NOT NULL,
    MensajeEncriptado VARBINARY(128) NOT NULL,
    FechaEnvio DATETIME DEFAULT GETDATE(),
    Actualizado DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (EmisorID) REFERENCES Usuario(UsuarioID),
    FOREIGN KEY (ReceptorID) REFERENCES Usuario(UsuarioID)
);
GO

-- Tabla Sesion
CREATE TABLE Sesion (
    SesionID INT PRIMARY KEY IDENTITY(1,1),
    UsuarioID INT NOT NULL,
    Token NVARCHAR(255) NOT NULL UNIQUE,
    FechaInicio DATETIME DEFAULT GETDATE(),
    FechaFin DATETIME NULL,
    Activa BIT DEFAULT 1,
    FOREIGN KEY (UsuarioID) REFERENCES Usuario(UsuarioID)
);
GO


INSERT INTO Usuario (Nombre, Apellido, Contrasenna, Correo, NumeroTelefono)
VALUES
('Ana', 'Gómez', CONVERT(VARBINARY(128), 'clave123'), 'ana@example.com', '88881111'),
('Luis', 'Ramírez', CONVERT(VARBINARY(128), 'secreto456'), 'luis@example.com', '88882222'),
('Maria', 'López', CONVERT(VARBINARY(128), 'pass789'), 'maria@example.com', '88883333');


INSERT INTO Mensaje (EmisorID, ReceptorID, MensajeEncriptado)
VALUES
(1, 2, CONVERT(VARBINARY(128), 'Hola Luis!')),
(2, 1, CONVERT(VARBINARY(128), 'Hola Ana! ¿Cómo estás?')),
(3, 1, CONVERT(VARBINARY(128), 'Buen día Ana, soy María.')),
(1, 3, CONVERT(VARBINARY(128), 'Hola María, gusto en saludarte.'));

SELECT * FROM Usuario;
SELECT * FROM Mensaje;