CREATE VIEW ResumenComprasPorCliente AS
SELECT 
    c.ClienteID,
    c.Nombre + ' ' + c.Apellido AS ClienteNombre,
    COUNT(f.FacturaID) AS TotalCompras,
    SUM(f.MontoTotal) AS MontoTotalGastado,
    MAX(f.FechaFactura) AS UltimaCompra,
    DATEDIFF(DAY, MAX(f.FechaFactura), GETDATE()) AS DiasDesdeUltimaCompra
FROM 
    Clientes c
LEFT JOIN 
    Facturas f ON c.ClienteID = f.ClienteID
GROUP BY 
    c.ClienteID, c.Nombre, c.Apellido;
GO