import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta

 #  Configurar la conexión a la base de datos
connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=OMER\\SQLEXPRESS01;"  # Cambiar por el nombre del servidor
    "Database=SistemaFacturacion3;"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()
cursor.fast_executemany = True
fake = Faker()
Faker.seed(42)  # Para datos consistentes

#configuraciones iniciales 
START_DATE = datetime(2014, 1, 1)
END_DATE = datetime.now()

# Datos base
telefonos_paises = {
    'Honduras': '504',
    'Costa Rica': '506',
    'Nicaragua': '505',
    'El Salvador': '503',
    'Guatemala': '502'
}
localidades_paises = {
    'Honduras': ['Tegucigalpa', 'San Pedro Sula', 'La Ceiba'],
    'Costa Rica': ['San José', 'Alajuela', 'Cartago'],
    'Nicaragua': ['Managua', 'León', 'Granada'],
    'El Salvador': ['San Salvador', 'Santa Ana', 'La Libertad'],
    'Guatemala': ['Ciudad de Guatemala', 'Antigua', 'Quetzaltenango']
}

# Datos de prueba: Países, Departamentos y Municipios
estructura_paises = {
    "Honduras": {
        "Francisco Morazán": ["Tegucigalpa", "Comayagüela"],
        "Cortés": ["San Pedro Sula", "Puerto Cortés", "La Lima"],
        "Atlántida": ["La Ceiba", "Tela"],
        "Choluteca": ["Choluteca", "San Marcos de Colón"]
    },
    "Guatemala": {
        "Guatemala": ["Ciudad de Guatemala", "Mixco"],
        "Sacatepéquez": ["Antigua Guatemala", "Ciudad Vieja"],
        "Escuintla": ["Escuintla", "Puerto de San José"]
    },
    "El Salvador": {
        "San Salvador": ["San Salvador", "Soyapango"],
        "La Libertad": ["Santa Tecla", "Nuevo Cuscatlán"],
        "Santa Ana": ["Santa Ana", "Metapán"]
    },
    "Nicaragua": {
        "Managua": ["Managua", "Masaya", "Carazo"],
        "León": ["León", "Chinandega", "El Sauce"],
        "Chinandega": ["Chinandega", "Corinto", "Somotillo"],
        "Rivas": ["Rivas", "San Juan del Sur"]
    },
    "Costa Rica": {
        "San José": ["San José", "Escazú", "Desamparados"],
        "Alajuela": ["Alajuela", "Grecia", "San Ramón"],
        "Cartago": ["Cartago", "Turrialba", "Paraíso"],
        "Guanacaste": ["Liberia", "Nicoya", "Santa Cruz"]
    }
}


# Insertar países, departamentos y municipios
def insertar_paises_departamentos_municipios():
      for pais, departamentos in estructura_paises.items():
          # Insertar país si no existe
          cursor.execute("SELECT COUNT(*) FROM Paises WHERE NombrePais = ?", pais)
          if cursor.fetchone()[0] == 0:
              cursor.execute("INSERT INTO Paises (NombrePais) VALUES (?)", pais)
          connection.commit()
  
          # Obtener ID del país
          cursor.execute("SELECT PaisID FROM Paises WHERE NombrePais = ?", pais)
          pais_id = cursor.fetchone()[0]
  
          for departamento, municipios in departamentos.items():
              # Insertar departamento si no existe
              cursor.execute(
                  "SELECT COUNT(*) FROM Departamentos WHERE NombreDepartamento = ? AND PaisID = ?",
                  departamento,
                  pais_id
              )
              if cursor.fetchone()[0] == 0:
                  cursor.execute(
                      "INSERT INTO Departamentos (NombreDepartamento, PaisID) VALUES (?, ?)",
                      departamento,
                      pais_id
                  )
              connection.commit()
  
              # Obtener ID del departamento
              cursor.execute(
                  "SELECT DepartamentoID FROM Departamentos WHERE NombreDepartamento = ? AND PaisID = ?",
                  departamento,
                  pais_id
              )
              departamento_id = cursor.fetchone()[0]
  
              for municipio in municipios:
                  # Insertar municipio si no existe
                  cursor.execute(
                      "SELECT COUNT(*) FROM Municipios WHERE NombreMunicipio = ? AND DepartamentoID = ?",
                      municipio,
                      departamento_id
                  )
                  if cursor.fetchone()[0] == 0:
                      cursor.execute(
                          "INSERT INTO Municipios (NombreMunicipio, DepartamentoID) VALUES (?, ?)",
                          municipio,
                          departamento_id
                      )
          connection.commit()
         
  
  # Llamar a la función
print("Insertando países, departamentos y municipios...")
insertar_paises_departamentos_municipios()
print("¡Datos insertados correctamente!")
  
  
def insertar_productos():
      productos_comunes = ['Soda', 'Pan', 'Tortillas', 'Arroz', 'Frijoles', 'Carne', 'Pollo']
      productos_especificos = {
          'Honduras': ['Baleada', 'Tajadas con carne', 'Enchiladas'],
          'Costa Rica': ['Gallo Pinto', 'Casado', 'Sopa Negra'],
          'El Salvador': ['Pupusas', 'Yuca con chicharrón'],
          'Guatemala': ['Pepián', 'Kak’ik'],
          'Nicaragua': ['Vigorón', 'Indio viejo']
      }
  
      cursor.execute("SELECT PaisID, NombrePais FROM Paises")
      paises = cursor.fetchall()
  
      # Insertar productos comunes para todos los países
      for producto in productos_comunes:
          cursor.execute("INSERT INTO Productos (Nombre, Descripción) VALUES (?, ?)", (producto, 'Producto común'))
      
      # Insertar productos específicos según el país
      for pais in paises:
          pais_id, nombre_pais = pais
          if nombre_pais in productos_especificos:
              for producto in productos_especificos[nombre_pais]:
                  cursor.execute("INSERT INTO Productos (Nombre, Descripción) VALUES (?, ?)", (producto, f'Producto típico de {nombre_pais}'))
      
      # Confirmar cambios
      connection.commit()
  
      # Llamar a la función
print("Insertando productos...")
insertar_productos()
print("¡Datos insertados correctamente!")
  
  
  # Función para insertar cambios de precio de productos
def insertar_precios_productos():
      cursor.execute("SELECT ProductoID FROM Productos")
      productos = cursor.fetchall()
  
      for producto in productos:
          for año in range(2014, 2024):  # 10 años
              precio = round(random.uniform(5, 100), 2)
              fecha_inicio = datetime(año, 1, 1)
              cursor.execute(
                  "INSERT INTO PreciosProductos (ProductoID, Precio, Fecha) VALUES (?, ?, ?)",
                  producto.ProductoID, precio, fecha_inicio
              )
          connection.commit()
  
print("Insertando precio prodcutos...")
insertar_precios_productos()
print("¡Datos insertados correctamente!")
  
  # Método para poblar la tabla Inventarios
def insertar_inventarios():
      # Obtener todos los productos y sucursales
      cursor.execute("SELECT ProductoID FROM Productos")
      productos = cursor.fetchall()
  
      cursor.execute("SELECT SucursalID FROM Sucursales")
      sucursales = cursor.fetchall()
  
      # Insertar inventarios para cada producto y sucursal
      for producto in productos:
          for sucursal in sucursales:
              producto_id = producto[0]
              sucursal_id = sucursal[0]
  
              # Generar stock aleatorio (por ejemplo entre 0 y 1000)
              stock = random.randint(0, 1000)
  
              # Insertar el inventario
              cursor.execute(
                  "INSERT INTO Inventarios (ProductoID, SucursalID, Stock) "
                  "VALUES (?, ?, ?)",
                  producto_id, sucursal_id, stock
              )
  
      # Confirmar cambios
      connection.commit()
  
  # Llamada a la función
print("Insertando inventarios...")
insertar_inventarios()
print("¡Inventarios insertados correctamente!")
  
  
  
  
  # Insertar sucursales
def insertar_sucursales():
      cursor.execute("SELECT PaisID, NombrePais FROM Paises")
      paises = cursor.fetchall()
  
      for pais_id, nombre_pais in paises:
          # Obtenemos los departamentos y municipios según la estructura
          departamentos = estructura_paises.get(nombre_pais, {})
          for departamento, municipios in departamentos.items():
              # Obtener el ID del departamento
              cursor.execute("SELECT DepartamentoID FROM Departamentos WHERE NombreDepartamento = ? AND PaisID = ?", departamento, pais_id)
              departamento_id = cursor.fetchone()[0]
  
              for _ in range(30):  # 30 sucursales por país
                  # Seleccionar una localidad (municipio) aleatoriamente de los municipios del departamento
                  municipio = random.choice(municipios)
                  cursor.execute("SELECT MunicipioID FROM Municipios WHERE NombreMunicipio = ? AND DepartamentoID = ?", municipio, departamento_id)
                  municipio_id = cursor.fetchone()[0]
  
                  # Generar datos para la sucursal
                  nombre_sucursal = fake.company()
                  telefono = f"{telefonos_paises[nombre_pais]}-{random.randint(10000000, 99999999)}"
                  email = fake.company_email()
  
                  # Insertar la sucursal
                  cursor.execute(
                      "INSERT INTO Sucursales (Nombre, Teléfono, Email) VALUES (?, ?, ?)",
                      nombre_sucursal, telefono, email
                  )
  
                  # Obtener el ID de la sucursal insertada
                  sucursal_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
  
                  # Insertar la dirección de la sucursal con el municipio
                  cursor.execute(
                      "INSERT INTO DireccionesSucursales (SucursalID, MunicipioID, DireccionDetalle) "
                      "VALUES (?, ?, ?)",
                      sucursal_id, municipio_id, f"{municipio}, {fake.street_address()}"
                  )
      
      connection.commit()
  
      # Llamar a la función
print("Insertando sucursales...")
insertar_sucursales()
print("¡Datos insertados correctamente!")
  
  
def insertar_clientes():
      num_clientes = 1200000  # Total de clientes
      ssns_usados = set()  # Conjunto para almacenar SSNs ya utilizados
      for _ in range(num_clientes):
          while True:
              numero_identidad = fake.ssn()
              if numero_identidad not in ssns_usados:  # Verificar que el SSN no haya sido utilizado
                  ssns_usados.add(numero_identidad)  # Añadir el SSN al conjunto
                  break  # Romper el ciclo si el SSN es único
  
          nombre = fake.first_name()
          apellido = fake.last_name()
          telefono = f"{random.choice(list(telefonos_paises.values()))}{random.randint(10000000, 99999999)}"
          email = fake.email()
          fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=60)
  
          # Insertar el cliente en la base de datos
          cursor.execute(
              "INSERT INTO Clientes (Nombre, Apellido, NúmeroIdentidad, Teléfono, Email, FechaNacimiento) "
              "VALUES (?, ?, ?, ?, ?, ?)",
              nombre, apellido, numero_identidad, telefono, email, fecha_nacimiento
          )
  
          connection.commit()  # Confirmar la inserción del cliente
  
  # Llamada a la función
print("Insertando clientes ...")
insertar_clientes()
print("¡Datos insertados correctamente!")

# Pre-cargar los IDs de municipios, departamentos y países en memoria
cursor.execute("""
    SELECT 
        p.NombrePais, d.NombreDepartamento, m.NombreMunicipio, m.MunicipioID
    FROM Municipios m
    JOIN Departamentos d ON m.DepartamentoID = d.DepartamentoID
    JOIN Paises p ON d.PaisID = p.PaisID
""")
municipios_cache = cursor.fetchall()
municipios_dict = {
    (row[0], row[1], row[2]): row[3] for row in municipios_cache
}

cursor.execute("SELECT ClienteID FROM Clientes")
clientes = [row[0] for row in cursor.fetchall()]

#insertar direcciones de clientes
def insertar_direcciones():
    # Configurar lotes de inserción
    num_direcciones = 500  # Total de direcciones a insertar
    batch_size = 100
    batch = []

    for _ in range(num_direcciones):
        # Seleccionar un cliente aleatorio
        cliente_id = random.choice(clientes)

        # Seleccionar un país, departamento y municipio aleatorio
        pais = random.choice(list(estructura_paises.keys()))
        departamento = random.choice(list(estructura_paises[pais].keys()))
        municipio = random.choice(estructura_paises[pais][departamento])

        # Buscar el MunicipioID usando el caché
        municipio_id = municipios_dict.get((pais, departamento, municipio))
        if municipio_id is None:
            continue  # Saltar si no se encuentra el municipio

        direccion_detalle = fake.address()

        # Agregar al lote
        batch.append((cliente_id, municipio_id, direccion_detalle))

        # Insertar cuando el lote esté lleno
        if len(batch) >= batch_size:
            cursor.executemany(
                """
                INSERT INTO DireccionesClientes (ClienteID, MunicipioID, DireccionDetalle)
                VALUES (?, ?, ?)
                """,
                batch
            )
            connection.commit()
            batch = []  # Vaciar el lote

    # Insertar cualquier resto en el lote
    if batch:
        cursor.executemany(
            """
            INSERT INTO DireccionesClientes (ClienteID, MunicipioID, DireccionDetalle)
            VALUES (?, ?, ?)
            """,
            batch
        )
        connection.commit()

print("Insertando direcciones de clientes ...")
insertar_direcciones()
print("¡Datos insertados correctamente!")


# Función para determinar el número de facturas basadas en el comportamiento de compra
def obtener_num_facturas(comportamiento):
    if comportamiento == 'frecuente':
        return random.randint(30, 52)  # 15 a 30 facturas para clientes frecuentes
    elif comportamiento == 'ocasional':
        return random.randint(15, 29)  # 5 a 10 facturas para clientes ocasionales
    elif comportamiento == 'única vez':
        return 1  # 1 factura para clientes de una sola compra
    elif comportamiento == 'aleatoria':
        return random.randint(1, 52)  # Entre 1 y 5 facturas para clientes aleatorios

# Función para insertar facturas y detalles de facturas
def insertar_facturas_y_detalles(cantidad_total):
    # Obtener clientes existentes
    cursor.execute("SELECT ClienteID FROM Clientes")
    clientes = [row.ClienteID for row in cursor.fetchall()]
    
    # Obtener sucursales existentes
    cursor.execute("SELECT SucursalID FROM Sucursales")
    sucursales = [row.SucursalID for row in cursor.fetchall()]
    
    # Obtener productos existentes
    cursor.execute("SELECT ProductoID FROM Productos")
    productos = [row.ProductoID for row in cursor.fetchall()]
    
    # Obtener métodos de pago existentes
    cursor.execute("SELECT MetodoPagoID FROM MetodosPago")
    metodos_pago = [row.MetodoPagoID for row in cursor.fetchall()]
    
    # Consultar el número actual de facturas en la base de datos
    cursor.execute("SELECT COUNT(*) FROM Facturas")
    facturas_existentes = cursor.fetchone()[0]

    total_facturas_insertadas = facturas_existentes

    # Generar facturas hasta alcanzar la cantidad deseada
    while total_facturas_insertadas < cantidad_total:
        # Obtener un cliente, sucursal, método de pago y comportamiento aleatorio
        cliente_id = random.choice(clientes)
        sucursal_id = random.choice(sucursales)
        metodo_pago_id = random.choice(metodos_pago)
        
        # Determinar el comportamiento de compra del cliente (esto se podría agregar a una tabla cliente)
        comportamiento = random.choice(['frecuente', 'ocasional', 'única vez', 'aleatoria'])
        
        # Determinar el número de facturas para este cliente
        num_facturas = obtener_num_facturas(comportamiento)
        
        # Insertar facturas
        for _ in range(num_facturas):
            if total_facturas_insertadas >= cantidad_total:
                break  # Detener si ya se alcanzó la cantidad total

            fecha_factura = fake.date_time_between(start_date=START_DATE, end_date=END_DATE)  # Fecha aleatoria
            monto_total = random.uniform(50, 500)  # Monto total aleatorio para la factura
            valoracion = random.uniform(1, 6)

            cursor.execute("""
                INSERT INTO Facturas (SucursalID, ClienteID, MetodoPagoID, FechaFactura, MontoTotal, Valoracion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, sucursal_id, cliente_id, metodo_pago_id, fecha_factura, monto_total, valoracion)
            connection.commit()

            # Obtener la FacturaID generada
            factura_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

            # Insertar detalles de la factura (productos)
            num_productos = random.randint(1, 5)  # Número aleatorio de productos por factura
            for _ in range(num_productos):
                producto_id = random.choice(productos)
                cantidad = random.randint(1, 10)  # Cantidad aleatoria de productos
                precio_unitario = random.uniform(10, 100)  # Precio unitario aleatorio

                cursor.execute("""
                    INSERT INTO DetalleFactura (FacturaID, ProductoID, Cantidad, PrecioUnitario)
                    VALUES (?, ?, ?, ?)
                """, factura_id, producto_id, cantidad, precio_unitario)
                connection.commit()

            total_facturas_insertadas += 1

        # Log para seguimiento
        print(f"Facturas insertadas hasta ahora: {total_facturas_insertadas}")

    print(f"¡Proceso completado! Total de facturas insertadas: {total_facturas_insertadas}")

# Llamar a la función de inserción de facturas por lotes
print("Insertando facturas ...")
insertar_facturas_y_detalles(24000000)  # Insertar 100 facturas por lote
print("¡Datos insertados correctamente!")



  # Cerrar la conexión
cursor.close()
connection.close()
