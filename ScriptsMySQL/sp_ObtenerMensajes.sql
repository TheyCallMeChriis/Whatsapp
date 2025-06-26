USE mensajeriareplica

DELIMITER $$

CREATE PROCEDURE sp_ObtenerMensajes (
    IN p_EmisorID INT,
    IN p_ReceptorID INT
)
BEGIN
    
    SELECT 
        m.MensajeID,
        m.EmisorID,
        u.Nombre AS NombreEmisor,
        CAST(AES_DECRYPT(m.MensajeEncriptado, 'clave_secreta_123') AS CHAR(300)) AS MensajeTexto,
        m.ReceptorID,
        m.FechaEnvio
    FROM Mensaje m
    INNER JOIN Usuario u ON m.EmisorID = u.UsuarioID
    WHERE 
        (m.EmisorID = p_EmisorID AND m.ReceptorID = p_ReceptorID)
        OR 
        (m.EmisorID = p_ReceptorID AND m.ReceptorID = p_EmisorID)
    ORDER BY m.FechaEnvio ASC;
END$$

DELIMITER ;
