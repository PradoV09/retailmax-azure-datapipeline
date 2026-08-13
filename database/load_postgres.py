import os
import psycopg2
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "retailmax",
    "user": "retailmax",
    "password": "retailmax123",
}

# Ruta del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpeta donde data-generation.py guarda los CSV
CSV_DIR = os.path.join(BASE_DIR, "data", "raw", "csv")
JSON_DIR = os.path.join(BASE_DIR, "data", "raw", "json")

def conectar_postgresql():
    try:
        conexion = psycopg2.connect(**DB_CONFIG)
        print("Conexión exitosa a PostgreSQL")
        return conexion

    except psycopg2.Error as error:
        print(f"Error al conectar con PostgreSQL: {error}")
        raise

def crear_tablas(cursor):

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mstr_proveedores (
            id_proveedor UUID PRIMARY KEY,
            razon_social VARCHAR(150),
            pais_origen VARCHAR(50),
            tiempo_repo_dias INTEGER,
            calificacion_calidad CHAR(1),
            activo BOOLEAN
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mstr_articulos (
            id_articulo UUID PRIMARY KEY,
            cod_barra VARCHAR(20),
            desc_art VARCHAR(255),
            id_categ_n1 INTEGER,
            id_categ_n2 INTEGER,
            id_categ_n3 INTEGER,
            id_proveedor UUID,
            precio_lista NUMERIC(12,2),
            peso_kg NUMERIC(8,2),
            unid_medida VARCHAR(10),
            activo BOOLEAN,
            fec_alta DATE,

            CONSTRAINT fk_articulo_proveedor
                FOREIGN KEY (id_proveedor)
                REFERENCES mstr_proveedores(id_proveedor)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mstr_tiendas (
            id_tienda UUID PRIMARY KEY,
            nom_tienda VARCHAR(150),
            tipo_tienda VARCHAR(50),
            id_pais INTEGER,
            id_ciudad INTEGER,
            metros_cuadrados NUMERIC(10,2),
            activo BOOLEAN,
            fec_apertura DATE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crm_miembros (
            id_miembro UUID PRIMARY KEY,
            fec_registro DATE,
            id_ciudad INTEGER,
            genero CHAR(1),
            rango_edad VARCHAR(10),
            canal_pref VARCHAR(30),
            activo BOOLEAN,
            fec_ultima_compra DATE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trans_ventas (
            id_trans VARCHAR(16) PRIMARY KEY,
            id_miembro UUID,
            id_tienda UUID,
            art_id UUID,
            fec_trans DATE,
            hra_trans TIME,
            qty_vendida INTEGER,
            precio_unitario_venta NUMERIC(12,2),
            descuento_aplicado NUMERIC(5,2),
            tipo_pago VARCHAR(50),
            canal_venta VARCHAR(30),

            CONSTRAINT fk_venta_miembro
                FOREIGN KEY (id_miembro)
                REFERENCES crm_miembros(id_miembro),

            CONSTRAINT fk_venta_tienda
                FOREIGN KEY (id_tienda)
                REFERENCES mstr_tiendas(id_tienda),

            CONSTRAINT fk_venta_articulo
                FOREIGN KEY (art_id)
                REFERENCES mstr_articulos(id_articulo)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inv_stock_diario (
            id_snapshot UUID PRIMARY KEY,
            art_id UUID,
            id_tienda UUID,
            fec_snapshot DATE,
            stock_fisico INTEGER,
            stock_transito INTEGER,
            stock_reservado INTEGER,
            stock_minimo_config INTEGER,
            stock_maximo_config INTEGER,

            CONSTRAINT fk_stock_articulo
                FOREIGN KEY (art_id)
                REFERENCES mstr_articulos(id_articulo),

            CONSTRAINT fk_stock_tienda
                FOREIGN KEY (id_tienda)
                REFERENCES mstr_tiendas(id_tienda)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_devoluciones (
            id_devolucion UUID PRIMARY KEY,
            id_trans_origen UUID,
            art_id UUID,
            id_tienda UUID,
            fec_devolucion DATE,
            qty_devuelta INTEGER,
            motivo_cod VARCHAR(30),
            canal_devolucion VARCHAR(30),
            estado_devolucion VARCHAR(30),
            vr_reembolso NUMERIC(12,2),

            CONSTRAINT fk_devolucion_transaccion
                FOREIGN KEY (id_trans_origen)
                REFERENCES trans_ventas(id_trans),

            CONSTRAINT fk_devolucion_articulo
                FOREIGN KEY (art_id)
                REFERENCES mstr_articulos(id_articulo),

            CONSTRAINT fk_devolucion_tienda
                FOREIGN KEY (id_tienda)
                REFERENCES mstr_tiendas(id_tienda)
        );
    """)

    print("Tablas creadas correctamente")

def cargar_csv(cursor, nombre_archivo, nombre_tabla, columnas):

    ruta = os.path.join(CSV_DIR, nombre_archivo)

    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    df = pd.read_csv(ruta)

    # Convertir NaN de pandas a None para PostgreSQL
    df = df.where(pd.notnull(df), None)

    columnas_sql = ", ".join(columnas)
    placeholders = ", ".join(["%s"] * len(columnas))

    sql = f"""
        INSERT INTO {nombre_tabla} ({columnas_sql})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING;
    """

    registros = [
        tuple(fila[columna] for columna in columnas) for _, fila in df.iterrows()
    ]

    cursor.executemany(sql, registros)

    print(f"{nombre_tabla}: {len(registros):,} registros procesados")

def main():

    conexion = conectar_postgresql()

    try:

        cursor = conexion.cursor()

        # Crear tablas
        crear_tablas(cursor)
        conexion.commit()

        cargar_csv(
            cursor,
            "MSTR_PROVEEDORES.csv",
            "mstr_proveedores",
            [
                "id_proveedor",
                "razon_social",
                "pais_origen",
                "tiempo_repo_dias",
                "calificacion_calidad",
                "activo",
            ],
        )

        cargar_csv(
            cursor,
            "MSTR_ARTICULOS.csv",
            "mstr_articulos",
            [
                "id_articulo",
                "cod_barra",
                "desc_art",
                "id_categ_n1",
                "id_categ_n2",
                "id_categ_n3",
                "id_proveedor",
                "precio_lista",
                "peso_kg",
                "unid_medida",
                "activo",
                "fec_alta",
            ],
        )

        cargar_csv(
            cursor,
            "MSTR_TIENDAS.csv",
            "mstr_tiendas",
            [
                "id_tienda",
                "nom_tienda",
                "tipo_tienda",
                "id_pais",
                "id_ciudad",
                "metros_cuadrados",
                "activo",
                "fec_apertura",
            ],
        )

        cargar_csv(
            cursor,
            "CRM_MIEMBROS.csv",
            "crm_miembros",
            [
                "id_miembro",
                "fec_registro",
                "id_ciudad",
                "genero",
                "rango_edad",
                "canal_pref",
                "activo",
                "fec_ultima_compra",
            ],
        )

        cargar_csv(
            cursor,
            "TRANS_VENTAS.csv",
            "trans_ventas",
            [
                "id_trans",
                "id_miembro",
                "id_tienda",
                "art_id",
                "fec_trans",
                "hra_trans",
                "qty_vendida",
                "precio_unitario_venta",
                "descuento_aplicado",
                "tipo_pago",
                "canal_venta",
            ],
        )

        cargar_csv(
            cursor,
            "INV_STOCK_DIARIO.csv",
            "inv_stock_diario",
            [
                "id_snapshot",
                "art_id",
                "id_tienda",
                "fec_snapshot",
                "stock_fisico",
                "stock_transito",
                "stock_reservado",
                "stock_minimo_config",
                "stock_maximo_config",
            ],
        )

        cargar_csv(
            cursor,
            "POST_DEVOLUCIONES.csv",
            "post_devoluciones",
            [
                "id_devolucion",
                "id_trans_origen",
                "art_id",
                "id_tienda",
                "fec_devolucion",
                "qty_devuelta",
                "motivo_cod",
                "canal_devolucion",
                "estado_devolucion",
                "vr_reembolso",
            ],
        )

        conexion.commit()

        print("\nCarga completada correctamente")

        tablas = [
            "mstr_proveedores",
            "mstr_articulos",
            "mstr_tiendas",
            "crm_miembros",
            "trans_ventas",
            "inv_stock_diario",
            "post_devoluciones",
        ]

        print("\nConteo de registros:")

        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla};")

            cantidad = cursor.fetchone()[0]

            print(f"  {tabla}: {cantidad:,}")

    except Exception as error:
        conexion.rollback()
        print(f"\nError durante la carga: {error}")
        raise
    finally:
        cursor.close()
        conexion.close()
        print("\nConexión cerrada")

if __name__ == "__main__":
    main()
