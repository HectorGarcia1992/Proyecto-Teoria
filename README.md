SELECT 
    f.FacturaID,
    f.MontoTotal,
    f.Valoracion,
    f.SucursalID,
    f.MetodoPagoID,
    c.ClienteID,
    s.Nombre AS SucursalNombre,
    mp.NombreMetodo AS MetodoPagoNombre
FROM 
    Facturas f
JOIN 
    Clientes c ON f.ClienteID = c.ClienteID
JOIN 
    Sucursales s ON f.SucursalID = s.SucursalID
JOIN 
    MetodosPago mp ON f.MetodoPagoID = mp.MetodoPagoID;

