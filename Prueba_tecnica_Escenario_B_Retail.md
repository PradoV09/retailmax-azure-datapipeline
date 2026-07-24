# PRUEBA TÉCNICA DE CONOCIMIENTO
**Perfil:** Ingeniero de Datos
**End-to-End Data Pipeline Challenge**

| | |
|---|---|
| **Duración estimada** | 7 días hábiles |
| **Modalidad** | Individual — Repositorio Git + presentación |
| **Plataformas válidas** | Microsoft Azure, Amazon AWS, Google Cloud Platform, Microsoft Fabric |
| **Herramientas IaC** | Terraform, Bicep, AWS CloudFormation, Google Deployment Manager, UI (ver rúbrica) |
| **Entrega** | Repositorio Git compartido + evidencias de ejecución + README completo |

---

## INTRODUCCIÓN

Esta prueba técnica está diseñada para evaluar las competencias end-to-end de un Ingeniero de Datos moderno. El candidato deberá demostrar habilidades en diseño de arquitecturas de datos, generación de datos sintéticos, infraestructura como código, construcción de pipelines de ingesta y transformación, orquestación de flujos de trabajo y gobierno de datos.

La prueba simula un escenario real de negocio. El candidato tomará decisiones técnicas justificadas en cada etapa, desde la infraestructura hasta la capa de consumo analítico. No existe una única solución correcta; se valora la coherencia técnica, la documentación de supuestos y la calidad del razonamiento.

### ¿Qué se evalúa?
- Capacidad de leer un requisito de negocio y diseñar un modelo de datos acorde
- Decisiones de arquitectura en la nube: plataforma, servicios y patrones de diseño
- Dominio de herramientas de Infraestructura como Código (IaC)
- Construcción de pipelines con arquitectura Medallón: Bronze, Silver y Gold
- Orquestación de flujos de trabajo y manejo de dependencias entre tareas
- Aplicación de seguridad, roles, permisos y notificaciones operacionales
- Calidad del código, documentación técnica y claridad en la presentación de la solución

### Reglas generales
El candidato tiene libertad de elección en plataforma cloud, herramientas de IaC y motor de procesamiento. Cada decisión debe quedar documentada y justificada en el README del repositorio. La plataforma elegida debe ser consistente a lo largo de toda la solución.

**Sector seleccionado: Escenario B — Retail y Comercio Electrónico.**

El tiempo máximo de entrega es de **siete (7) días hábiles** contados desde la recepción del documento original. Ante cualquier duda de interpretación, el candidato debe documentar el supuesto adoptado y continuar con el desarrollo.

---

## ESCENARIO B — RETAIL Y COMERCIO ELECTRÓNICO

### Contexto del negocio

RetailMax es una cadena de retail de consumo masivo fundada en 1998 con presencia física en Colombia, México, Chile, Perú y Ecuador. Opera 148 tiendas distribuidas entre hipermercados, supermercados de barrio y tiendas de conveniencia, y desde 2019 cuenta con un canal de e-commerce propio y presencia en los principales marketplaces de la región. Sus ventas anuales consolidadas superan los USD 1.200 millones con un crecimiento del canal digital del 34% en el último año fiscal.

El catálogo activo contiene aproximadamente 48.000 referencias de producto agrupadas en seis macro categorías: Alimentos y bebidas, Cuidado personal e higiene, Hogar y limpieza, Electrónica y tecnología, Ropa y calzado básico, y Bebés y maternidad. El reabastecimiento opera desde tres centros de distribución regionales en Bogotá, Ciudad de México y Santiago de Chile, con frecuencia de despacho a tienda de uno a tres días según la velocidad de rotación de cada categoría.

El área de Supply Chain estima que un quiebre de stock en una referencia de alta rotación genera una pérdida de entre el 3% y el 8% de las ventas proyectadas, con riesgo adicional de migración del cliente al competidor. Hoy el equipo revisa inventarios tres veces por semana de forma manual, dejando ventanas de hasta 48 horas sin visibilidad. El área de Marketing necesita segmentar los 7.2 millones de miembros del programa de fidelización usando RFM, ya que la segmentación actual por frecuencia produce campañas con tasas de apertura inferiores al 12%. El área de Devoluciones gestiona 18.000 devoluciones mensuales sin visibilidad sistemática sobre causas ni proveedores problemáticos.

### Necesidades del negocio
- Identificar diariamente referencias con riesgo de quiebre en los próximos siete días considerando stock actual, velocidad de consumo de los últimos catorce días y tiempo de reabastecimiento desde el centro de distribución.
- Calcular el score RFM de cada cliente del programa de fidelización con actualización semanal para segmentar en al menos cinco grupos de valor.
- Calcular la tasa de conversión por canal y por categoría: cuántos clientes que visitaron el sitio o tienda efectivamente compraron y cuál es el ticket promedio por canal.
- Analizar devoluciones por motivo, categoría, proveedor y canal para identificar patrones que permitan reducir la tasa mediante acciones preventivas.
- Construir una vista de ventas diarias consolidada por país, tienda, canal y categoría para el dashboard ejecutivo de la dirección comercial.

### Fuente de datos (tablas de origen)

Estas son las estructuras de las tablas que existen en el sistema transaccional de RetailMax. Los nombres reflejan la nomenclatura interna del sistema legado. El candidato debe generar datos sintéticos con estas estructuras y estos nombres exactos.

| Tabla en la fuente | Campos principales | Volumen mínimo |
|---|---|---|
| MSTR_ARTICULOS | art_id, cod_barra, desc_art, id_categ_n1, id_categ_n2, id_categ_n3, id_proveedor, precio_lista, peso_kg, unid_medida, activo, fec_alta | 5.000 registros |
| MSTR_PROVEEDORES | id_proveedor, razon_social, pais_origen, tiempo_repo_dias, calificacion_calidad, activo | 800 registros |
| MSTR_TIENDAS | id_tienda, nom_tienda, tipo_tienda, id_ciudad, id_pais, metros_cuadrados, activo, fec_apertura | 150 registros |
| CRM_MIEMBROS | id_miembro, fec_registro, id_ciudad, genero, rango_edad, canal_pref, activo, fec_ultima_compra | 50.000 registros |
| TRANS_VENTAS | id_trans, id_miembro, id_tienda, art_id, fec_trans, hra_trans, qty_vendida, precio_unitario_venta, descuento_aplicado, tipo_pago, canal_venta | 1.000.000 registros |
| INV_STOCK_DIARIO | id_snapshot, art_id, id_tienda, fec_snapshot, stock_fisico, stock_transito, stock_reservado, stock_minimo_config, stock_maximo_config | 750.000 registros |
| POST_DEVOLUCIONES | id_devolucion, id_trans_origen, art_id, id_tienda, fec_devolucion, qty_devuelta, motivo_cod, canal_devolucion, estado_devolucion, vr_reembolso | 50.000 registros |

### Procesamiento zona de bronze y silver: limpieza y preprocesamiento

En la zona silver se debe garantizar una correcta estructuración, limpieza, mapeo y enriquecimiento del dato que se ingestó en la fase anterior (MSTR_ARTICULOS, TRANS_VENTAS, MSTR_PROVEEDORES, INV_STOCK_DIARIO, POST_DEVOLUCIONES, MSTR_TIENDAS, CRM_MIEMBROS) usando los formatos adecuados para procesamiento de big data, además se debe garantizar seguridad de la información utilizando mecanismo de encriptación y/o enmascaramiento de la data sensible como número de documentos, valores de estado de cuenta, etc.

### Procesamiento zona Gold: creación de dim y fact con lógicas de negocio

La capa Gold debe contener un modelo dimensional limpio. Las siguientes tablas destino son dimensiones (dim) o tablas de hechos (fact) que el candidato construye a partir de las fuentes anteriores de acuerdo con las lógicas de negocio requeridas.

| Tabla fuente (origen) | Tabla destino en Gold | Transformaciones clave en Silver y Gold |
|---|---|---|
| MSTR_ARTICULOS + MSTR_PROVEEDORES | dim_productos | Join por id_proveedor; construir jerarquía de categorías (nivel 1, 2 y 3) como campos planos; calcular margen estimado por categoría |
| MSTR_TIENDAS | dim_tiendas | Estandarizar tipo_tienda a catálogo controlado; enriquecer con ciudad y país; calcular zona de distribución asignada |
| CRM_MIEMBROS | dim_clientes | Calcular antigüedad en días desde fec_registro; imputar rango_edad nulo con la mediana del canal preferido; estandarizar género a M, F o No informado |
| TRANS_VENTAS | fact_ventas | Calcular vr_venta_neto = qty_vendida x precio_unitario - descuento; validar id_miembro contra dim_clientes o asignar cliente anónimo; agregar indicador de venta con descuento |
| INV_STOCK_DIARIO | fact_inventario | Calcular cobertura_dias = stock_fisico / promedio_consumo_14dias; flag alerta_quiebre cuando cobertura_dias sea menor a 7; calcular diferencia frente a stock_minimo_config |
| POST_DEVOLUCIONES + TRANS_VENTAS | fact_devoluciones | Join con la venta origen para obtener precio original; estandarizar motivo_cod a descripción legible; calcular tasa_devolucion por artículo y categoría |
| TRANS_VENTAS + CRM_MIEMBROS (agregado) | fact_rfm_clientes | Calcular R como días desde última transacción, F como número de transacciones en 90 días, M como valor monetario en 90 días; asignar score 1 a 5 por quintiles y construir segmento RFM |

### Reglas de negocio para la capa Gold

- El score RFM se calcula sobre los últimos 90 días. Cada dimensión recibe un puntaje de 1 a 5 usando quintiles sobre todos los clientes activos (al menos una compra en 180 días). El segmento final se construye concatenando los tres scores, por ejemplo, R5-F4-M5 = Champions.
- Una referencia entra en alerta de quiebre cuando cobertura_dias sea menor a 7 Y el promedio de ventas de los últimos 14 días sea mayor a cero. Referencias sin ventas en 14 días no generan alerta.
- La tasa de devolución por categoría se calcula como unidades devueltas sobre unidades vendidas en el mismo periodo, expresada en porcentaje, por categoría de nivel 1 y por canal de venta.
- El dashboard ejecutivo consolida diariamente: ventas netas por país y canal, comparativo versus el mismo día de la semana anterior, top 10 de artículos por categoría y tasa de descuento promedio aplicada.

---

## ENTREGABLE FASE 1 — GENERACIÓN DE DATOS Y MODELO RELACIONAL

Una vez seleccionado el sector, el candidato debe generar los datos sintéticos utilizando el lenguaje y la librería de su preferencia. Se recomienda Python, PySpark, aunque también son válidos R, Scala o cualquier generador SQL. El script de generación debe ser reproducible mediante una semilla aleatoria fija.

### Requisitos de los datos generados
- **Distribuciones realistas:** los datos no deben ser completamente aleatorios. Por ejemplo, las ventas deben concentrarse en horarios pico, las edades deben seguir una distribución normal, y los montos de transacciones deben reflejar comportamientos típicos del sector.
- **Integridad referencial:** todos los identificadores presentes en las tablas de hechos deben existir en las tablas de dimensiones correspondientes.
- **Valores nulos controlados:** incluir aproximadamente un 5% de valores nulos en campos no críticos para simular condiciones reales de calidad de datos.
- **Cobertura temporal:** los datos deben cubrir al menos doce meses de histórico con distribución uniforme o estacional según el sector.
- **Anomalías intencionales:** incluir al menos tres patrones de datos anómalos documentados, como transacciones duplicadas, fechas fuera de rango o registros con campos inconsistentes. El pipeline deberá detectarlos o manejarlos de forma explícita.
- **Múltiples formatos de salida:** generar los datos en al menos dos formatos distintos entre CSV, JSON y Parquet para simular un escenario de ingesta heterogénea.

### Carga en base de datos relacional

Los datos sintéticos deben ser cargados en una base de datos SQL que actúe como fuente origen del pipeline.

| Plataforma | Motores recomendados | Alternativa local |
|---|---|---|
| Microsoft Azure | Azure SQL Database, Azure Database for PostgreSQL | SQL Server Express o PostgreSQL en Docker |
| Amazon AWS | Amazon RDS (PostgreSQL, MySQL o SQL Server) | PostgreSQL en Docker o SQLite para pruebas locales |
| Google Cloud | Cloud SQL (PostgreSQL o MySQL) | PostgreSQL en Docker |
| Microsoft Fabric | SQL Analytics Endpoint del Lakehouse o Warehouse | PostgreSQL local para la generación inicial |

Los scripts de generación y carga de datos deben estar versionados en el repositorio Git y ser completamente reproducibles. El candidato debe incluir un archivo de configuración en formato YAML o JSON que centralice los parámetros de generación: volumen por tabla, rango de fechas y semilla aleatoria.

**Entregables Fase 1:**
- Script de generación de datos dummy con semilla aleatoria fija y parámetros configurables
- Script SQL o Python de carga en la base de datos relacional seleccionada
- Diagrama Entidad-Relación (ER) de todas las tablas generadas, ubicado en la carpeta `/docs` del repositorio
- Evidencia de la carga exitosa: captura de pantalla o resultado de `SELECT COUNT(*)` por tabla

---

## ENTREGABLE FASE 2 — INFRAESTRUCTURA COMO CÓDIGO

El candidato debe aprovisionar todos los recursos de nube necesarios para la solución utilizando una herramienta de Infraestructura como Código. La elección de la herramienta debe ser coherente con la plataforma seleccionada y debe quedar justificada en el README.

### Recursos mínimos requeridos por plataforma

| Plataforma | Recursos mínimos a aprovisionar |
|---|---|
| Microsoft Azure | Resource Group, Storage Account con ADLS Gen2 y contenedores bronze/silver/gold, Azure Data Factory o Databricks Workspace, Azure Key Vault, Log Analytics Workspace y Action Group para alertas |
| Amazon AWS | S3 Buckets separados para bronze, silver y gold, AWS Glue Database con Crawlers, roles IAM con política de mínimo privilegio, CloudWatch Log Groups, SNS Topic para notificaciones y AWS Secrets Manager |
| Google Cloud | GCS Buckets para bronze, silver y gold, BigQuery Dataset, Cloud Composer Environment, Service Accounts con roles granulares, Cloud Logging, Pub/Sub Topic para alertas y Secret Manager |
| Microsoft Fabric | Workspace con capacidad trial o F2, Lakehouse con estructura bronze/silver/gold en OneLake, Data Factory de Fabric y configuración de alertas por email o Microsoft Teams |

### Estándares obligatorios del código IaC
- Ningún valor de credencial, contraseña o clave de acceso debe aparecer directamente en el código. Todos los secretos deben referenciarse desde el gestor de secretos de la plataforma.
- Las variables de nombre de recursos, región, entorno y tamaño de instancias deben estar parametrizadas y documentadas.
- El estado de Terraform debe almacenarse en un backend remoto: Storage Account en Azure, S3 en AWS o GCS en Google Cloud. No se debe confirmar el archivo de estado en el repositorio.
- La configuración debe soportar al menos dos entornos distintos mediante workspaces o archivos de variables separados: por ejemplo, dev y prod.
- Los outputs del módulo deben exportar los ARNs, URLs o nombres de todos los recursos creados para que puedan ser consumidos por los scripts del pipeline.

**Entregables Fase 2:**
- Código IaC completo en la carpeta `/infra` del repositorio, con README de instrucciones de despliegue
- Evidencia del despliegue exitoso: captura de pantalla del portal o salida del terminal con el resultado del apply
- Lista de recursos creados con sus nombres, regiones y propósito dentro de la solución
- Archivo de variables o parámetros separado del código principal, sin credenciales expuestas

---

## ENTREGABLE FASE 3 — PIPELINE END TO END: ARQUITECTURA MEDALLION

Esta es la fase central de la prueba. El candidato debe construir un pipeline de datos que mueva la información a través de tres capas de calidad creciente aplicando transformaciones progresivas. La arquitectura debe ser idiomática: cada capa tiene un propósito claro y los datos no deben saltarse niveles.

### Capa Bronze — Ingesta de datos crudos
- Ingestar los datos desde la base de datos SQL origen hacia el almacenamiento en la nube en formato Parquet o Delta Lake
- Mantener el esquema original de la fuente sin modificaciones
- Agregar tres columnas de metadatos de auditoría: marca de tiempo de ingesta, sistema fuente e identificador del lote de procesamiento
- Implementar particionamiento por fecha de ingesta con estructura año/mes/día
- Registrar un log de cada ejecución de ingesta con número de registros procesados, tamaño del archivo y duración total
- La ingesta debe soportar modo incremental: en ejecuciones posteriores a la inicial, procesar únicamente los registros nuevos o modificados

### Capa Silver — Limpieza y conformación
- Eliminar registros duplicados exactos y registros con campos obligatorios nulos o corrompidos
- Estandarizar tipos de datos
- Validar la integridad referencial entre tablas de hechos y dimensiones: registros con identificador inexistente van a una tabla de errores con el motivo documentado
- Aplicar una estrategia documentada para el manejo de valores nulos en cada columna
- Aplicar enmascaramiento o hash sobre columnas con información de identificación personal
- Generar un reporte de calidad de datos por cada ejecución: % de nulos por columna, número de registros rechazados y % de registros conformes

### Capa Gold — Modelo analítico y reglas de negocio
- Implementar todas las reglas de negocio del Escenario B (ver sección anterior)
- Construir al menos tres tablas o vistas de agregación diferentes que respondan a las necesidades de negocio descritas
- Optimizar las tablas de Gold para consultas: particionamiento por las dimensiones de análisis más frecuentes y, si la plataforma lo soporta, clustering o indexación
- Documentar el linaje de datos de al menos tres campos calculados: tabla de origen, transformación aplicada y propósito del campo
- Construir al menos una tabla de KPIs ejecutivos

### Consideraciones técnicas transversales
- **Idempotencia:** el pipeline debe poder ejecutarse múltiples veces sobre los mismos datos sin generar duplicados ni alterar el resultado final
- **Manejo de errores:** cualquier excepción debe capturarse, registrarse en una tabla de errores y notificarse sin interrumpir la ejecución de tareas independientes
- **Pruebas de calidad de datos:** implementar al menos cinco verificaciones automatizadas (Great Expectations, pruebas de dbt o validaciones personalizadas)

**Entregables Fase 3:**
- Código completo de las tres capas del pipeline en la carpeta `/pipelines` del repositorio
- Tabla de errores del pipeline con al menos un registro de prueba
- Reporte de calidad de datos generado por la capa Silver
- Al menos tres tablas o vistas de agregación en la capa Gold con sus definiciones documentadas
- Resultados de las cinco pruebas de calidad de datos con reporte de aprobación o fallo

---

## ENTREGABLE FASE 4 — ORQUESTACIÓN DEL PIPELINE

Todos los pasos del pipeline deben estar orquestados mediante una herramienta formal de gestión de flujos de trabajo, coherente con la plataforma cloud seleccionada.

### Opciones de orquestación por plataforma

| Plataforma | Herramientas de orquestación válidas |
|---|---|
| Microsoft Azure | Azure Data Factory Pipelines, Databricks Workflows, Apache Airflow en Azure Kubernetes Service |
| Amazon AWS | Amazon Managed Workflows for Apache Airflow (MWAA), AWS Step Functions, AWS Glue Workflows |
| Google Cloud | Cloud Composer (Apache Airflow), Cloud Workflows, Cloud Scheduler + Cloud Run |
| Microsoft Fabric | Fabric Pipelines, Spark Notebooks con programación integrada |

### Requisitos del orquestador
- Definir un DAG o pipeline principal con dependencias explícitas entre tareas: Silver solo inicia cuando Bronze completó exitosamente, y Gold solo cuando Silver completó exitosamente
- Configurar una ejecución programada automática diaria a las 02:00 horas del huso horario local del proyecto
- Implementar reintentos automáticos: al menos tres intentos por tarea fallida con backoff exponencial
- Definir un tiempo máximo de ejecución por tarea coherente con el volumen de datos procesado
- Configurar alerta de correo o mensaje en canal de comunicación cuando cualquier tarea falle (nombre del DAG, tarea, fecha/hora y mensaje de error)
- Configurar reporte de resumen diario automático al completarse el pipeline con éxito (registros procesados por capa, tiempo total, número de alertas de calidad)
- El estado de cada ejecución debe ser visible en un dashboard o log de monitoreo accesible sin acceder al código fuente

### Flujo de ejecución esperado
```
Trigger — Programado o Manual
  ↓
Extracción desde la base de datos origen
  ↓
Carga en capa Bronze con validación de volúmenes
  ↓
Transformación Silver — limpieza, validación y calidad
  ↓
Transformación Gold — reglas de negocio y agregaciones
  ↓
Verificaciones de calidad de datos sobre la capa Gold
  ↓
Notificación de resultado — éxito o fallo con detalle
```

**Entregables Fase 4:**
- Definición del DAG o pipeline principal en la carpeta `/orchestration` del repositorio
- Captura de pantalla del DAG ejecutado exitosamente con el estado de cada tarea visible
- Evidencia de la alerta de fallo: captura del correo o mensaje ante una ejecución fallida de prueba
- Evidencia del reporte diario de éxito: captura del correo o mensaje de resumen
- Acceso al dashboard o log de monitoreo con el historial de al menos dos ejecuciones

---

## ENTREGABLE FASE 5 — GOBIERNO, SEGURIDAD Y CALIDAD

### Gestión de roles y accesos
- Definir e implementar al menos tres roles diferenciados: Ingeniero de Datos (lectura/escritura en todas las capas), Analista (solo lectura en capa Gold), Administrador (control total)
- Aplicar principio de mínimo privilegio: cada componente ejecuta bajo su propia identidad de servicio
- Ninguna credencial debe aparecer en código fuente, archivos de configuración o variables no cifradas
- Habilitar registros de auditoría de accesos a los datos

### Privacidad y protección de datos sensibles
- Identificar y etiquetar todas las columnas con información de identificación personal en las tablas de origen
- Aplicar enmascaramiento dinámico o función hash sobre columnas sensibles a partir de la capa Silver; los datos originales no deben ser accesibles para el perfil Analista
- Mantener un catálogo de datos básico que liste cada tabla de las capas Silver y Gold con descripción de cada campo, tipo, origen y sensibilidad

### Notificaciones y monitoreo operacional
- Alerta de fallo del pipeline: notificación inmediata con nombre de la tarea, capa afectada, hora y mensaje de error completo
- Reporte diario de ejecución: resumen automático con registros procesados por capa, tiempo de ejecución y registros rechazados por calidad
- Alerta de anomalía de volumen: si el número de registros difiere más de 30% respecto al promedio de las últimas siete ejecuciones, enviar alerta diferenciada antes de continuar

### Linaje y documentación de datos
- Documentar el linaje de al menos tres campos calculados en la capa Gold: tabla de origen, transformaciones aplicadas en orden, propósito del campo
- Mantener un `CHANGELOG.md` con cada cambio significativo (fecha, autor, descripción)

**Entregables Fase 5:**
- Definición de los tres roles implementados con evidencia de configuración en la plataforma
- Demostración del acceso denegado: evidencia de que el perfil Analista no puede acceder a Bronze o Silver directamente
- Catálogo de datos básico en formato Markdown en la carpeta `/docs`
- Evidencia del funcionamiento de las tres alertas: fallo, reporte diario y anomalías de volumen
- `CHANGELOG.md` con el historial de cambios del proyecto

---

## RECOMENDACIONES TÉCNICAS Y PROCESO DE ENTREGA

### Elementos que elevan la calidad de la solución
- **Delta Lake o Apache Iceberg:** formato de tabla ACID sobre Parquet para Silver y Gold (versionado, upserts, viajes en el tiempo)
- **dbt (Data Build Tool):** documentación automática, pruebas declarativas y linaje con mínimo esfuerzo
- **Great Expectations o Soda Core:** expectativas de calidad de datos como código, versionadas y ejecutadas como parte del pipeline
- **OpenLineage o Apache Atlas:** linaje de datos automático y centralizado
- **CI/CD del pipeline:** GitHub Actions o Azure DevOps para validar código, ejecutar pruebas y desplegar cambios automáticamente

### Errores frecuentes que se penalizan en la evaluación
- Credenciales, tokens o contraseñas en el código fuente o historial de commits
- Estado de Terraform confirmado en el repositorio (`terraform.tfstate` nunca debe aparecer en el historial de Git)
- Pipeline sin idempotencia (duplicados al ejecutar dos veces)
- README sin instrucciones reproducibles
- Decisiones técnicas sin justificación

### Estructura de carpetas recomendada para el repositorio

| Carpeta o archivo | Contenido esperado |
|---|---|
| `/infra` | Código IaC completo con README de instrucciones de despliegue |
| `/data-generation` | Scripts de generación de datos dummy y archivo de configuración |
| `/pipelines` | Código de transformaciones para las tres capas del pipeline |
| `/orchestration` | Definición del DAG o pipeline del orquestador elegido |
| `/docs` | Diagrama de arquitectura, catálogo de datos y diagrama ER |
| `README.md` | Descripción completa de la solución, justificaciones y guía de despliegue e imágenes |
| `CHANGELOG.md` | Historial de cambios con fecha, autor y descripción por entrada |

### Proceso de entrega
1. Crear un repositorio Git en GitHub, GitLab o Bitbucket y compartirlo con el evaluador antes de la fecha límite
2. Incluir en el README como primera sección el sector elegido (Retail y Comercio Electrónico), la plataforma cloud seleccionada y la justificación de ambas decisiones
