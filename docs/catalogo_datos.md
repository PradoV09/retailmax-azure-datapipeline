# Catálogo de Datos - RetailMax Data Platform

## Capa Silver

### dim_productos
| Campo | Tipo | Origen | Sensibilidad | Descripción |
|-------|------|--------|--------------|-------------|
| id_articulo | VARCHAR(12) | MSTR_ARTICULOS | No | Identificador único del artículo |
| nombre_producto | VARCHAR(100) | MSTR_ARTICULOS | No | Nombre descriptivo del producto |
| categoria | VARCHAR(100) | MSTR_ARTICULOS | No | Categoría del producto |
| precio | NUMERIC(10,2) | MSTR_ARTICULOS | No | Precio de lista del producto |
| id_proveedor | VARCHAR(12) | MSTR_PROVEEDORES | No | Identificador del proveedor |
| nombre_proveedor | VARCHAR(100) | MSTR_PROVEEDORES | No | Razón social del proveedor |
| pais | VARCHAR(100) | MSTR_PROVEEDORES | No | País de origen del proveedor |
| calificacion | NUMERIC(2,1) | MSTR_PROVEEDORES | No | Calificación de calidad del proveedor (1-5) |

### dim_tiendas
| Campo | Tipo | Origen | Sensibilidad | Descripción |
|-------|------|--------|--------------|-------------|
| id_tienda | VARCHAR(12) | MSTR_TIENDAS | No | Identificador único de la tienda |
| tipo_tienda | VARCHAR(50) | MSTR_TIENDAS | No | Tipo de tienda (HIPERMERCADO, SUPERMERCADO, CONVENIENCIA) |
| pais | VARCHAR(100) | MSTR_TIENDAS | No | País donde opera la tienda |
| ciudad | VARCHAR(100) | MSTR_TIENDAS | No | Ciudad donde opera la tienda |
| centro_distribucion | VARCHAR(100) | MSTR_TIENDAS | No | Centro de distribución asignado |
| zona_distribucion | VARCHAR(50) | Calculado | No | Zona de distribución (ZONA_NORTE, ZONA_CENTRO, etc.) |

### dim_clientes
| Campo | Tipo | Origen | Sensibilidad | Descripción |
|-------|------|--------|--------------|-------------|
| id_miembro | VARCHAR(12) | CRM_MIEMBROS | **Alta** | Identificador único del miembro (enmascarado en Silver) |
| id_miembro_hash | VARCHAR(16) | Calculado | No | Hash SHA256 del id_miembro para enmascaramiento |
| fec_registro | TIMESTAMP | CRM_MIEMBROS | No | Fecha de registro del miembro |
| antiguedad_dias | INTEGER | Calculado | No | Antigüedad en días desde el registro |
| rango_edad | VARCHAR(100) | CRM_MIEMBROS | No | Rango de edad del cliente |
| genero | VARCHAR(1) | CRM_MIEMBROS | **Media** | Género estandarizado (M, F, NO_INFORMADO) |
| canal_pref | VARCHAR(100) | CRM_MIEMBROS | No | Canal de compra preferido |
| email_hash | VARCHAR(16) | Calculado | **Alta** | Hash SHA256 del email para enmascaramiento |

### fact_ventas
| Campo | Tipo | Origen | Sensibilidad | Descripción |
|-------|------|--------|--------------|-------------|
| id_venta | VARCHAR(12) | TRANS_VENTAS | No | Identificador único de la transacción |
| fecha_hora | TIMESTAMP | TRANS_VENTAS | No | Fecha y hora de la transacción |
| id_miembro | VARCHAR(12) | TRANS_VENTAS | **Media** | Identificador del miembro (ANONIMO si no aplica) |
| id_articulo | VARCHAR(12) | TRANS_VENTAS | No | Identificador del artículo vendido |
| id_tienda | VARCHAR(12) | TRANS_VENTAS | No | Identificador de la tienda |
| canal | VARCHAR(100) | TRANS_VENTAS | No | Canal de venta (tienda, ecommerce, marketplace) |
| tipo_pago | VARCHAR(50) | TRANS_VENTAS | No | Método de pago |
| precio | NUMERIC(12,2) | TRANS_VENTAS | No | Precio unitario de la venta |
| descuento | NUMERIC(5,2) | TRANS_VENTAS | No | Descuento aplicado |
| vr_venta_neto | NUMERIC(12,2) | Calculado | No | Valor neto de la venta (precio - descuento) |
| con_descuento | BOOLEAN | Calculado | No | Indicador de venta con descuento |

### fact_inventario
| Campo | Tipo | Origen | Sensibilidad | Descripción |
|-------|------|--------|--------------|-------------|
| id_tienda | VARCHAR(12) | INV_STOCK_DIARIO | No | Identificador de la tienda |
| id_articulo | VARCHAR(12) | INV_STOCK_DIARIO | No | Identificador del artículo |
| stock_fisico | INTEGER | INV_STOCK_DIARIO | No | Stock físico disponible |
| stock_minimo | INTEGER | INV_STOCK_DIARIO | No | Stock mínimo configurado |
| stock_maximo | INTEGER | INV_STOCK_DIARIO | No | Stock máximo configurado |
| cobertura_dias | NUMERIC(10,2) | Calculado | No | Días de cobertura de inventario |
| alerta_quiebre | BOOLEAN | Calculado | No | Alerta de quiebre de stock (cobertura_dias < 7) |
| diferencia_stock_min | INTEGER | Calculado | No | Diferencia frente al stock mínimo |

### fact_devoluciones
| Campo | Tipo | Origen | Sensibilidad | Descripción |
|-------|------|--------|--------------|-------------|
| id_venta | VARCHAR(12) | POST_DEVOLUCIONES | No | Identificador de la venta original |
| estado | VARCHAR(100) | POST_DEVOLUCIONES | No | Estado de la devolución (aprobada, rechazada, en_proceso) |
| motivo | VARCHAR(100) | POST_DEVOLUCIONES | No | Código del motivo de devolución |
| motivo_descripcion | VARCHAR(100) | Calculado | No | Descripción legible del motivo |
| precio | NUMERIC(12,2) | TRANS_VENTAS | No | Precio original de la venta |

## Capa Gold

### Tablas Dimensionales (Final)

Las tablas dimensionales en Gold son versiones enriquecidas de las tablas Silver con joins adicionales y campos calculados para análisis.

### Tablas de Hechos (Final)

Las tablas de hechos en Gold incluyen campos enriquecidos de dimensiones para optimizar consultas analíticas.

### Tablas de Agregación

#### kpi_ventas_pais_canal
Ventas netas consolidadas por país y canal de venta.

#### kpi_tasa_descuento
Tasa de descuento promedio aplicada por país y canal.

#### kpi_top_10_articulos_categoria
Top 10 artículos por categoría basado en ventas netas.

#### kpi_tasa_devolucion
Tasa de devolución por categoría y canal de venta (unidades devueltas / unidades vendidas).

### fact_rfm_clientes
Segmentación RFM de clientes con scores de Recencia, Frecuencia y Monto.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_miembro | VARCHAR(12) | Identificador del cliente |
| recencia_dias | INTEGER | Días desde la última transacción |
| frecuencia_90dias | INTEGER | Número de transacciones en los últimos 90 días |
| monto_90dias | NUMERIC(12,2) | Valor monetario de transacciones en los últimos 90 días |
| score_r | INTEGER | Score de recencia (1-5, 5 = mejor) |
| score_f | INTEGER | Score de frecuencia (1-5, 5 = mejor) |
| score_m | INTEGER | Score de monto (1-5, 5 = mejor) |
| segmento_rfm | VARCHAR(3) | Segmento concatenado (ej: 545) |
| nombre_segmento | VARCHAR(50) | Nombre del segmento (Champions, Loyal Customers, etc.) |

## Tablas de Errores

### pipeline_errors
Registra errores de integridad referencial detectados durante la transformación Silver.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| table_name | VARCHAR(100) | Tabla donde ocurrió el error |
| error_reason | TEXT | Motivo del error |
| error_timestamp | TIMESTAMP | Fecha y hora del error |
| [campos originales] | - | Campos del registro con error |

## Reportes de Calidad

### quality_report
Reporte generado por la capa Silver con métricas de calidad de datos por tabla.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| tabla | VARCHAR(100) | Nombre de la tabla |
| registros_originales | INTEGER | Cantidad de registros en Bronze |
| registros_transformados | INTEGER | Cantidad de registros en Silver |
| registros_rechazados | INTEGER | Cantidad de registros rechazados |
| tasa_rechazo_pct | NUMERIC(5,2) | Porcentaje de rechazo |
| porcentaje_conforme_pct | NUMERIC(5,2) | Porcentaje de registros conformes |
| porcentaje_nulos_por_columna | JSON | Porcentaje de nulos por columna |

## Linaje de Datos

### linaje_datos
Documentación de linaje para campos calculados en la capa Gold.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| campo_calculado | VARCHAR(100) | Nombre del campo calculado |
| tabla_origen | VARCHAR(100) | Tabla de origen |
| transformaciones | TEXT | Transformaciones aplicadas en orden |
| proposito | TEXT | Propósito del campo calculado |
