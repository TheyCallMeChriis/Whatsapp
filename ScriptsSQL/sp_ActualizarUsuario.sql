USE MensajeriaBD
GO
CREATE OR ALTER PROCEDURE sp_ActualizarUsuario (
    @UsuarioID INT,
    @NuevoNombre NVARCHAR(100),
    @NuevoApellido NVARCHAR(100),
    @NuevoCorreo NVARCHAR(100),
    @NuevoNumeroTelefono NVARCHAR(100)
)
AS
BEGIN
    -- Verifica si el usuario existe y está activo
    IF NOT EXISTS (
        SELECT 1 FROM Usuario
        WHERE UsuarioID = @UsuarioID AND Estado = 0
    )
    BEGIN
        PRINT 'Usuario no encontrado o está eliminado.';
        RETURN;
    END

    -- Realiza la actualización
    UPDATE Usuario
    SET 
        Nombre = @NuevoNombre,
        Apellido = @NuevoApellido,
        Correo = @NuevoCorreo,
        NumeroTelefono = @NuevoNumeroTelefono
    WHERE UsuarioID = @UsuarioID;

    PRINT 'Datos del usuario actualizados correctamente.';
END;

EXEC sp_ActualizarUsuario 
    @UsuarioID = 1,
    @NuevoNombre = 'Chris',
    @NuevoApellido = 'Leon',
    @NuevoCorreo = 'chris@ucr',
    @NuevoNumeroTelefono = '63056255';

select * from usuario;