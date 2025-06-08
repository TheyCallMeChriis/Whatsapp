use MensajeriaBD
go

CREATE OR ALTER PROCEDURE sp_LoginUsuario (
    @param_Identificador NVARCHAR(100), -- Correo o número de teléfono
    @param_Contrasenna NVARCHAR(100)    -- Contraseña en texto plano
)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @UsuarioID INT;
    DECLARE @ContrasennaEnBD VARBINARY(128);
    DECLARE @ContrasennaDesencriptada NVARCHAR(100);
    DECLARE @TokenSesion NVARCHAR(255);

    -- Buscar usuario activo
    SELECT TOP 1 
        @UsuarioID = UsuarioID,
        @ContrasennaEnBD = Contrasenna
    FROM Usuario
    WHERE Estado = 0
    AND (Correo = @param_Identificador OR NumeroTelefono = @param_Identificador);

    -- Validación de existencia
    IF @UsuarioID IS NULL
    BEGIN
        SELECT 'ERROR' AS Estado, 'Usuario no encontrado o inactivo' AS Mensaje;
        RETURN;
    END

    -- Abrir llave simétrica
    BEGIN TRY
        OPEN SYMMETRIC KEY Usuario_Key_01
        DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;
    END TRY
    BEGIN CATCH
        SELECT 'ERROR' AS Estado, 'Error al abrir la llave simétrica' AS Mensaje;
        RETURN;
    END CATCH

    -- Desencriptar contraseña
    SET @ContrasennaDesencriptada = CAST(DecryptByKey(@ContrasennaEnBD) AS NVARCHAR(100));

    -- Cerrar llave
    CLOSE SYMMETRIC KEY Usuario_Key_01;

    -- Comparar contraseñas
    IF @param_Contrasenna <> @ContrasennaDesencriptada
    BEGIN
        SELECT 'ERROR' AS Estado, 'Contraseña incorrecta' AS Mensaje;
        RETURN;
    END

    -- Generar token único
    SET @TokenSesion = CONVERT(NVARCHAR(255), NEWID());

    -- Insertar sesión
    INSERT INTO Sesion (UsuarioID, Token)
    VALUES (@UsuarioID, @TokenSesion);

    -- Éxito
    SELECT 'OK' AS Estado, 'Inicio de sesión exitoso' AS Mensaje, @UsuarioID AS UsuarioID, @TokenSesion AS Token;
END;

EXEC sp_LoginUsuario
    @param_Identificador = '1',
    @param_Contrasenna = '123';

	SELECT *
FROM Usuario
WHERE Estado = 0;