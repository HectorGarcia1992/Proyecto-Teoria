
--use master
--drop database SistemaFacturacion3
CREATE DATABASE SistemaFacturacion3;
GO

-- Usar la base de datos
USE SistemaFacturacion3;
GO

-- Tabla Paises
CREATE TABLE Paises (
    PaisID INT IDENTITY(1,1) PRIMARY KEY,
    NombrePais NVARCHAR(25) NOT NULL UNIQUE
);
GO

-- Tabla Departamentos (o Estados)
CREATE TABLE Departamentos (
    DepartamentoID INT IDENTITY(1,1) PRIMARY KEY,
    NombreDepartamento NVARCHAR(20) NOT NULL,
    PaisID INT NOT NULL,
    FOREIGN KEY (PaisID) REFERENCES Paises(PaisID)
);
GO

-- Tabla Municipios o Ciudades
CREATE TABLE Municipios (
    MunicipioID INT IDENTITY(1,1) PRIMARY KEY,
    NombreMunicipio NVARCHAR(25) NOT NULL,
    DepartamentoID INT NOT NULL,
    FOREIGN KEY (DepartamentoID) REFERENCES Departamentos(DepartamentoID)
);
GO

-- Tabla Clientes
CREATE TABLE Clientes (
    ClienteID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(15) NOT NULL,
    Apellido NVARCHAR(15) NOT NULL,
    NúmeroIdentidad NVARCHAR(20) NOT NULL UNIQUE,
    Teléfono NVARCHAR(15) NOT NULL,
    Email NVARCHAR(75) NOT NULL,
    FechaNacimiento DATE NOT NULL
);
GO

-- Tabla Direcciones de Clientes
CREATE TABLE DireccionesClientes (
    DireccionID INT IDENTITY(1,1) PRIMARY KEY,
    ClienteID INT NOT NULL,
    MunicipioID INT NOT NULL,
    DireccionDetalle NVARCHAR(75) NOT NULL, -- Calle, avenida, etc.
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID),
    FOREIGN KEY (MunicipioID) REFERENCES Municipios(MunicipioID)
);
GO

-- Tabla MetodosPago
CREATE TABLE MetodosPago (
    MetodoPagoID INT IDENTITY(1,1) PRIMARY KEY,
    NombreMetodo NVARCHAR(20) NOT NULL UNIQUE -- Ejemplo: 'Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito'
);
GO

-- Insertar métodos de pago predefinidos
INSERT INTO MetodosPago (NombreMetodo)
VALUES ('Efectivo'), ('Tarjeta de Crédito'), ('Tarjeta de Débito');
GO

-- Tabla Sucursales
CREATE TABLE Sucursales (
    SucursalID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(75) NOT NULL,
    Teléfono NVARCHAR(15) NOT NULL,
    Email NVARCHAR(75) NOT NULL
);
GO

-- Tabla Direcciones de Sucursales
CREATE TABLE DireccionesSucursales (
    DireccionID INT IDENTITY(1,1) PRIMARY KEY,
    SucursalID INT NOT NULL,
    MunicipioID INT NOT NULL,
    DireccionDetalle NVARCHAR(125) NOT NULL, -- Calle, avenida, etc.
    FOREIGN KEY (SucursalID) REFERENCES Sucursales(SucursalID),
    FOREIGN KEY (MunicipioID) REFERENCES Municipios(MunicipioID)
);
GO

-- Tabla Facturas (Campo MetodoPagoID permanece)
CREATE TABLE Facturas (
    FacturaID INT IDENTITY(1,1) PRIMARY KEY,
    SucursalID INT NOT NULL,
    ClienteID INT NOT NULL,
    MetodoPagoID INT NOT NULL, -- Referencia directa al método de pago usado
    FechaFactura DATETIME NOT NULL DEFAULT GETDATE(),
    MontoTotal DECIMAL(5,2) NOT NULL,
    Valoracion INT CHECK (Valoracion BETWEEN 1 AND 5), -- Valoración entre 1 y 5
    FOREIGN KEY (SucursalID) REFERENCES Sucursales(SucursalID),
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID),
    FOREIGN KEY (MetodoPagoID) REFERENCES MetodosPago(MetodoPagoID)
);
GO

-- Tabla Productos
CREATE TABLE Productos (
    ProductoID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(20) NOT NULL,
    Descripción NVARCHAR(50) NULL
);
GO

-- Tabla PreciosProductos
CREATE TABLE PreciosProductos (
    PrecioID INT IDENTITY(1,1) PRIMARY KEY,
    ProductoID INT NOT NULL,
    Precio DECIMAL(5,2) NOT NULL CHECK (Precio > 0),
    Fecha DATETIME NOT NULL DEFAULT GETDATE(), -- Solo se mantiene una columna de Fecha
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
);
GO

-- Tabla Inventarios
CREATE TABLE Inventarios (
    InventarioID INT IDENTITY(1,1) PRIMARY KEY,
    ProductoID INT NOT NULL,
    SucursalID INT NOT NULL,
    Stock INT NOT NULL CHECK (Stock >= 0),
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID),
    FOREIGN KEY (SucursalID) REFERENCES Sucursales(SucursalID)
);
GO

-- Tabla DetalleFactura
CREATE TABLE DetalleFactura (
    DetalleID INT IDENTITY(1,1) PRIMARY KEY,
    FacturaID INT NOT NULL,
    ProductoID INT NOT NULL,
    Cantidad INT NOT NULL CHECK (Cantidad > 0),
    PrecioUnitario DECIMAL(5,2) NOT NULL,
    Subtotal AS (Cantidad * PrecioUnitario) PERSISTED,
    FOREIGN KEY (FacturaID) REFERENCES Facturas(FacturaID),
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
);
GO
