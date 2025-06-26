USE MensajeriaBD
Go

CREATE MASTER KEY ENCRYPTION BY PASSWORD ='1234ABCD'


CREATE CERTIFICATE Usuario_KEY_CERT
WITH SUBJECT = 'Certificado para las inserciones de Usuarios';

CREATE SYMMETRIC KEY Usuario_Key_01
WITH ALGORITHM = AES_256
ENCRYPTION BY CERTIFICATE Usuario_KEY_CERT;

GO

CREATE OR ALTER PROCEDURE sp_RegistrarUsuario (
    @param_Nombre NVARCHAR(100),
    @param_Apellido NVARCHAR(100),
    @param_Contrasenna NVARCHAR(100), 
    @param_Correo NVARCHAR(100),
    @param_NumeroTelefono NVARCHAR(100)
)
AS
BEGIN
    DECLARE @ContrasennaEncriptada VARBINARY(128);
    
    OPEN SYMMETRIC KEY Usuario_Key_01
    DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;

    
    SET @ContrasennaEncriptada = ENCRYPTBYKEY(KEY_GUID('Usuario_Key_01'), @param_Contrasenna);

    
    INSERT INTO Usuario (Nombre, Apellido, Contrasenna, Correo, NumeroTelefono)
    VALUES (@param_Nombre, @param_Apellido, @ContrasennaEncriptada, @param_Correo, @param_NumeroTelefono);

    
    CLOSE SYMMETRIC KEY Usuario_Key_01;

    PRINT 'Usuario registrado correctamente.';
END;
GO

EXEC sp_RegistrarUsuario
    @param_Nombre = 'Prueba',
    @param_Apellido = 'Dos',
    @param_Contrasenna = '1234',
    @param_Correo = 'prueba2@ucr',
    @param_NumeroTelefono = '12';

select * from Usuario;