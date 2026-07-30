# RetailMax Data Platform

Solución desarrollada para la prueba técnica **End-to-End Data Pipeline Challenge — Ingeniero de Datos**, utilizando **Microsoft Azure** como plataforma cloud y **Terraform** como herramienta de Infraestructura como Código (IaC).

Este README documenta el **sector elegido, la plataforma cloud seleccionada y la justificación de ambas decisiones**, junto con cada recurso implementado hasta el momento y el motivo puntual por el cual fue necesario para esta prueba. Solo se describe lo que realmente está construido; las capas y funcionalidades aún no desarrolladas se listan al final como pendientes.

---

## 1. Sector elegido

Se seleccionó el **Escenario B — Retail y Comercio Electrónico (RetailMax)**.

**Justificación:** el escenario plantea necesidades de negocio concretas (alertas de quiebre de stock, segmentación RFM de clientes, análisis de conversión por canal, seguimiento de devoluciones y un consolidado de ventas ejecutivo) que exigen mover datos desde un sistema transaccional hasta un modelo analítico por medio de una arquitectura Medallion (Bronze, Silver, Gold). Es el tipo de caso que mejor permite demostrar de forma completa las competencias que evalúa la prueba: modelado de datos, IaC, ingesta, transformación y gobierno.

---

## 2. Plataforma cloud elegida

Se eligió **Microsoft Azure**.

**Justificación:**

- Es la plataforma con la que tengo mayor experiencia práctica, lo que reduce el riesgo de errores de configuración dentro del tiempo límite de la prueba (7 días hábiles).
- Terraform tiene soporte oficial de primer nivel para Azure mediante el proveedor `azurerm`, cumpliendo el requisito de IaC de la rúbrica.
- Azure cubre de forma nativa todos los recursos mínimos que pide la rúbrica para esta plataforma: Storage con ADLS Gen2, orquestador (Data Factory), gestor de secretos (Key Vault) y monitoreo (Log Analytics + Action Group), por lo que no fue necesario combinar proveedores.
- Azure SQL Database permite tener la fuente transaccional (origen del pipeline) totalmente administrada, sin gestionar servidores.

---

## 3. Herramienta de IaC elegida

Se utilizó **Terraform**.

**Justificación:** la rúbrica exige provisionar la infraestructura como código y evita la creación manual de recursos desde el portal. Terraform se eligió sobre Bicep porque:

- Permite versionar la infraestructura junto con el resto del repositorio, cumpliendo el requisito de trazabilidad.
- Facilita parametrizar nombres, región y configuración por entorno (`dev` / `prod`) mediante variables, tal como pide la rúbrica de Fase 2.
- Soporta backend remoto (usado aquí sobre un Storage Account de Azure) para no versionar el estado (`terraform.tfstate`) en Git, evitando uno de los errores que la rúbrica penaliza explícitamente.

---

## 4. Recursos implementados y justificación

### Resource Group

**Por qué:** agrupa todos los recursos del proyecto bajo un mismo límite administrativo, facilita el control de costos y permite eliminar el entorno completo si es necesario. Es el contenedor base que exige cualquier despliegue en Azure.

### Storage Account con ADLS Gen2

**Por qué:** la rúbrica pide explícitamente un Storage Account con ADLS Gen2 y contenedores separados por capa. Se habilitó **Hierarchical Namespace** para convertirlo en Data Lake Storage Gen2, ya que este modo es requisito para trabajar con arquitectura Medallion sobre Azure y es compatible con procesamiento distribuido (Spark) en fases posteriores.

### Contenedores `bronze`, `silver` y `gold`

**Por qué:** la rúbrica exige que cada capa de la arquitectura Medallion esté físicamente aislada. Separar los datos crudos, limpios y de negocio en contenedores distintos evita mezclarlos y permite aplicar políticas de acceso y retención diferenciadas por capa en el futuro.

### Azure SQL Database

**Por qué:** la Fase 1 exige cargar los datos sintéticos generados en una base de datos SQL que actúe como fuente del pipeline. Se eligió Azure SQL Database (en lugar de PostgreSQL) porque es un servicio totalmente administrado y se integra de forma nativa con Azure Data Factory para la ingesta de la Fase 3.

### Azure Key Vault

**Por qué:** es un requisito explícito de la rúbrica y de las buenas prácticas de seguridad evaluadas: ninguna credencial, cadena de conexión o secreto puede quedar escrita en el código fuente. Key Vault centraliza esos valores para que el pipeline los consuma de forma segura cuando se implemente la ingesta.

### Log Analytics Workspace

**Por qué:** la rúbrica pide poder monitorear y auditar las ejecuciones del pipeline sin depender del código fuente. Este recurso centraliza los logs de los servicios de Azure para habilitar esa visibilidad en las siguientes fases (Fase 4 y 5).

### Action Group

**Por qué:** la rúbrica exige poder notificar fallos o eventos relevantes del pipeline (alertas de correo o mensajería). El Action Group queda como el mecanismo de notificación al que se engancharán las alertas de ejecución cuando se configure la orquestación completa.

### Azure Data Factory

**Por qué:** es el servicio ETL/ELT administrado de Microsoft y el recomendado para orquestar la integración entre Azure SQL Database y ADLS Gen2. Hasta el momento se creó el recurso y el **pipeline principal** (sin actividades de copia o transformación todavía), como punto de partida sobre el cual se construirán las capas Bronze, Silver y Gold en la siguiente etapa del desarrollo.

---

## 5. Estado actual del proyecto

Completado hasta la fecha:

- **Fase 1:** generación de datos sintéticos y carga en Azure SQL Database.
- **Fase 2:** infraestructura completa aprovisionada con Terraform (backend remoto, Resource Group, Storage Account/ADLS Gen2, contenedores Bronze/Silver/Gold, Azure SQL Database, Key Vault, Log Analytics Workspace y Action Group).
- **Fase 3 (inicio):** creación del recurso Azure Data Factory y del pipeline principal, aún sin actividades de ingesta ni transformación.

Pendiente (no implementado todavía):

- Conexión de Azure SQL Database a Data Factory y copia hacia Bronze.
- Transformaciones de limpieza y conformación en Silver.
- Modelo dimensional, reglas de negocio (RFM, alertas de quiebre, tasa de devoluciones) y KPIs en Gold.
- Orquestación completa con dependencias, reintentos y alertas (Fase 4).
- Roles diferenciados, enmascaramiento de datos sensibles y catálogo de datos (Fase 5).

---

## 6. Tecnologías utilizadas hasta el momento

- Microsoft Azure
- Terraform
- Azure SQL Database
- Azure Storage Account (ADLS Gen2)
- Azure Data Factory
- Azure Key Vault
- Azure Log Analytics
- Azure Monitor Action Group
- Python
- Git