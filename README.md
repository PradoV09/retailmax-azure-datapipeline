# PROYECTO RETAILMAX

## 1. ¿Por qué elegí este escenario?

El **Escenario B — Retail y Comercio Electrónico** refleja un problema que toda cadena de consumo masivo enfrenta diariamente: la falta de visibilidad en tiempo real sobre el inventario, el comportamiento del cliente y las devoluciones.

- Un **quiebre de stock** no detectado a tiempo se traduce directamente en ventas perdidas y clientes que migran a la competencia.
- Una **segmentación de clientes deficiente** hace que las campañas de marketing pierdan efectividad.

Implementar un pipeline que consolide estas fuentes dispersas permite tomar decisiones de reabastecimiento, fidelización y reducción de devoluciones basadas en datos y hechos, no en revisiones manuales ni suposiciones.

## 2. ¿Por qué trabajar con Microsoft Fabric?

Microsoft Fabric es una plataforma unificada de análisis de datos que integra en un solo entorno las capacidades de:

- Ingesta
- Transformación
- Almacenamiento
- Orquestación
- Visualización

Esto ofrece los recursos necesarios para llevar a cabo el **pipeline** que dará solución a los problemas de RetailMax mencionados anteriormente, de forma ordenada y centralizada, evitando tener los recursos dispersos en varios sitios y facilitando el desarrollo e integración de los componentes usados en la solución del escenario.

## 3. Configuración del archivo de generación de datos

Librerías necesarias (instalar antes de ejecutar el script):

```bash
pip install faker
pip install PyYAML
pip install pandas
pip install numpy
```

### 3.1 Base de datos (PostgreSQL con Docker)

Entrar a la carpeta `database` y desde ahí levantar el contenedor:

```bash
cd database
docker compose up -d
```

Configura el usuario, contraseña y nombre de base de datos que se usarán desde el contenedor.

```yaml
services:
  postgres:
    image: postgres:16
    container_name: retailmax-postgres
    restart: unless-stopped

    environment:
      POSTGRES_DB: retailmax
      POSTGRES_USER: retailmax
      POSTGRES_PASSWORD: retailmax123

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```