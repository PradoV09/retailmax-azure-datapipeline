# Infraestructura - RetailMax Data Platform

Este directorio contiene la infraestructura necesaria para ejecutar el entorno local de base de datos mediante Docker y desplegar recursos cloud utilizando Terraform sobre Microsoft Azure.

La infraestructura está organizada separando:

- Infraestructura local (`docker`)
- Infraestructura cloud (`terraform`)
- Scripts de carga y preparación de datos

---

# Estructura del proyecto

```
infra/
│
├── docker/
│   ├── docker-compose.yml
│   │
│   ├── init/
│   │   └── schema.sql
│   │
│   └── scripts/
│       ├── load_bd.ipynb
│       └── requirements.txt
│
├── environments/
│   └── dev/
│       ├── main.tf
│       ├── providers.tf
│       ├── variables.tf
│       ├── dev.tfvars
│       ├── prod.tfvars
│       ├── keyvault.tf
│       ├── log_analytics.tf
│       ├── terraform.tfvars
│       └── terraform.tfstate
│
└── README.md
```

---

# 1. Infraestructura local con Docker

La carpeta `docker` contiene la configuración necesaria para ejecutar PostgreSQL localmente.

## Servicios disponibles

Actualmente se utiliza:

- PostgreSQL 16
- Base de datos RetailMax
- Inicialización automática mediante scripts SQL

Archivo principal:

```
docker/docker-compose.yml
```

---

# Levantar PostgreSQL

Desde la carpeta:

```bash
cd infra/docker
```

Ejecutar:

```bash
docker compose up -d
```

Verificar contenedor:

```bash
docker ps
```

Detener servicios:

```bash
docker compose down
```

---

# Inicialización de base de datos

El archivo:

```
docker/init/schema.sql
```

contiene:

- Creación de tablas
- Llaves primarias
- Llaves foráneas
- Restricciones
- Estructura inicial del modelo relacional

Este archivo se ejecuta automáticamente al crear el contenedor PostgreSQL.

---

# Carga de datos

Los scripts de carga se encuentran en:

```
docker/scripts/
```

Contenido:

```
load_bd.ipynb
requirements.txt
```

El notebook realiza:

- Lectura de archivos fuente
- Transformación de datos
- Conexión con PostgreSQL
- Inserción de información en las tablas

---

# Instalación de dependencias

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno:

Windows:

```powershell
.\venv\Scripts\activate
```

Instalar paquetes:

```bash
pip install -r requirements.txt
```

Ejecutar notebook:

```bash
jupyter notebook
```

---

# 2. Infraestructura Cloud con Terraform

La carpeta:

```
environments/dev
```

contiene la infraestructura como código para Microsoft Azure.

Terraform permite crear, modificar y administrar recursos cloud de manera reproducible mediante archivos de configuración.

---

# Recursos administrados

Actualmente Terraform administra los siguientes componentes:

## Resource Group

Archivo:

```
main.tf
```

Responsable de crear el grupo lógico donde se alojan los recursos del ambiente.

---

## Azure Key Vault

Archivo:

```
keyvault.tf
```

Gestiona:

- Almacenamiento seguro de secretos
- Credenciales
- Configuraciones sensibles
- Información protegida de aplicaciones

---

## Log Analytics Workspace

Archivo:

```
log_analytics.tf
```

Permite:

- Recolección de logs
- Monitoreo
- Diagnóstico
- Análisis operativo de recursos Azure

---

# Lista de recursos creados

Los recursos desplegados mediante Terraform corresponden al ambiente de desarrollo (`dev`).

| Recurso | Nombre | Región | Propósito |
|---|---|---|---|
| Resource Group | `rg-retailmax-dev` | East US | Agrupar y administrar todos los recursos asociados a la plataforma RetailMax |
| Azure Key Vault | `kv-retailmax-dev` | East US | Gestión segura de secretos, credenciales y configuraciones sensibles |
| Log Analytics Workspace | `law-retailmax-dev` | East US | Centralización de logs, monitoreo y análisis de actividad de los recursos Azure |
| Storage Account | `stretailmaxdev` | East US | Almacenamiento de información utilizada por los procesos de datos |

---

# Detalle de recursos

## Resource Group

**Nombre:**

```
rg-retailmax-dev
```

**Región:**

```
East US
```

**Propósito:**

Contenedor principal de Azure encargado de organizar los recursos relacionados con el ambiente de desarrollo de RetailMax.

---

## Azure Key Vault

**Nombre:**

```
kv-retailmax-dev
```

**Región:**

```
East US
```

**Propósito:**

Proteger información sensible como secretos, claves y configuraciones utilizadas por los servicios desplegados.

---

## Log Analytics Workspace

**Nombre:**

```
law-retailmax-dev
```

**Región:**

```
East US
```

**Propósito:**

Permitir la supervisión de recursos mediante almacenamiento y análisis de registros generados por Azure.

---

## Storage Account

**Nombre:**

```
stretailmaxdev
```

**Región:**

```
East US
```

**Propósito:**

Proporcionar almacenamiento para archivos, datos procesados y componentes utilizados dentro del flujo de datos.

---

# Configuración Terraform

Archivos principales:

---

## providers.tf

Define el proveedor utilizado:

```
azurerm
```

Permite la comunicación entre Terraform y Microsoft Azure.

---

## variables.tf

Contiene variables reutilizables:

- Nombre de recursos
- Ubicación
- Configuración general
- Parámetros del ambiente

---

## dev.tfvars

Archivo con valores específicos para desarrollo.

Ejemplo:

```
environment = "dev"
```

---

## prod.tfvars

Archivo preparado para configuraciones del ambiente productivo.

---

# Inicializar Terraform

Ubicación:

```bash
cd infra/environments/dev
```

Inicializar proveedores:

```bash
terraform init
```

---

# Validar configuración

Ejecutar:

```bash
terraform validate
```

Resultado esperado:

```
Success! The configuration is valid.
```

---

# Revisar cambios

Antes de crear o modificar recursos:

```bash
terraform plan
```

Este comando muestra los cambios que Terraform aplicará en Azure.

---

# Aplicar infraestructura

Crear recursos:

```bash
terraform apply
```

Confirmar ejecución:

```
yes
```

---

# Destruir infraestructura

Eliminar recursos creados por Terraform:

```bash
terraform destroy
```

---

# Estado Terraform

Terraform mantiene el estado actual de la infraestructura en:

```
terraform.tfstate
```

Este archivo almacena la relación entre:

- Código Terraform
- Recursos existentes en Azure

Debe mantenerse protegido y no debe publicarse en repositorios públicos.

---

# Ambientes

Actualmente está configurado:

```
environments/
│
└── dev/
```

La estructura permite manejar diferentes ambientes:

```
dev
qa
prod
```

utilizando archivos independientes:

```
*.tfvars
```

---

# Requisitos

## Software necesario

- Docker
- Docker Compose
- Python 3.x
- Terraform >= 1.x
- Azure CLI
- Cuenta activa de Microsoft Azure

---

# Configuración Azure CLI

Antes de ejecutar Terraform:

```bash
az login
```

Verificar suscripción:

```bash
az account show
```

Cambiar suscripción:

```bash
az account set --subscription <subscription_id>
```

---

# Buenas prácticas aplicadas

- Separación entre infraestructura local y cloud
- Infraestructura como código utilizando Terraform
- Configuración por ambientes
- Gestión segura mediante Azure Key Vault
- Automatización de despliegues
- Versionamiento mediante Git
- Configuración reproducible

---

# Autor

Jose Luis Prado Valencia

Proyecto:

**RetailMax Data Platform Infrastructure**