USE IF5100_Proyecto
Go

CREATE OR ALTER PROCEDURE sp_CerrarSesion (
    @param_Token NVARCHAR(255)
)
AS
BEGIN
    -- Verifica si hay una sesión activa con ese token y la cierra
    UPDATE Sesion
    SET 
        FechaFin = GETDATE(),
        Activa = 0
    WHERE 
        Token = @param_Token
        AND Activa = 1
        AND FechaFin IS NULL;

    -- Verifica si alguna fila fue afectada
    IF @@ROWCOUNT = 0
    BEGIN
        PRINT 'Sesión no encontrada, ya cerrada o token inválido.';
    END
    ELSE
    BEGIN
        PRINT 'Sesión cerrada exitosamente.';
    END
END;
