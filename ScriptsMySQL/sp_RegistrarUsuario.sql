USE mensajeriareplica

DELIMITER $$

CREATE PROCEDURE sp_RegistrarUsuario (
    IN p_Nombre VARCHAR(100),
    IN p_Apellido VARCHAR(100),
    IN p_Contrasenna VARCHAR(100), 
    IN p_Correo VARCHAR(100),
    IN p_NumeroTelefono VARCHAR(100)
)
BEGIN
    DECLARE v_ContrasennaEncriptada BLOB;

    
    SET v_ContrasennaEncriptada = AES_ENCRYPT(p_Contrasenna, 'clave_secreta_123');

    
    INSERT INTO Usuario (Nombre, Apellido, Contrasenna, Correo, NumeroTelefono)
    VALUES (p_Nombre, p_Apellido, v_ContrasennaEncriptada, p_Correo, p_NumeroTelefono);

    
    SELECT 'Usuario registrado correctamente.' AS Mensaje;
END$$

DELIMITER ;
