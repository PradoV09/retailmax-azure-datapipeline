# RetailMax Data Platform

Proyecto desarrollado como solución para la prueba técnica **End-to-End Data Pipeline Challenge**, utilizando **Microsoft Azure** y **Terraform** para el aprovisionamiento de la infraestructura.

---

## Escenario seleccionado

Se seleccionó el **Escenario B – Retail y Comercio Electrónico (RetailMax)**.

Este escenario fue elegido porque permite trabajar con información de ventas, clientes, inventarios y devoluciones, lo que hace posible construir un pipeline de datos completo siguiendo una arquitectura de tipo Medallion.

---

## Plataforma Cloud

Se eligió **Microsoft Azure**.

La decisión se tomó porque:

- Es la plataforma cloud con la que tengo mayor experiencia.
- Terraform posee soporte oficial para Azure.
- Azure ofrece servicios administrados para almacenamiento, integración y monitoreo.
- Todos los servicios necesarios para esta prueba pueden integrarse de forma sencilla.

---

## Infraestructura como Código

Para la creación de la infraestructura se utilizó **Terraform**.

Terraform fue seleccionado porque permite:

- Automatizar el despliegue de recursos.
- Versionar la infraestructura junto con el proyecto.
- Reutilizar configuraciones mediante variables.
- Evitar crear recursos manualmente desde el portal de Azure.

También se configuró un **backend remoto** utilizando Azure Storage Account para almacenar el estado de Terraform.

---

## Recursos implementados

### Resource Group

Se creó un Resource Group para agrupar todos los recursos del proyecto en un mismo lugar, facilitando su administración.

### Storage Account

Se creó un Azure Storage Account con **Hierarchical Namespace** habilitado para utilizar **Azure Data Lake Storage Gen2**.

Este servicio será el encargado de almacenar los datos del proyecto.

### Contenedores del Data Lake

Dentro del Storage Account se crearon tres contenedores:

- `bronze`
- `silver`
- `gold`

Estos contenedores representan las tres capas de la arquitectura Medallion y permitirán organizar los datos según su nivel de procesamiento.

### Azure SQL Database

Se creó una base de datos Azure SQL Database que actuará como fuente de datos del pipeline.

Los datos sintéticos generados durante la Fase 1 serán utilizados posteriormente para realizar la ingesta.

### Azure Key Vault

Se creó un Azure Key Vault para almacenar secretos y credenciales del proyecto, de forma que las cadenas de conexión no queden almacenadas dentro del código.

### Log Analytics Workspace

Se implementó un Log Analytics Workspace para centralizar los registros de los recursos de Azure, con el objetivo de facilitar el monitoreo y la revisión de eventos del proyecto.

### Action Group

Se creó un Action Group que permitirá enviar alertas cuando ocurran eventos importantes durante la ejecución del pipeline.

### Azure Data Factory

Se implementó Azure Data Factory como servicio de integración de datos. Hasta el momento se creó el recurso y el pipeline principal, que servirá como base para las siguientes fases del proyecto.

Azure Data Factory fue seleccionado porque:

- Se integra directamente con Azure SQL Database.
- Permite construir pipelines mediante una interfaz gráfica.
- Facilita la automatización de procesos ETL/ELT.
- Es uno de los servicios recomendados por Microsoft para integración de datos.

---

## Estado actual del proyecto

Actualmente se encuentra implementado:

- Generación de datos sintéticos.
- Carga de datos en Azure SQL Database.
- Infraestructura creada mediante Terraform.
- Backend remoto de Terraform.
- Azure Data Lake Storage Gen2.
- Contenedores Bronze, Silver y Gold (vacíos, como estructura base).
- Azure Key Vault.
- Log Analytics Workspace.
- Action Group.
- Azure Data Factory.
- Pipeline principal de Azure Data Factory.

Las actividades correspondientes a la ingesta de datos y las transformaciones Bronze, Silver y Gold se desarrollarán en las siguientes fases del proyecto.

---

## Tecnologías utilizadas

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