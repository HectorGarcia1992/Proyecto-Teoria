CREATE VIEW vw_retencion_clientes AS
WITH ClientesAnuales AS (
    SELECT
        YEAR(F.FechaFactura) AS A�o,
        F.ClienteID,
        COUNT(F.FacturaID) AS NumeroFacturas,
        SUM(F.MontoTotal) AS GastoTotal
    FROM Facturas F
    GROUP BY YEAR(F.FechaFactura), F.ClienteID
),
RangoFechas AS (
    SELECT 
        MIN(YEAR(F.FechaFactura)) AS A�oMinimo,
        MAX(YEAR(F.FechaFactura)) AS A�oMaximo,
        MAX(F.FechaFactura) AS FechaMaxima
    FROM Facturas F
),
Consecutivos AS (
    SELECT
        CA1.ClienteID,
        CA1.A�o,
        CA1.NumeroFacturas,
        CA1.GastoTotal,
        CASE 
            -- Verifica si el cliente tiene compras consecutivas desde el A�oMinimo hasta el A�oMaximo
            WHEN NOT EXISTS (
                SELECT 1
                FROM (SELECT A�oMinimo, A�oMaximo FROM RangoFechas) AS Rango
                LEFT JOIN ClientesAnuales CA2
                ON CA2.ClienteID = CA1.ClienteID AND CA2.A�o = CA1.A�o + (Rango.A�oMaximo - Rango.A�oMinimo)
                WHERE CA2.ClienteID IS NULL
            ) 
            AND EXISTS (
                -- Verifica si la �ltima compra fue dentro de los 730 d�as desde la FechaMaxima
                SELECT 1
                FROM ClientesAnuales CA3
                WHERE CA3.ClienteID = CA1.ClienteID
                AND CA3.A�o = (SELECT MAX(A�o) FROM ClientesAnuales WHERE ClienteID = CA1.ClienteID)
                AND CA3.A�o >= YEAR(DATEADD(DAY, -730, (SELECT FechaMaxima FROM RangoFechas)))
            ) THEN 'Retenido'
            ELSE 'No Retenido'
        END AS Retencion
    FROM ClientesAnuales CA1
)
SELECT *
FROM Consecutivos;
GO
