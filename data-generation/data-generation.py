# importación de librerías necesarias
from faker import Faker
import yaml
import pandas as pd
import numpy as np
import os

# Abrir el archivo YAML
with open('config.yaml', 'r', encoding='utf-8') as archivo:
    # Cargar los datos de forma segura
    datos = yaml.full_load(archivo)

# Extraer la semilla de datos del archivo YAML
semilla = datos['semilla']
Faker.seed(semilla)  # Establecer una semilla para reproducibilidad
fake = Faker('es_CO')  # Configurar Faker para generar datos en español (Colombia)
print("Semilla de datos establecida:", semilla)

# Extraer los volúmenes de datos
MSTR_ARTICULOS = datos['MSTR_ARTICULOS']
MSTR_PROVEEDORES = datos['MSTR_PROVEEDORES']
MSTR_TIENDAS = datos['MSTR_TIENDAS']
CRM_MIEMBROS = datos['CRM_MIEMBROS']
TRANS_VENTAS = datos['TRANS_VENTAS']
INV_STOCK_DIARIO = datos['INV_STOCK_DIARIO']
POST_DEVOLUCIONES = datos['POST_DEVOLUCIONES']
MICRO_CATEGORIAS = datos['MICRO_CATEGORIAS']

# Paises y ciudades
PAISES = datos['PAISES']
CIUDADES = datos['CIUDADES']

# Tipo tiendas
TIPOS_TIENDA = datos['TIPOS_TIENDA']

print("Datos cargados desde el archivo YAML")

#MSTR_PROVEEDORES
def mstr_proveedores(num_proveedores):
    proveedores = []
    for i in range(num_proveedores):
        proveedor = {
            'id_proveedor': fake.uuid4(),
            'razon_social': fake.company(),
            'pais_origen': fake.random_element(elements=[pais['nombre'] for pais in PAISES]),
            'tiempo_repo_dias': fake.random_int(min=1, max=30),
            'calificacion_calidad': fake.random_element(elements=('A', 'B', 'C', 'D')),
            'activo': fake.boolean(chance_of_getting_true=80)
        }
        proveedores.append(proveedor)
    return pd.DataFrame(proveedores)

mstr_proveedores_df = mstr_proveedores(MSTR_PROVEEDORES)
print("MSTR_PROVEEDORES generados:", len(mstr_proveedores_df))

# Mapeo de nombres de categoría -> IDs numéricos (jerárquico)
# id_categ_n1: id por nombre de categoría nivel 1
# id_categ_n2: id por (nivel1, nivel2), reinicia en cada categoría padre
# id_categ_n3: id por (nivel1, nivel2, nivel3), reinicia en cada subcategoría padre
categorias_n1_list = list(MICRO_CATEGORIAS.keys())
id_categ_n1_map = {nombre: i + 1 for i, nombre in enumerate(categorias_n1_list)}

id_categ_n2_map = {}
id_categ_n3_map = {}
for n1 in categorias_n1_list:
    subcategorias = MICRO_CATEGORIAS[n1]
    n2_list = list(subcategorias.keys())
    for j, n2 in enumerate(n2_list):
        id_categ_n2_map[(n1, n2)] = j + 1
        microcategorias = subcategorias[n2]
        for k, n3 in enumerate(microcategorias):
            id_categ_n3_map[(n1, n2, n3)] = k + 1

def generar_articulos(num_articulos):
    articulos = []
    for i in range(num_articulos):
        # Nivel 1
        categoria_n1 = fake.random_element(elements=categorias_n1_list)
        # Nivel 2
        subcategorias = MICRO_CATEGORIAS[categoria_n1]
        categoria_n2 = fake.random_element(elements=list(subcategorias.keys()))
        # Nivel 3
        microcategorias = subcategorias[categoria_n2]
        categoria_n3 = fake.random_element(elements=microcategorias)
        articulo = {
            "id_articulo": fake.uuid4(),
            "cod_barra": fake.ean(),
            "desc_art": fake.sentence(),
            "id_categ_n1": id_categ_n1_map[categoria_n1],
            "id_categ_n2": id_categ_n2_map[(categoria_n1, categoria_n2)],
            "id_categ_n3": id_categ_n3_map[(categoria_n1, categoria_n2, categoria_n3)],
            "id_proveedor": fake.random_element(elements=mstr_proveedores_df.id_proveedor.tolist()),
            "precio_lista": round(fake.random_number(digits=5) / 100, 2),
            "peso_kg": round(fake.random_number(digits=3) / 100, 2),
            "unid_medida": fake.random_element(
                elements=("kg", "g", "l", "ml", "m", "cm")
            ),
            "activo": fake.boolean(chance_of_getting_true=90),
            "fec_alta": fake.date_this_decade(),
        }
        articulos.append(articulo)
    return pd.DataFrame(articulos)

articulos_df = generar_articulos(MSTR_ARTICULOS)
print("MSTR_ARTICULOS generados:", len(articulos_df))

#MSTR_TIENDAS
def generar_tiendas(num_tiendas):
    tiendas = []
    for i in range(num_tiendas):
        id_pais_seleccionado = fake.random_element(elements=[pais['id_pais'] for pais in PAISES])

        tienda = {
            'id_tienda': fake.uuid4(),
            'nom_tienda': fake.company(),
            'tipo_tienda' : fake.random_element(elements=([TIPOS_TIENDA['nombre'] for TIPOS_TIENDA in TIPOS_TIENDA])),
            'id_pais': id_pais_seleccionado, 
            'id_ciudad': fake.random_element(elements=[ciudad['id_ciudad'] for ciudad in CIUDADES if ciudad['id_pais'] == id_pais_seleccionado]),
            'metros_cuadrados': fake.random_int(min=50, max=5000),
            'activo': fake.boolean(chance_of_getting_true=95),
            'fec_apertura': fake.date_this_decade()
        }
        tiendas.append(tienda)
    return pd.DataFrame(tiendas)

tiendas_df = generar_tiendas(MSTR_TIENDAS)
print("MSTR_TIENDAS generadas:", len(tiendas_df))

#CRM_MIEMBROS
def generar_miembros(num_miembros):
    miembros = []
    for i in range(num_miembros):
        miembro = {
            'id_miembro': fake.uuid4(),
            'fec_registro': fake.date_this_decade(),
            'id_ciudad': fake.random_element(elements=[ciudad['id_ciudad'] for ciudad in CIUDADES]),
            'genero': fake.random_element(elements=('M', 'F', 'O')),
            'rango_edad': fake.random_element(elements=('18-25', '26-35', '36-45', '46-55', '56+')),
            'canal_pref': fake.random_element(elements=('tienda', 'ecommerce', 'marketplace')),
            'activo': fake.boolean(chance_of_getting_true=90),
            'fec_ultima_compra': fake.date_this_decade()
        }
        miembros.append(miembro)
    return pd.DataFrame(miembros)

miembros_df = generar_miembros(CRM_MIEMBROS)
print("CRM_MIEMBROS generados:", len(miembros_df))

#TRANS_VENTAS
def generar_transacciones(num_transacciones):
    rng = np.random.default_rng(semilla)
    n = num_transacciones

    ids_articulos = articulos_df['id_articulo'].to_numpy()
    precios_lista = articulos_df['precio_lista'].to_numpy()
    ids_miembros = miembros_df['id_miembro'].to_numpy()
    ids_tiendas = tiendas_df['id_tienda'].to_numpy()

    idx_articulos = rng.integers(0, len(articulos_df), size=n)
    art_id = ids_articulos[idx_articulos]
    precio_lista_arr = precios_lista[idx_articulos]
    precio_unitario = np.round(precio_lista_arr * rng.uniform(0.85, 1.10, size=n), 2)

    # Fechas vectorizadas (rango: inicio de la década -> hoy)
    inicio = pd.Timestamp('2020-01-01').value // 10**9
    fin = pd.Timestamp.now().value // 10**9
    fec_trans = pd.to_datetime(rng.integers(inicio, fin, size=n), unit='s').date

    # Horas vectorizadas (segundos aleatorios del día -> HH:MM:SS)
    secs = rng.integers(0, 86400, size=n)
    hh = (secs // 3600).astype(str)
    mm = ((secs % 3600) // 60).astype(str)
    ss = (secs % 60).astype(str)
    hra_trans = np.char.add(np.char.add(np.char.zfill(hh, 2), ':'),
                             np.char.add(np.char.zfill(mm, 2), np.char.add(':', np.char.zfill(ss, 2))))

    # id_transaccion vectorizado (hex de 64 bits en vez de fake.uuid4() por fila)
    rand_ints = rng.integers(0, 2**63 - 1, size=n, dtype=np.int64)
    id_transaccion = np.array([f'{x:016x}' for x in rand_ints])

    return pd.DataFrame({
        'id_trans': id_transaccion,
        'id_miembro': rng.choice(ids_miembros, size=n),
        'id_tienda': rng.choice(ids_tiendas, size=n),
        'art_id': art_id,
        'fec_trans': fec_trans,
        'hra_trans': hra_trans,
        'qty_vendida': rng.integers(1, 11, size=n),
        'precio_unitario_venta': precio_unitario,
        'descuento_aplicado': rng.choice([0, 0.05, 0.10, 0.15, 0.20], size=n),
        'tipo_pago': rng.choice(['efectivo', 'tarjeta_credito', 'tarjeta_debito', 'transferencia', 'billetera digital'], size=n),
        'canal_venta': rng.choice(['tienda', 'ecommerce', 'marketplace'], size=n),
    })

transacciones_df = generar_transacciones(TRANS_VENTAS)
print("TRANS_VENTAS generadas:", len(transacciones_df))

#INV_STOCK_DIARIO
def generar_inventario(num_registros):
    inventario = []
    for i in range(num_registros):
        registro = {
            'id_snapshot': fake.uuid4(),
            'art_id': fake.random_element(elements=articulos_df.id_articulo.tolist()),
            'id_tienda': fake.random_element(elements=tiendas_df.id_tienda.tolist()),
            'fec_snapshot': fake.date_this_decade(),
            'stock_fisico': fake.random_int(min=0, max=100),
            'stock_transito': fake.random_int(min=0, max=50),
            'stock_reservado': fake.random_int(min=0, max=30),
            'stock_minimo_config': fake.random_int(min=0, max=20),
            'stock_maximo_config': fake.random_int(min=20, max=100),
        }
        inventario.append(registro)
    return pd.DataFrame(inventario)

inventario_df = generar_inventario(INV_STOCK_DIARIO)
print("INV_STOCK_DIARIO generados:", len(inventario_df))

#POST_DEVOLUCIONES
def generar_devoluciones(num_devoluciones):
    devoluciones = []
    transacciones_records = transacciones_df.to_dict('records')
    for i in range(num_devoluciones):
        # Se selecciona la transacción completa para heredar de ella
        # el artículo, la tienda, la cantidad vendida y el precio real
        transaccion_sel = fake.random_element(elements=transacciones_records)
        qty_devuelta = fake.random_int(min=1, max=transaccion_sel['qty_vendida'])

        devolucion = {
            'id_devolucion': fake.uuid4(),
            'id_trans_origen': transaccion_sel['id_trans'],
            'art_id': transaccion_sel['art_id'],
            'id_tienda': transaccion_sel['id_tienda'],
            'fec_devolucion': fake.date_this_decade(),
            'qty_devuelta': qty_devuelta,
            'motivo_cod': fake.random_element(elements=('defectuoso', 'insatisfaccion', 'error_envio', 'otro')),
            'canal_devolucion': fake.random_element(elements=('tienda', 'ecommerce', 'marketplace')),
            'estado_devolucion': fake.random_element(elements=('pendiente', 'procesada', 'rechazada')),
            'vr_reembolso': round(transaccion_sel['precio_unitario_venta'] * qty_devuelta, 2)
        }
        devoluciones.append(devolucion)
    return pd.DataFrame(devoluciones)

devoluciones_df = generar_devoluciones(POST_DEVOLUCIONES)
print("POST_DEVOLUCIONES generadas:", len(devoluciones_df))

# Anomalias
# ---------------------------------------------------------
# 3 patrones de datos anomalos documentados (requisito de la prueba)
# + 5% de nulos en campos no criticos.
# ---------------------------------------------------------

rng_anom = np.random.default_rng(semilla)

# Patron 1: Duplicados exactos en TRANS_VENTAS
# Se repiten filas ya existentes tal cual (mismo id_trans),
# simulando ventas duplicadas por reintentos del punto de venta.
pct_duplicados = 0.01
n_duplicados = max(1, int(len(transacciones_df) * pct_duplicados))
idx_duplicados = rng_anom.choice(transacciones_df.index, size=n_duplicados, replace=False)
duplicados_df = transacciones_df.loc[idx_duplicados].copy()
transacciones_df = pd.concat([transacciones_df, duplicados_df], ignore_index=True)
print(f"Patron 1 - Duplicados inyectados en TRANS_VENTAS: {n_duplicados}")

# Patron 2: Fecha fuera de rango en TRANS_VENTAS
# Un grupo de transacciones queda con fec_trans anterior al inicio
# del historico (2020-01-01), simulando errores de carga/config.
pct_fecha_invalida = 0.005
n_fecha_invalida = max(1, int(len(transacciones_df) * pct_fecha_invalida))
idx_fecha_invalida = rng_anom.choice(transacciones_df.index, size=n_fecha_invalida, replace=False)
fechas_invalidas = pd.to_datetime(
    rng_anom.integers(
        pd.Timestamp('2015-01-01').value // 10**9,
        pd.Timestamp('2019-12-31').value // 10**9,
        size=n_fecha_invalida
    ),
    unit='s'
).date
transacciones_df.loc[idx_fecha_invalida, 'fec_trans'] = fechas_invalidas
print(f"Patron 2 - Fechas fuera de rango inyectadas en TRANS_VENTAS: {n_fecha_invalida}")

# Patron 3: Inconsistencia de negocio en POST_DEVOLUCIONES
# qty_devuelta queda por encima de qty_vendida de la transaccion
# origen, y vr_reembolso deja de cuadrar con precio * cantidad.
pct_inconsistencia = 0.03
n_inconsistencia = max(1, int(len(devoluciones_df) * pct_inconsistencia))
idx_inconsistencia = rng_anom.choice(devoluciones_df.index, size=n_inconsistencia, replace=False)

devoluciones_df.loc[idx_inconsistencia, 'qty_devuelta'] = (
    devoluciones_df.loc[idx_inconsistencia, 'qty_devuelta']
    + rng_anom.integers(2, 6, size=n_inconsistencia)
)
devoluciones_df.loc[idx_inconsistencia, 'vr_reembolso'] = np.round(
    devoluciones_df.loc[idx_inconsistencia, 'vr_reembolso'] * rng_anom.uniform(1.5, 3.0, size=n_inconsistencia),
    2
)
print(f"Patron 3 - Inconsistencias de negocio inyectadas en POST_DEVOLUCIONES: {n_inconsistencia}")

# Nulos en campos no criticos (5%)
# Solo se aplica sobre campos que no son llave ni afectan calculos
# criticos (precios, cantidades, fechas de negocio, IDs).
pct_nulos = 0.05
campos_no_criticos = {
    "MSTR_ARTICULOS": (articulos_df, ["desc_art", "peso_kg"]),
    "MSTR_TIENDAS": (tiendas_df, ["metros_cuadrados"]),
    "TRANS_VENTAS": (transacciones_df, ["descuento_aplicado", "canal_venta"]),
    "POST_DEVOLUCIONES": (devoluciones_df, ["motivo_cod", "canal_devolucion"]),
}

for nombre_tabla, (df, columnas) in campos_no_criticos.items():
    for col in columnas:
        n_nulos = int(len(df) * pct_nulos)
        idx_nulos = rng_anom.choice(df.index, size=n_nulos, replace=False)
        df.loc[idx_nulos, col] = np.nan
    print(f"Nulos (5%) inyectados en {nombre_tabla}: {columnas}")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CARPETA_CSV = os.path.join(BASE_DIR, "data", "raw", "csv")
os.makedirs(CARPETA_CSV, exist_ok=True)
mstr_proveedores_df.to_csv(os.path.join(CARPETA_CSV, 'MSTR_PROVEEDORES.csv'), index=False)
articulos_df.to_csv(os.path.join(CARPETA_CSV, 'MSTR_ARTICULOS.csv'), index=False)
tiendas_df.to_csv(os.path.join(CARPETA_CSV, 'MSTR_TIENDAS.csv'), index=False)
miembros_df.to_csv(os.path.join(CARPETA_CSV, 'CRM_MIEMBROS.csv'), index=False)
transacciones_df.to_csv(os.path.join(CARPETA_CSV, 'TRANS_VENTAS.csv'), index=False)
inventario_df.to_csv(os.path.join(CARPETA_CSV, 'INV_STOCK_DIARIO.csv'), index=False)
devoluciones_df.to_csv(os.path.join(CARPETA_CSV, 'POST_DEVOLUCIONES.csv'), index=False)
print("Archivos CSV generados en:", CARPETA_CSV)

CARPETA_JSON = os.path.join(BASE_DIR, "data", "raw", "json")
os.makedirs(CARPETA_JSON, exist_ok=True)
mstr_proveedores_df.to_json(os.path.join(CARPETA_JSON, 'MSTR_PROVEEDORES.json'), index=False)
articulos_df.to_json(os.path.join(CARPETA_JSON, 'MSTR_ARTICULOS.json'), index=False)
tiendas_df.to_json(os.path.join(CARPETA_JSON, 'MSTR_TIENDAS.json'), index=False)
miembros_df.to_json(os.path.join(CARPETA_JSON, 'CRM_MIEMBROS.json'), index=False)
transacciones_df.to_json(os.path.join(CARPETA_JSON, 'TRANS_VENTAS.json'), index=False)
inventario_df.to_json(os.path.join(CARPETA_JSON, 'INV_STOCK_DIARIO.json'), index=False)
devoluciones_df.to_json(os.path.join(CARPETA_JSON, 'POST_DEVOLUCIONES.json'), index=False)
print("Archivos JSON generados en:", CARPETA_JSON)