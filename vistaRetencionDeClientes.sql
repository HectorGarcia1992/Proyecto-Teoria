CREATE VIEW vw_retencion_clientes AS
WITH ClientesAnuales AS (
    SELECT
        YEAR(F.FechaFactura) AS Año,
        F.ClienteID,
        COUNT(F.FacturaID) AS NumeroFacturas,
        SUM(F.MontoTotal) AS GastoTotal
    FROM Facturas F
    GROUP BY YEAR(F.FechaFactura), F.ClienteID
),
RangoFechas AS (
    SELECT 
        MIN(YEAR(F.FechaFactura)) AS AñoMinimo,
        MAX(YEAR(F.FechaFactura)) AS AñoMaximo,
        MAX(F.FechaFactura) AS FechaMaxima
    FROM Facturas F
),
Consecutivos AS (
    SELECT
        CA1.ClienteID,
        CA1.Año,
        CA1.NumeroFacturas,
        CA1.GastoTotal,
        CASE 
            -- Verifica si el cliente tiene compras consecutivas desde el AñoMinimo hasta el AñoMaximo
            WHEN NOT EXISTS (
                SELECT 1
                FROM (SELECT AñoMinimo, AñoMaximo FROM RangoFechas) AS Rango
                LEFT JOIN ClientesAnuales CA2
                ON CA2.ClienteID = CA1.ClienteID AND CA2.Año = CA1.Año + (Rango.AñoMaximo - Rango.AñoMinimo)
                WHERE CA2.ClienteID IS NULL
            ) 
            AND EXISTS (
                -- Verifica si la última compra fue dentro de los 730 días desde la FechaMaxima
                SELECT 1
                FROM ClientesAnuales CA3
                WHERE CA3.ClienteID = CA1.ClienteID
                AND CA3.Año = (SELECT MAX(Año) FROM ClientesAnuales WHERE ClienteID = CA1.ClienteID)
                AND CA3.Año >= YEAR(DATEADD(DAY, -730, (SELECT FechaMaxima FROM RangoFechas)))
            ) THEN 'Retenido'
            ELSE 'No Retenido'
        END AS Retencion
    FROM ClientesAnuales CA1
)
SELECT *
FROM Consecutivos;
GO
