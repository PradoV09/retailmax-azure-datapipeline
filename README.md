# RetailMax Data Platform — End-to-End Data Pipeline

Pipeline de datos end-to-end con arquitectura Medallion (Bronze / Silver / Gold) construido sobre **Microsoft Azure**, desarrollado como solución a la Prueba Técnica de Ingeniero de Datos — *End-to-End Data Pipeline Challenge*.

---

## 1. Declaración inicial

| Decisión | Selección | Justificación |
|---|---|---|
| **Sector / Escenario de negocio** | **Escenario B — Retail y Comercio Electrónico (RetailMax)** | Es el dominio con el que tengo mayor afinidad técnica y de negocio: modelos de inventario, RFM, conversión por canal y análisis de devoluciones son problemas recurrentes en retail donde puedo aportar criterio de diseño sólido en la capa Gold. |
| **Plataforma cloud** | **Microsoft Azure** | Azure ofrece una capa gratuita permanente suficiente para el alcance del ejercicio (Storage, SQL Database, Data Factory, Key Vault), una integración nativa y madura entre Azure Data Factory / Databricks y ADLS Gen2 para implementar Medallion, y un ecosistema de gobierno (Key Vault, Log Analytics, RBAC/Entra ID) alineado con los requisitos de seguridad y auditoría de la Fase 5. |

---

## 2. Contexto del negocio

**RetailMax** es una cadena de retail de consumo masivo con presencia física en Colombia, México, Chile, Perú y Ecuador, operando 148 tiendas (hipermercados, supermercados de barrio y tiendas de conveniencia) junto con un canal de e-commerce propio y presencia en marketplaces regionales. Ventas anuales consolidadas superiores a USD 1.200 millones, catálogo activo de ~48.000 referencias y un programa de fidelización con 7.2 millones de miembros.

### Problemáticas que resuelve esta solución

- **Quiebres de stock:** visibilidad manual de inventario (revisión tres veces por semana) genera ventanas de hasta 48 horas sin control, con pérdidas estimadas de 3% a 8% de ventas en referencias de alta rotación.
- **Segmentación de clientes:** la segmentación actual por frecuencia produce campañas con tasas de apertura inferiores al 12%; se requiere segmentación RFM.
- **Conversión por canal:** no existe medición consolidada de tasa de conversión y ticket promedio por canal y categoría.
- **Devoluciones:** 18.000 devoluciones mensuales sin visibilidad sistemática sobre causas y proveedores problemáticos.
- **Reporting ejecutivo:** ausencia de una vista consolidada y diaria de ventas por país, tienda, canal y categoría.

---

## 3. Arquitectura de la solución

### 3.1 Visión general

```
Sistema transaccional (Azure SQL Database)
            │
            ▼
   ┌─────────────────┐
   │   BRONZE (raw)   │  ADLS Gen2 · Parquet · metadatos de auditoría · particionado año/mes/día
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │  SILVER (clean)  │  Limpieza, tipado, integridad referencial, enmascaramiento PII
   └─────────────────┘
            │
            ▼
   ┌─────────────────┐
   │   GOLD (model)   │  Modelo dimensional · reglas de negocio · KPIs ejecutivos
   └─────────────────┘
            │
            ▼
   Consumo analítico (Power BI / SQL Analytics)
```

### 3.2 Servicios Azure utilizados

| Componente | Servicio Azure | Propósito |
|---|---|---|
| Almacenamiento por capas | Azure Data Lake Storage Gen2 (contenedores `bronze`, `silver`, `gold`) | Repositorio central del lago de datos |
| Base de datos origen | Azure SQL Database | Fuente transaccional sintética de RetailMax |
| Orquestación y transformación | Azure Data Factory (+ Databricks/Spark para transformaciones) | Ingesta, pipelines Medallion, dependencias entre capas |
| Gestión de secretos | Azure Key Vault | Almacenamiento de credenciales y cadenas de conexión |
| Monitoreo | Log Analytics Workspace + Action Group | Logs de ejecución, alertas de fallo y anomalías |
| Gobierno de identidad | Microsoft Entra ID (RBAC) | Roles de Ingeniero de Datos, Analista y Administrador |
| Infraestructura como código | Terraform (con backend remoto en Storage Account) | Aprovisionamiento reproducible de todos los recursos |
| Consumo / visualización | Power BI | Tableros de KPIs sobre la capa Gold |

### 3.3 Modelo de datos (fuente → Gold)

**Tablas origen (sistema transaccional RetailMax):**
`MSTR_ARTICULOS`, `MSTR_PROVEEDORES`, `MSTR_TIENDAS`, `CRM_MIEMBROS`, `TRANS_VENTAS`, `INV_STOCK_DIARIO`, `POST_DEVOLUCIONES`

**Modelo dimensional en Gold:**

| Tabla Gold | Tipo | Origen |
|---|---|---|
| `dim_productos` | Dimensión | MSTR_ARTICULOS + MSTR_PROVEEDORES |
| `dim_tiendas` | Dimensión | MSTR_TIENDAS |
| `dim_clientes` | Dimensión | CRM_MIEMBROS |
| `fact_ventas` | Hechos | TRANS_VENTAS |
| `fact_inventario` | Hechos | INV_STOCK_DIARIO |
| `fact_devoluciones` | Hechos | POST_DEVOLUCIONES + TRANS_VENTAS |
| `fact_rfm_clientes` | Hechos (agregado) | TRANS_VENTAS + CRM_MIEMBROS |

### 3.4 Reglas de negocio implementadas

- **Alerta de quiebre de stock:** `cobertura_dias < 7` y promedio de ventas de los últimos 14 días > 0.
- **Segmentación RFM:** cálculo sobre los últimos 90 días, score 1–5 por quintiles en cada dimensión (Recencia, Frecuencia, Monto) sobre clientes activos (compra en los últimos 180 días); segmento final como concatenación de scores (ej. R5-F4-M5 = *Champions*).
- **Tasa de devolución:** unidades devueltas / unidades vendidas en el mismo periodo, por categoría de nivel 1 y canal de venta.
- **Dashboard ejecutivo:** ventas netas por país y canal, comparativo semana anterior, top 10 artículos por categoría y tasa de descuento promedio.

---

## 4. Estructura del repositorio

```
retailmax-data-platform/
├── infra/                 # Infraestructura como código (Terraform)
│   ├── modules/
│   ├── environments/      # dev/ y prod/
│   └── README.md
├── data-generation/        # Scripts de generación de datos sintéticos + config YAML
├── pipelines/              # Transformaciones Bronze → Silver → Gold
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── orchestration/          # Definición del pipeline/DAG (Azure Data Factory / Airflow)
├── docs/                   # Diagrama ER, diagrama de arquitectura, catálogo de datos
├── tests/                  # Pruebas de calidad de datos
├── README.md
└── CHANGELOG.md
```

---

## 5. Stack técnico

| Capa | Herramienta |
|---|---|
| Generación de datos sintéticos | Python (Faker, NumPy, Pandas) |
| IaC | Terraform |
| Ingesta y orquestación | Azure Data Factory |
| Procesamiento | PySpark (Azure Databricks) |
| Calidad de datos | Great Expectations |
| Formato de almacenamiento | Delta Lake sobre ADLS Gen2 |
| Base de datos relacional origen | Azure SQL Database |
| Control de versiones | Git |
| Visualización | Power BI |

---

## 6. Prerrequisitos

- Cuenta de Azure activa (free tier o Azure for Students)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) autenticado (`az login`)
- Terraform >= 1.5
- Python >= 3.10
- Acceso a un workspace de Databricks o Spark local para pruebas

---

## 7. Seguridad y gobierno de datos

- Ningún secreto o credencial se almacena en el código: todas las cadenas de conexión y claves se gestionan vía **Azure Key Vault**.
- Enmascaramiento/hash aplicado desde la capa Silver sobre campos sensibles (identificadores de cliente, datos de contacto).
- Tres roles diferenciados mediante Entra ID / RBAC: **Ingeniero de Datos** (lectura/escritura en todas las capas), **Analista** (solo lectura sobre Gold) y **Administrador** (control total).
- Auditoría de accesos habilitada vía Log Analytics.

---

## 8. Licencia y confidencialidad

Este repositorio contiene una solución desarrollada exclusivamente con fines de evaluación técnica para el proceso de selección de **DataKnow**. Todos los datos utilizados son sintéticos y no representan información real de ninguna organización.
