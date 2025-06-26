USE mensajeriareplica

DELIMITER $$

CREATE PROCEDURE sp_RecibirMensajes (
    IN p_ReceptorID INT
)
BEGIN
    
    SELECT 
        m.MensajeID,
        m.EmisorID,
        u.Nombre AS NombreEmisor,
        CAST(AES_DECRYPT(m.MensajeEncriptado, 'clave_secreta_123') AS CHAR(300)) AS MensajeTexto,
        m.ReceptorID
    FROM Mensaje m
    INNER JOIN Usuario u ON m.EmisorID = u.UsuarioID
    WHERE m.ReceptorID = p_ReceptorID;
END$$

DELIMITER ;
