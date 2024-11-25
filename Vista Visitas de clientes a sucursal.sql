
Create view vw_visitas_cliente_sucursales as 

Select f.ClienteID,dc.DireccionDetalle as direccion_cliente,ds.DireccionDetalle as direccion_sucursal ,
COUNT(f.SucursalID) as cantidad_de_visitas  from Facturas f

INNER JOIN DireccionesClientes dc ON
f.ClienteID= dc.ClienteID
INNER JOIN DireccionesSucursales ds ON
f.SucursalID= ds.SucursalID

group by  f.ClienteID, dc.DireccionDetalle ,ds.DireccionDetalle
