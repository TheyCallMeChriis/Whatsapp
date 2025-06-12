USE MensajeriaBD;
GO

CREATE OR ALTER PROCEDURE sp_ObtenerMensajes (
    @param_EmisorID INT,
    @param_ReceptorID INT
)
AS
BEGIN
    SET NOCOUNT ON;

    -- Abrir la llave sim�trica si a�n no est� abierta
    IF NOT EXISTS (
        SELECT * FROM sys.openkeys WHERE key_name = 'Usuario_Key_01'
    )
    BEGIN
        OPEN SYMMETRIC KEY Usuario_Key_01
        DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;
    END

    -- Obtener mensajes desencriptados entre el emisor y receptor
    SELECT 
        m.MensajeID,
        m.EmisorID,
        u.Nombre AS NombreEmisor,
        CAST(DECRYPTBYKEY(m.MensajeEncriptado) AS NVARCHAR(MAX)) AS MensajeTexto,
        m.ReceptorID,
        m.FechaEnvio
    FROM Mensaje m
    INNER JOIN Usuario u ON m.EmisorID = u.UsuarioID
    WHERE (m.EmisorID = @param_EmisorID AND m.ReceptorID = @param_ReceptorID)
       OR (m.EmisorID = @param_ReceptorID AND m.ReceptorID = @param_EmisorID)
    ORDER BY m.FechaEnvio ASC;

    -- Cerrar la llave despu�s de usarla
    CLOSE SYMMETRIC KEY Usuario_Key_01;
END;
GO


EXEC sp_ObtenerMensajes @param_EmisorID = 4, @param_ReceptorID = 3;
