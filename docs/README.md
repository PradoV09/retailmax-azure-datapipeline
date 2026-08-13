# Entregable Fase 1 — Modelado de Datos y Generación de Datos Sintéticos
**Proyecto:** RetailMax Azure Data Pipeline  
**Autor:** Jose Luis Prado  
**Fecha:** 13 de agosto de 2026

---

## 1. Objetivo de la Fase

Diseñar el modelo entidad-relación (MER) del dominio retail/e-commerce de RetailMax y generar/cargar los datos sintéticos correspondientes en Azure SQL Database, cubriendo las siguientes áreas del negocio:

- Gestión de miembros (CRM)
- Catálogo de artículos y proveedores
- Red de tiendas
- Transacciones de venta y devoluciones (POS)
- Inventario / stock diario

## 2. Modelo Entidad-Relación (MER)

Diagrama general del modelo de datos, mostrando las relaciones entre las entidades maestras (`mstr_*`), transaccionales (`trans_*`, `post_*`), de inventario (`inv_*`) y de CRM (`crm_*`).

![Modelo Entidad-Relación](/docs/ENTREGABLES%20FASE%201/MER.png)

**Notas del modelo:**
- Las tablas `mstr_*` (artículos, proveedores, tiendas) actúan como catálogos maestros.
- `trans_ventas` y `post_devoluciones` conforman el ciclo transaccional de punto de venta.
- `inv_stock_diario` alimenta el control de inventario para las alertas de quiebre de stock.
- `crm_miembros` soporta la segmentación RFM.

## 3. Tablas Cargadas en Azure SQL Database

Evidencia de ejecución en la nube: cada captura corresponde a la tabla ya creada y poblada con datos sintéticos en Azure SQL Database.

### 3.1 Tablas Maestras

**Artículos**
![mstr_articulos](/docs/ENTREGABLES%20FASE%201/mstr_articulos.png)

**Proveedores**
![mstr_proveedores](/docs/ENTREGABLES%20FASE%201/mstr_proveedores.png)

**Tiendas**
![mstr_tiendas](/docs/ENTREGABLES%20FASE%201/mstr_tiendas.png)

### 3.2 CRM

**Miembros**
![crm_miembros](/docs/ENTREGABLES%20FASE%201/crm_miembros.png)

### 3.3 Transaccionales

**Ventas**
![trans_ventas](/docs/ENTREGABLES%20FASE%201/trans_ventas.png)

**Devoluciones (POS)**
![post_devoluciones](/docs/ENTREGABLES%20FASE%201/post_devoluciones.png)

### 3.4 Inventario

**Stock Diario**
![inv_stock_diario](/docs/ENTREGABLES%20FASE%201/inv_stock_diario.png)

## 4. Resumen de Entregables

| # | Entidad | Tipo | Evidencia | Estado |
|---|---------|------|-----------|--------|
| 1 | MER (Modelo de Datos) | Diagrama | `MER.png` | ✅ Completado |
| 2 | mstr_articulos | Tabla maestra | `mstr_articulos.png` | ✅ Cargada en Azure SQL |
| 3 | mstr_proveedores | Tabla maestra | `mstr_proveedores.png` | ✅ Cargada en Azure SQL |
| 4 | mstr_tiendas | Tabla maestra | `mstr_tiendas.png` | ✅ Cargada en Azure SQL |
| 5 | crm_miembros | CRM | `crm_miembros.png` | ✅ Cargada en Azure SQL |
| 6 | trans_ventas | Transaccional | `trans_ventas.png` | ✅ Cargada en Azure SQL |
| 7 | post_devoluciones | Transaccional | `post_devoluciones.png` | ✅ Cargada en Azure SQL |
| 8 | inv_stock_diario | Inventario | `inv_stock_diario.png` | ✅ Cargada en Azure SQL |
