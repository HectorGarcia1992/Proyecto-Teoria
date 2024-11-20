CREATE VIEW ClientesSucursales AS
SELECT 
    c.ClienteID,
    c.Nombre + ' ' + c.Apellido AS ClienteNombre,
    f.SucursalID,
    s.Nombre AS SucursalNombre,
    COUNT(f.FacturaID) AS TotalVisitas
FROM 
    Clientes c
JOIN 
    Facturas f ON c.ClienteID = f.ClienteID
JOIN 
    Sucursales s ON f.SucursalID = s.SucursalID
GROUP BY 
    c.ClienteID, c.Nombre, c.Apellido, f.SucursalID, s.Nombre;
GO
