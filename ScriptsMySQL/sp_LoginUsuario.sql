USE mensajeriareplica;

DELIMITER $$

CREATE PROCEDURE sp_LoginUsuario (
    IN p_Identificador VARCHAR(100), 
    IN p_Contrasenna VARCHAR(100)    
)
BEGIN
    DECLARE v_UsuarioID INT;
    DECLARE v_ContrasennaEnBD BLOB;
    DECLARE v_ContrasennaDesencriptada VARCHAR(100);
    DECLARE v_TokenSesion VARCHAR(255);


    SELECT UsuarioID, Contrasenna
    INTO v_UsuarioID, v_ContrasennaEnBD
    FROM Usuario
    WHERE Estado = 0
    AND (Correo = p_Identificador OR NumeroTelefono = p_Identificador)
    LIMIT 1;

    
    IF v_UsuarioID IS NULL THEN
        SELECT 'ERROR' AS Estado, 'Usuario no encontrado o inactivo' AS Mensaje;
        LEAVE sp_LoginUsuario;
    END IF;

    
    SET v_ContrasennaDesencriptada = CAST(AES_DECRYPT(v_ContrasennaEnBD, 'clave_secreta_123') AS CHAR(100));

   
    IF p_Contrasenna <> v_ContrasennaDesencriptada THEN
        SELECT 'ERROR' AS Estado, 'Contraseña incorrecta' AS Mensaje;
        LEAVE sp_LoginUsuario;
    END IF;

    
    SET v_TokenSesion = UUID();

    
    INSERT INTO Sesion (UsuarioID, Token)
    VALUES (v_UsuarioID, v_TokenSesion);

    
    SELECT 'OK' AS Estado, 'Inicio de sesión exitoso' AS Mensaje, v_UsuarioID AS UsuarioID, v_TokenSesion AS Token;
END$$

DELIMITER ;
