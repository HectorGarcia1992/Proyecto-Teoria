CREATE VIEW DetallesCompras AS
SELECT 
    f.FacturaID,
    f.FechaFactura,
    f.ClienteID,
    f.SucursalID,
    df.ProductoID,
    df.Cantidad,
    df.Subtotal
FROM 
    Facturas f
JOIN 
    DetalleFactura df ON f.FacturaID = df.FacturaID;
GO