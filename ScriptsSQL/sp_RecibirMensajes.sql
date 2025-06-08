USE MensajeriaBD
GO

CREATE OR ALTER PROCEDURE sp_RecibirMensajes (
    @param_ReceptorID INT
)
AS
BEGIN
    -- Abrir la llave simétrica para desencriptar
    OPEN SYMMETRIC KEY Usuario_Key_01
    DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;

    -- Consultar mensajes desencriptados
    SELECT 
        m.MensajeID,
        m.EmisorID,
        u.Nombre AS NombreEmisor,
        CAST(DECRYPTBYKEY(m.MensajeEncriptado) AS NVARCHAR(MAX)) AS MensajeTexto,
        m.ReceptorID
    FROM Mensaje m
    INNER JOIN Usuario u ON m.EmisorID = u.UsuarioID
    WHERE m.ReceptorID = @param_ReceptorID;

    -- Cerrar la llave
    CLOSE SYMMETRIC KEY Usuario_Key_01;
END;

EXEC sp_RecibirMensajes @param_ReceptorID = 1;


