
USE mensajeriareplica;

DELIMITER $$

CREATE PROCEDURE sp_CerrarSesion (
    IN p_Token VARCHAR(255)
)
BEGIN
    DECLARE filas_afectadas INT;

    UPDATE Sesion
    SET 
        FechaFin = NOW(),
        Activa = 0
    WHERE 
        Token = p_Token
        AND Activa = 1
        AND FechaFin IS NULL;

 
    SET filas_afectadas = ROW_COUNT();

    IF filas_afectadas = 0 THEN
        SELECT 'Sesión no encontrada, ya cerrada o token inválido.' AS Mensaje;
    ELSE
        SELECT 'Sesión cerrada exitosamente.' AS Mensaje;
    END IF;
END$$

DELIMITER ;
