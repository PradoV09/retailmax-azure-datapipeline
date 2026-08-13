# CHANGELOG

Todos los cambios importantes realizados en el proyecto RetailMax se documentan en este archivo.

## [Unreleased]

### Added
- Script de generación de datos dummy en Python.
- Configuración centralizada mediante `config.yaml`.
- Semilla fija para garantizar reproducibilidad de los datos.
- Generación de las tablas:
  - `MSTR_PROVEEDORES`
  - `MSTR_ARTICULOS`
  - `MSTR_TIENDAS`
  - `CRM_MIEMBROS`
  - `TRANS_VENTAS`
  - `INV_STOCK_DIARIO`
  - `POST_DEVOLUCIONES`
- Catálogo jerárquico de categorías y microcategorías.
- Configuración de países, ciudades y tipos de tienda mediante YAML.
- Generación de archivos de salida en formatos CSV y JSON.
- Inyección de anomalías controladas en los datos:
  - Duplicados en `TRANS_VENTAS`.
  - Fechas fuera de rango.
  - Inconsistencias en `POST_DEVOLUCIONES`.
  - Valores nulos en campos no críticos.
- Configuración de PostgreSQL mediante Docker.
- Script `load_postgres.py` para crear las tablas y cargar los archivos CSV en PostgreSQL.

### Changed
- Optimización de la generación de `TRANS_VENTAS` mediante operaciones vectorizadas con NumPy.
- Generación de precios de venta a partir del precio de lista del artículo.
- Generación de devoluciones relacionadas con una transacción de venta existente.
- Organización de los archivos generados dentro de `data/raw/csv` y `data/raw/json`.
- Ajuste de las rutas de archivos para evitar problemas al ejecutar los scripts desde diferentes directorios.

### Fixed
- Corrección de la selección de `id_proveedor` para que cada artículo tenga un único proveedor válido.
- Corrección de las relaciones entre artículos, tiendas, miembros y transacciones.
- Corrección de las rutas utilizadas para localizar los archivos CSV.
- Corrección del formato de `id_trans` para que sea compatible con el tipo `UUID` de PostgreSQL.

### Database
- Creación de las tablas relacionales correspondientes al modelo de RetailMax.
- Implementación de claves primarias y relaciones mediante claves foráneas.
- Carga inicial de datos dummy en PostgreSQL.