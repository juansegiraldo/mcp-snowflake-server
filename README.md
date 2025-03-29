# Servidor MCP para Snowflake

Este servidor implementa el Protocolo de Contexto de Modelo (MCP) para interactuar con bases de datos Snowflake. Permite ejecutar consultas SQL y mantener un registro de insights descubiertos durante el análisis.

## Características

### Recursos

El servidor expone un recurso dinámico:

* `memo://insights`: Un memo de insights de datos que se actualiza continuamente
  * Se actualiza automáticamente cuando se descubren nuevos insights

### Herramientas

El servidor ofrece las siguientes herramientas:

#### Herramientas de Consulta

* `read_query`
  * Ejecuta consultas SELECT para leer datos
  * Entrada: `query` (string)
  * Retorna: Resultados como array de objetos

* `write_query`
  * Ejecuta consultas INSERT, UPDATE o DELETE
  * Entrada: `query` (string)
  * Retorna: `{ affected_rows: number }`

#### Herramientas de Esquema

* `list_tables`
  * Lista todas las tablas en la base de datos
  * No requiere entrada
  * Retorna: Array de nombres de tablas

* `describe_table`
  * Muestra información de columnas de una tabla
  * Entrada: `table_name` (string)
  * Retorna: Array de definiciones de columnas

#### Herramientas de Análisis

* `append_insight`
  * Agrega nuevos insights al recurso memo
  * Entrada: `insight` (string)
  * Retorna: Confirmación de adición
  * Actualiza el recurso memo://insights

## Instalación

```bash
pip install mcp-snowflake-server
```

## Uso

### Línea de Comandos

```bash
mcp_snowflake_server \
  --account TU_CUENTA \
  --warehouse TU_WAREHOUSE \
  --user TU_USUARIO \
  --password TU_CONTRASEÑA \
  --role TU_ROL \
  --database TU_BASE_DE_DATOS \
  --schema TU_ESQUEMA \
  --port 8080
```

### Como Biblioteca

```python
from mcp_snowflake_server import SnowflakeMCPServer

server = SnowflakeMCPServer(
    account="tu_cuenta",
    warehouse="tu_warehouse",
    user="tu_usuario",
    password="tu_contraseña",
    role="tu_rol",
    database="tu_base_de_datos",
    schema="tu_esquema"
)

server.run(port=8080)
```

## Seguridad

* Todas las credenciales se pasan como argumentos de línea de comandos o variables de entorno
* No se almacenan credenciales en archivos
* Se recomienda usar variables de entorno para las credenciales en producción

## Licencia

GPL-3.0