USE MensajeriaBD
Go

CREATE OR ALTER PROCEDURE sp_EnviarMensaje (
    @param_EmisorID INT,
    @param_ReceptorID INT,
    @param_MensajeTexto NVARCHAR(300) -- mensaje en texto plano
)
AS
BEGIN
    DECLARE @MensajeEncriptado VARBINARY(128);

    -- Abrir la llave simétrica para encriptar el mensaje
    OPEN SYMMETRIC KEY Usuario_Key_01
    DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;

    -- Encriptar el mensaje
    SET @MensajeEncriptado = ENCRYPTBYKEY(KEY_GUID('Usuario_Key_01'), @param_MensajeTexto);

    -- Insertar el mensaje en la tabla
    INSERT INTO Mensaje (EmisorID, ReceptorID, MensajeEncriptado)
    VALUES (@param_EmisorID, @param_ReceptorID, @MensajeEncriptado);

    -- Cerrar la llave
    CLOSE SYMMETRIC KEY Usuario_Key_01;

    PRINT 'Mensaje enviado correctamente.';
END;


EXEC sp_EnviarMensaje
    @param_EmisorID = 1,
    @param_ReceptorID = 3,
    @param_MensajeTexto = 'Hola, ¿cómo estás?';

SELECT * FROM [dbo].[Mensaje]

-- Abrir llave
OPEN SYMMETRIC KEY Usuario_Key_01
DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;

-- Ver mensajes desencriptados
SELECT 
    MensajeID,
    EmisorID,
    ReceptorID,
    CAST(DecryptByKey(MensajeEncriptado) AS NVARCHAR(MAX)) AS MensajeTexto
FROM Mensaje;

-- Cerrar llave
CLOSE SYMMETRIC KEY Usuario_Key_01;