USE MensajeriaBD
Go

CREATE MASTER KEY ENCRYPTION BY PASSWORD ='1234ABCD'

-- Creacion del Certificado
CREATE CERTIFICATE Usuario_KEY_CERT
WITH SUBJECT = 'Certificado para las inserciones de Usuarios';

CREATE SYMMETRIC KEY Usuario_Key_01
WITH ALGORITHM = AES_256
ENCRYPTION BY CERTIFICATE Usuario_KEY_CERT;

CREATE OR ALTER PROCEDURE sp_RegistrarUsuario (
    @param_Nombre NVARCHAR(100),
    @param_Apellido NVARCHAR(100),
    @param_Contrasenna NVARCHAR(100), -- Contraseña en texto plano
    @param_Correo NVARCHAR(100),
    @param_NumeroTelefono NVARCHAR(100)
)
AS
BEGIN
    DECLARE @ContrasennaEncriptada VARBINARY(128);
    -- Abrir la llave simétrica para encriptar la contraseña
    OPEN SYMMETRIC KEY Usuario_Key_01
    DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;

    -- Encriptar la contraseña
    SET @ContrasennaEncriptada = ENCRYPTBYKEY(KEY_GUID('Usuario_Key_01'), @param_Contrasenna);

    -- Insertar el nuevo usuario
    INSERT INTO Usuario (Nombre, Apellido, Contrasenna, Correo, NumeroTelefono)
    VALUES (@param_Nombre, @param_Apellido, @ContrasennaEncriptada, @param_Correo, @param_NumeroTelefono);

    -- Cerrar la llave simétrica
    CLOSE SYMMETRIC KEY Usuario_Key_01;

    PRINT 'Usuario registrado correctamente.';
END;

EXEC sp_RegistrarUsuario
    @param_Nombre = 'Joselito',
    @param_Apellido = 'Arias',
    @param_Contrasenna = 'Pepe2544',
    @param_Correo = 'joselito@ucr',
    @param_NumeroTelefono = '63056255';

select * from Usuario;