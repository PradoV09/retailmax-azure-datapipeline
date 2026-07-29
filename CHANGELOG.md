# CHANGELOG

Todas las entradas siguen el formato: `YYYY-MM-DD — Autor — Descripción`.

## [Sin publicar]

### Día 1
- 2026-07-24 — Jose Luis Prado Valencia — Inicialización del repositorio.
- 2026-07-24 — Jose Luis Prado Valencia — Creación del README con la descripción y planificación del proyecto.
- 2026-07-24 — Jose Luis Prado Valencia — Incorporación del archivo `requirements.txt` con las dependencias iniciales.
- 2026-07-24 — Jose Luis Prado Valencia — Adición del archivo `CHANGELOG.md` para el seguimiento de cambios.
- 2026-07-24 — Jose Luis Prado Valencia — Incorporación del documento `Prueba_tecnica_Escenario_B_Retail.md` con la definición del escenario de la prueba técnica.
- 2026-07-24 — Jose Luis Prado Valencia — Eliminación del archivo `requirements.txt` para seguir la estructura del proyecto.

### Día 2
- 2026-07-25 — Jose Luis Prado Valencia — Adición del archivo `config.yaml` que contiene la configuración del faker.

### Día 3
- 2026-07-26 — Jose Luis Prado Valencia — Adición del archivo `generate_retailmax_data.ipynb` para generar datos sinteticos realistas para el caso RetailMax.
- 2026-07-26 — Jose Luis Prado Valencia — Incorporación del archivo `requirements.txt` con las dependencias iniciales para el arhivo `generate_retailmax_data.ipynb`.
- 2026-07-26 — Jose Luis Prado Valencia — Modificación del archivo `config.yaml` que contiene la configuración del faker.

### Día 4
- 2026-07-27 — Jose Luis Prado Valencia — Modificación del archivo `generate_retailmax_data.ipynb` agregue los dataframe de las tablas.
- 2026-07-27 — Jose Luis Prado Valencia — Modificación del archivo `config.yaml` que contiene la configuración del faker.
- 2026-07-27 — Jose Luis Prado Valencia — Modificación del archivo `generate_retailmax_data.ipynb` guarda los dataframe en los tipos de archivos usados (csv y json).

### Día 5
- 2026-07-28 — Jose Luis Prado Valencia — Modificación del archivo `generate_retailmax_data.ipynb` cambie algunas tablas para las relaciones.
- 2026-07-28 — Jose Luis Prado Valencia — Adición del archivo `load_bd.ipynb` que contiene la carga de datos sintéticos en PostgreSQL.
- 2026-07-28 — Jose Luis Prado Valencia — Adición del archivo `schema.sql` que contiene el codigo sql de la base de datos.
- 2026-07-28 — Jose Luis Prado Valencia — Creada la infraestructura como código.

### Día 6
- 2026-07-29 — Jose Luis Prado Valencia — Adicción del archivo `keyvault.tf` que contiene el Azure Key Vault.
- 2026-07-29 — Jose Luis Prado Valencia — Adicción del archivo `variables.tf` que contiene los secretos (variables de entorno).
- 2026-07-29 — Jose Luis Prado Valencia — Adicción del archivo `log_analystics.tf` que contiene los secretos (variables de entorno).
- 2026-07-29 — Jose Luis Prado Valencia — Modificación del archivo `variables.tf` que contiene los secretos (variables de entorno).
- 2026-07-29 — Jose Luis Prado Valencia — Readme de documentacion con las capturas `README.md`.
- 2026-07-29 — Jose Luis Prado Valencia — Readme de documentacion con las capturas `README.md`.
- 2026-07-29 — Jose Luis Prado Valencia — Modificación de `load_bd.ipynb`.
- 2026-07-29 — Jose Luis Prado Valencia — Adicción del modulo azure_sql.tf.
- 2026-07-29 — Jose Luis Prado Valencia — Modificación de `silver_layer.ipynb`.
- 2026-07-29 — Jose Luis Prado Valencia — Implementación completa de la capa Silver con limpieza, validación de integridad referencial, enmascaramiento de PII y reporte de calidad de datos.
- 2026-07-29 — Jose Luis Prado Valencia — Implementación completa de la capa Gold con reglas de negocio del Escenario B, cálculo RFM y tablas de agregación para KPIs ejecutivos.
- 2026-07-29 — Jose Luis Prado Valencia — Creación del notebook `gold_layer.ipynb` con transformaciones finales y documentación de linaje de datos.
- 2026-07-29 — Jose Luis Prado Valencia — Creación del catálogo de datos en `docs/catalogo_datos.md` con documentación de todas las tablas Silver y Gold.
- 2026-07-29 — Jose Luis Prado Valencia — Simplificación de notebooks Silver y Gold Layer para hacer los procesos más fáciles de ejecutar y entender.
- 2026-07-29 — Jose Luis Prado Valencia — Completación de Fase 2: Creación de módulo Action Group para Azure Monitor, integración en entorno dev, outputs completos en entorno dev, y estructura completa de entorno prod reutilizando módulos existentes.
- 2026-07-29 — Jose Luis Prado Valencia — Completación de Fase 3: Agregado particionamiento año/mes/día en Bronze, carga incremental sencilla, log de ejecución, tabla de errores del pipeline, idempotencia con overwrite=True, y reporte de ejecución.
