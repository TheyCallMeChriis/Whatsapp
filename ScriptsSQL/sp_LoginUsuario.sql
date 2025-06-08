use MensajeriaBD
go

CREATE OR ALTER PROCEDURE sp_LoginUsuario (
    @param_Identificador NVARCHAR(100), -- correo o n�mero
    @param_Contrasenna NVARCHAR(100)    -- contrase�a en texto plano
)
AS
BEGIN
    DECLARE @UsuarioID INT;
    DECLARE @ContrasennaEnBD VARBINARY(128);
    DECLARE @ContrasennaDesencriptada NVARCHAR(100);
    DECLARE @TokenSesion NVARCHAR(255);

    -- Buscar usuario por correo o tel�fono, y que est� activo
    SELECT TOP 1 
        @UsuarioID = UsuarioID,
        @ContrasennaEnBD = Contrasenna
    FROM Usuario
    WHERE Estado = 0
      AND (Correo = @param_Identificador OR NumeroTelefono = @param_Identificador);

    -- Validaci�n de existencia
    IF @UsuarioID IS NULL
    BEGIN
        PRINT 'Usuario no encontrado o inactivo.';
        RETURN;
    END

    -- Abrir llave sim�trica
    OPEN SYMMETRIC KEY Usuario_Key_01
    DECRYPTION BY CERTIFICATE Usuario_KEY_CERT;

    -- Desencriptar contrase�a
    SET @ContrasennaDesencriptada = CAST(DecryptByKey(@ContrasennaEnBD) AS NVARCHAR(100));

    -- Cerrar llave
    CLOSE SYMMETRIC KEY Usuario_Key_01;

    -- Comparar contrase�as
    IF @param_Contrasenna <> @ContrasennaDesencriptada
    BEGIN
        PRINT 'Contrase�a incorrecta.';
        RETURN;
    END

    -- Generar token �nico
    SET @TokenSesion = CONVERT(NVARCHAR(255), NEWID());

    -- Registrar sesi�n (FechaInicio y Activa se llenan autom�ticamente por DEFAULT)
    INSERT INTO Sesion (UsuarioID, Token)
    VALUES (@UsuarioID, @TokenSesion);

    -- Respuesta exitosa
    PRINT 'Inicio de sesi�n exitoso.';
    SELECT @UsuarioID AS UsuarioID, @TokenSesion AS Token;
END;


EXEC sp_LoginUsuario
    @param_Identificador = 'jose@ucr',
    @param_Contrasenna = 'Pepe2525';
