import random
from datetime import datetime
from faker import Faker
import pyodbc

# Configurar Faker
fake = Faker()
Faker.seed(42)  # Para datos reproducibles

# Configurar conexión con SQL Server
connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=OMER\\SQLEXPRESS01;"  # Cambiar por el nombre del servidor
    "Database=SistemaFacturacion;"
    "Trusted_Connection=yes;"
)
cursor = connection.cursor()

# Lista de lugares en las ciudades de Honduras
lugares_honduras = {
    'Tegucigalpa': ['Zona 1', 'La Ronda', 'Colonia Kennedy', 'Colonia Palmira', 'Los Pinos'],
    'San Pedro Sula': ['Colonias del Valle', 'Suyapa', 'La Lima', 'El Progreso', 'Chamelecón'],
    'La Ceiba': ['La Costa', 'Centro de La Ceiba', 'Colonia 15 de Septiembre', 'La Ceiba Beach', 'Brisas de la Bahía'],
    'Choluteca': ['Barrio El Centro', 'La Cruz', 'Colonia 7 de Octubre', 'La Gloria', 'Santa Teresa']
}

# Configuración inicial
NUM_SUCURSALES = 40
CITIES = ["Tegucigalpa", "San Pedro Sula", "La Ceiba", "Choluteca"]
NUM_CLIENTES = random.randint(300_000, 400_000)
NUM_FACTURAS = 1_000_000
START_DATE = datetime(2019, 1, 1)
END_DATE = datetime.now()

# Crear sucursales
def populate_sucursales():
    print("Poblando la tabla Sucursales...")
    for i in range(NUM_SUCURSALES):
        city = random.choice(CITIES)
        cursor.execute(
            "INSERT INTO Sucursales (Nombre, Dirección, Ciudad, Teléfono, Email) VALUES (?, ?, ?, ?, ?)",
            fake.company(),
            fake.address(),
            city,
            fake.phone_number()[:8],
            fake.email(),
        )
    connection.commit()

# Crear productos (platos de un restaurante)
def populate_productos():
    print("Poblando la tabla Productos...")
    productos = [
        ('Sopa de Frijoles', 5.00),
        ('Ensalada César', 6.50),
        ('Pollo a la Parrilla', 12.00),
        ('Tacos de Carne Asada', 8.50),
        ('Baleada con Pollo', 4.00),
        ('Arroz con Pollo', 10.00),
        ('Fajitas de Res', 14.00),
        ('Pescado Frito', 12.50),
        ('Hamburguesa con Papas', 7.00),
        ('Pizza Margarita', 9.00),
        ('Pasta Alfredo', 11.00),
        ('Costillas a la Barbacoa', 15.00),
        ('Tacos de Pollo', 7.50),
        ('Chuletas de Cerdo', 13.00),
        ('Filete Mignon', 20.00),
        ('Paella de Mariscos', 18.00),
        ('Tamales de Elote', 4.50),
        ('Ceviche de Camarón', 11.50),
        ('Tortillas con Queso', 3.00),
        ('Chiles Rellenos', 10.50)
    ]
    
    for producto in productos:
        cursor.execute(
            "INSERT INTO Productos (Nombre, Precio, Stock) VALUES (?, ?, ?)",  # Incluir Stock
            producto[0],
            producto[1],
            random.randint(10, 50)  # Valor aleatorio para el stock, por ejemplo entre 10 y 50
        )
    connection.commit()

# Crear clientes
# Conjunto para verificar duplicados
numeros_identidad = set()

def populate_clientes():
    print("Poblando la tabla Clientes...")
    cantidad_de_clientes = 300000  # Ajusta la cantidad según lo que necesites
    for _ in range(cantidad_de_clientes):
        numero_identidad = fake.ssn()  # Número de identidad
        
        # Si el número ya está en el conjunto, genera uno nuevo
        while numero_identidad in numeros_identidad:
            numero_identidad = fake.ssn()

        # Añadir el número al conjunto para evitar futuros duplicados
        numeros_identidad.add(numero_identidad)

        # Insertar los datos en la base de datos
        cursor.execute(
            "INSERT INTO Clientes (Nombre, Apellido, NúmeroIdentidad, Teléfono, Email, FechaNacimiento, TarjetaCredito) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            fake.first_name(),
            fake.last_name(),
            numero_identidad,  # Número de identidad único
            fake.phone_number()[:8],
            fake.email(),
            fake.date_of_birth(minimum_age=20, maximum_age=60),
            fake.credit_card_number()
        )
    
    # Commit para guardar los cambios
    connection.commit()

# Crear facturas
def populate_facturas():
    print("Poblando la tabla Facturas...")
    cliente_ids = [row[0] for row in cursor.execute("SELECT ClienteID FROM Clientes").fetchall()]
    sucursal_ids = [row[0] for row in cursor.execute("SELECT SucursalID FROM Sucursales").fetchall()]
    productos_ids = [row[0] for row in cursor.execute("SELECT ProductoID FROM Productos").fetchall()]

    for i in range(NUM_FACTURAS):
        cliente = random.choice(cliente_ids)
        sucursal = random.choice(sucursal_ids)
        fecha = fake.date_time_between(start_date=START_DATE, end_date=END_DATE)
        monto = round(random.uniform(200, 5000), 2)
        forma_pago = random.choice(["Efectivo", "Tarjeta de Crédito", "Débito"])
        estado_factura = random.choice(["Pagado", "Pendiente"])

        # Insertar factura
        cursor.execute(
            "INSERT INTO Facturas (SucursalID, ClienteID, FechaFactura, MontoTotal, FormaPago, EstadoFactura) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            sucursal,
            cliente,
            fecha,
            monto,
            forma_pago,
            estado_factura,
        )

        # Insertar detalles de factura
        factura_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
        for _ in range(random.randint(1, 5)):  # Entre 1 y 5 productos por factura
            producto = random.choice(productos_ids)
            cantidad = random.randint(1, 10)
            precio_unitario = cursor.execute(
                "SELECT Precio FROM Productos WHERE ProductoID = ?", producto
            ).fetchone()[0]
            cursor.execute(
                "INSERT INTO DetalleFactura (FacturaID, ProductoID, Cantidad, PrecioUnitario) "
                "VALUES (?, ?, ?, ?)",
                factura_id,
                producto,
                cantidad,
                precio_unitario,
            )
    connection.commit()

# Poblar las tablas
print("Poblando la base de datos...")
populate_sucursales()
populate_clientes()
populate_productos()  # Llamar aquí para poblar los productos antes de las facturas
populate_facturas()
print("¡Datos generados exitosamente!")

# Cerrar conexión
cursor.close()
connection.close()
