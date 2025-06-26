USE mensajeriareplica

DELIMITER $$

CREATE PROCEDURE sp_EnviarMensaje (
    IN p_EmisorID INT,
    IN p_ReceptorID INT,
    IN p_MensajeTexto VARCHAR(300)
)
BEGIN
    DECLARE mensaje_encriptado BLOB;

    SET mensaje_encriptado = AES_ENCRYPT(p_MensajeTexto, 'clave_secreta_123');

  
    INSERT INTO Mensaje (EmisorID, ReceptorID, MensajeEncriptado)
    VALUES (p_EmisorID, p_ReceptorID, mensaje_encriptado);

    SELECT 'Mensaje enviado correctamente.' AS Mensaje;
END$$

DELIMITER ;


