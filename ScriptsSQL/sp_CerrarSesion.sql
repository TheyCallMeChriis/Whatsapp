use MensajeriaBD;
go

select * from Usuario;
go 

select * from Sesion;
go

CREATE OR ALTER PROCEDURE sp_CerrarSesion (
    @param_UsuarioID INT
)
AS
BEGIN
    BEGIN TRY
        -- Verificar si existe una sesi�n activa para el usuario
        IF NOT EXISTS (
            SELECT 1 FROM Sesion WHERE UsuarioID = @param_UsuarioID AND Activa = 1
        )
        BEGIN
            RAISERROR('No hay una sesi�n activa para este usuario.', 16, 1);
            RETURN;
        END

        -- Eliminar el registro de la sesi�n activa
        DELETE FROM Sesion
        WHERE UsuarioID = @param_UsuarioID AND Activa = 1;

        PRINT 'Sesi�n cerrada correctamente.';
    END TRY
    BEGIN CATCH
        DECLARE @ErrMsg NVARCHAR(4000), @ErrSeverity INT;
        SELECT @ErrMsg = ERROR_MESSAGE(), @ErrSeverity = ERROR_SEVERITY();
        RAISERROR(@ErrMsg, @ErrSeverity, 1);
    END CATCH
END;
GO


EXEC sp_CerrarSesion
    @param_UsuarioID = '2004';
