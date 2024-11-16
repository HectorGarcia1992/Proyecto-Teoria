CREATE DATABASE SistemaFacturacion;
GO

-- Usar la base de datos
USE SistemaFacturacion;
GO

-- Tabla Sucursales
CREATE TABLE Sucursales (
    SucursalID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Dirección NVARCHAR(255) NOT NULL,
    Ciudad NVARCHAR(100) NOT NULL,
    Teléfono NVARCHAR(15) NOT NULL,
    Email NVARCHAR(255) NOT NULL
);
GO

-- Tabla Clientes
CREATE TABLE Clientes (
    ClienteID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Apellido NVARCHAR(100) NOT NULL,
    NúmeroIdentidad NVARCHAR(50) NOT NULL UNIQUE,
    Teléfono NVARCHAR(15) NOT NULL,
    Email NVARCHAR(255) NOT NULL,
    FechaNacimiento DATE NOT NULL,
    TarjetaCredito NVARCHAR(19) NOT NULL
);
GO

-- Tabla Facturas
CREATE TABLE Facturas (
    FacturaID INT IDENTITY(1,1) PRIMARY KEY,
    SucursalID INT NOT NULL,
    ClienteID INT NOT NULL,
    FechaFactura DATETIME NOT NULL DEFAULT GETDATE(),
    MontoTotal DECIMAL(18,2) NOT NULL,
    FormaPago NVARCHAR(50) NOT NULL CHECK (FormaPago IN ('Efectivo', 'Tarjeta de Crédito', 'Débito')),
    EstadoFactura NVARCHAR(50) NOT NULL CHECK (EstadoFactura IN ('Pagado', 'Pendiente')),
    FOREIGN KEY (SucursalID) REFERENCES Sucursales(SucursalID),
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID)
);
GO


-- Crear tabla Productos
CREATE TABLE Productos (
    ProductoID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(255) NOT NULL,
    Descripción NVARCHAR(500) NULL,
    Precio DECIMAL(18,2) NOT NULL CHECK (Precio > 0),
    Stock INT NOT NULL CHECK (Stock >= 0)
);
GO



CREATE TABLE DetalleFactura (
    DetalleID INT IDENTITY(1,1) PRIMARY KEY,
    FacturaID INT NOT NULL,
    ProductoID INT NOT NULL,
    Cantidad INT NOT NULL CHECK (Cantidad > 0),
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    Subtotal AS (Cantidad * PrecioUnitario) PERSISTED, -- Calculado y persistido
    CONSTRAINT FK_Producto FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
);
