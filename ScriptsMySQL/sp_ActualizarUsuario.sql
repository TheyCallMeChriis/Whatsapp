USE mensajeriareplica
DELIMITER $$

CREATE PROCEDURE sp_ActualizarUsuario (
    IN p_UsuarioID INT,
    IN p_NuevoNombre VARCHAR(100),
    IN p_NuevoApellido VARCHAR(100),
    IN p_NuevoCorreo VARCHAR(100),
    IN p_NuevoNumeroTelefono VARCHAR(100)
)
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Usuario WHERE UsuarioID = p_UsuarioID AND Estado = 0
    ) THEN
        SELECT 'Usuario no encontrado o está eliminado.' AS Mensaje;
    ELSE
        UPDATE Usuario
        SET 
            Nombre = p_NuevoNombre,
            Apellido = p_NuevoApellido,
            Correo = p_NuevoCorreo,
            NumeroTelefono = p_NuevoNumeroTelefono
        WHERE UsuarioID = p_UsuarioID;

        SELECT 'Datos del usuario actualizados correctamente.' AS Mensaje;
    END IF;
END$$

DELIMITER ;

