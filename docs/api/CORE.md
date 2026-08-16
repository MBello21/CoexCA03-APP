# Core de la API

Documentación de los archivos base de `coex-api/app/`.

## Archivos

| Archivo | Responsabilidad |
|---------|----------------|
| `main.py` | Instancia de FastAPI, middlewares, registro de routers |
| `database.py` | Conexión a PostgreSQL, sesión de SQLAlchemy, clase base de modelos |
| `config.py` | Configuración centralizada desde variables de entorno |
| `router_global.py` | Router raíz que agrupa todos los routers del proyecto |

## main.py

Punto de entrada de la aplicación. Crea la instancia de FastAPI con los metadatos del proyecto:

- **Título**: Api modular COEXCA03
- **Descripción**: API para el centro de conservación de carreteras de CA-35 y CA-36
- **Versión**: 1.0.0

Configura CORS abierto (todos los orígenes, métodos y headers permitidos) para la fase de desarrollo. Esto debe restringirse antes de producción.

Registra todos los routers bajo el prefijo `/api/v1` a través del router global.

Crea las tablas de la base de datos al arrancar mediante `Base.metadata.create_all()`. Esto es temporal para desarrollo — en producción las migraciones se gestionarán con Alembic.

## database.py

Gestiona la conexión a PostgreSQL con SQLAlchemy.

- **Engine**: conexión a la BD con `pool_pre_ping=True` para detectar conexiones muertas antes de usarlas.
- **SessionLocal**: fábrica de sesiones con `autocommit=False` y `autoflush=False` para control explícito de transacciones.
- **Base**: clase base declarativa de la que heredan todos los modelos.
- **get_db()**: generador que proporciona una sesión por request y la cierra al finalizar. Se usa como dependencia en los routers con `Depends(get_db)`.

## config.py

Carga las variables de entorno desde `.env` usando `pydantic-settings`. Valida tipos automáticamente al instanciar.

### Variables

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `POSTGRES_USER` | str | — | Usuario de PostgreSQL |
| `POSTGRES_PASSWORD` | str | — | Contraseña de PostgreSQL |
| `POSTGRES_DB` | str | — | Nombre de la base de datos |
| `POSTGRES_HOST` | str | localhost | Host del servidor PostgreSQL |
| `POSTGRES_PORT` | int | 5433 | Puerto de PostgreSQL |

La propiedad `DATABASE_URL` construye la cadena de conexión a partir de estas variables con el formato `postgresql://user:password@host:port/db`.

## router_global.py

Router central (`APIRouter`) que actúa como punto de montaje para todos los routers del proyecto. Cada módulo nuevo registrará su router aquí:

```python
from .routers import incidencias, usuarios

api_router.include_router(incidencias.router, prefix="/incidencias", tags=["Incidencias"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
```

Esto mantiene `main.py` limpio — solo monta el router global una vez bajo `/api/v1`.

## Flujo de una petición

```
Cliente → /api/v1/recurso → router_global → router específico → service → DB
                                                      ↑
                                               Depends(get_db)
```