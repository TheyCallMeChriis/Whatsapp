USE MensajeriaBD;
GO

CREATE OR ALTER PROCEDURE sp_ObtenerUsuarios
AS
BEGIN
    SELECT UsuarioID, Nombre, Apellido
    FROM Usuario;
END;
GO
