USE MensajeriaBD
Go

CREATE OR ALTER PROCEDURE sp_EnviarMensaje (
    @param_EmisorID INT,
    @param_ReceptorID INT,
    @param_MensajeTexto NVARCHAR(300) 
)
AS
BEGIN
    DECLARE @MensajeEncriptado VARBINARY(128);

    OPEN SYMMETRIC KEY Usuario_Key_01
    DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;

  
    SET @MensajeEncriptado = ENCRYPTBYKEY(KEY_GUID('Usuario_Key_01'), @param_MensajeTexto);

    
    INSERT INTO Mensaje (EmisorID, ReceptorID, MensajeEncriptado)
    VALUES (@param_EmisorID, @param_ReceptorID, @MensajeEncriptado);

    
    CLOSE SYMMETRIC KEY Usuario_Key_01;

    PRINT 'Mensaje enviado correctamente.';
END;


EXEC sp_EnviarMensaje
    @param_EmisorID = 1,
    @param_ReceptorID = 3,
    @param_MensajeTexto = 'Hola, �c�mo est�s?';

SELECT * FROM [dbo].[Mensaje]


OPEN SYMMETRIC KEY Usuario_Key_01
DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;

SELECT 
    MensajeID,
    EmisorID,
    ReceptorID,
    CAST(DecryptByKey(MensajeEncriptado) AS NVARCHAR(MAX)) AS MensajeTexto
FROM Mensaje;


CLOSE SYMMETRIC KEY Usuario_Key_01;