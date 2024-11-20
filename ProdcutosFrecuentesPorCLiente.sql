CREATE VIEW ProductosFrecuentesPorCliente AS
SELECT 
    c.ClienteID,
    p.ProductoID,
    p.Nombre AS ProductoNombre,
    SUM(df.Cantidad) AS CantidadTotalComprada
FROM 
    Clientes c
JOIN 
    Facturas f ON c.ClienteID = f.ClienteID
JOIN 
    DetalleFactura df ON f.FacturaID = df.FacturaID
JOIN 
    Productos p ON df.ProductoID = p.ProductoID
GROUP BY 
    c.ClienteID, p.ProductoID, p.Nombre;
GO