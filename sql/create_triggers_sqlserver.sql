-- ============================================================
-- StreamUCV — SQL Server
-- Script: create_triggers_sqlserver.sql
-- Descripcion: Triggers de prueba para el reporte de integridad.
-- ============================================================

USE StreamUCV;
GO

DROP TRIGGER IF EXISTS streaming.trg_serie_after_insert;
DROP TRIGGER IF EXISTS streaming.trg_artista_after_update;
DROP TRIGGER IF EXISTS streaming.trg_lanzar_after_delete;
DROP TRIGGER IF EXISTS streaming.trg_pelicula_after_update;
DROP TRIGGER IF EXISTS streaming.trg_venta_after_insert;
GO

-- AFTER INSERT en serie
CREATE TRIGGER streaming.trg_serie_after_insert
ON streaming.serie
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM inserted)
        RETURN;
END;
GO

-- AFTER UPDATE en artista
CREATE TRIGGER streaming.trg_artista_after_update
ON streaming.artista
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM inserted)
        RETURN;
END;
GO

-- AFTER DELETE en lanzar
CREATE TRIGGER streaming.trg_lanzar_after_delete
ON streaming.lanzar
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM deleted)
        RETURN;
END;
GO

-- AFTER UPDATE en pelicula
CREATE TRIGGER streaming.trg_pelicula_after_update
ON streaming.pelicula
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM inserted)
        RETURN;
END;
GO

-- AFTER INSERT en venta (se crea deshabilitado)
CREATE TRIGGER streaming.trg_venta_after_insert
ON streaming.venta
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM inserted)
        RETURN;
END;
GO

DISABLE TRIGGER streaming.trg_venta_after_insert ON streaming.venta;
GO
