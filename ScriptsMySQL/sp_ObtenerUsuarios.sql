USE mensajeriareplica

DELIMITER $$

CREATE PROCEDURE sp_ObtenerUsuarios()
BEGIN
    SELECT UsuarioID, Nombre, Apellido
    FROM Usuario;
END$$

DELIMITER ;
