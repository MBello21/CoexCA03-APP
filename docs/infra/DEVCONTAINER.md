# Entorno de desarrollo — Dev Container

Documentación de la configuración del entorno de desarrollo containerizado del proyecto COEX.

Ubicación: `.devcontainer/`

## Archivos

| Archivo | Función |
|---------|---------|
| `devcontainer.json` | Configuración principal de VS Code Dev Containers |
| `Dockerfile` | Imagen base del contenedor de desarrollo |
| `docker-compose.yml` | Orquestación de servicios (app + base de datos) |

## Dockerfile

Imagen base: `mcr.microsoft.com/devcontainers/python:3.14`

Incluye:

- Python 3.14 con `pipenv` como gestor de dependencias
- Cliente PostgreSQL (`postgresql-client`) para acceso directo a la BD desde terminal
- `PYTHONUNBUFFERED=1` para que los logs de Python salgan en tiempo real

## docker-compose.yml

### Servicio `app`

Contenedor principal de desarrollo. Monta el workspace y se mantiene activo con `sleep infinity` para que VS Code se conecte por SSH.

- **Build**: usa el Dockerfile del `.devcontainer/` con contexto en la raíz del proyecto
- **Volumen**: monta `../..` en `/workspaces` (acceso a todo el monorepo)
- **Red**: comparte red con el servicio `db` vía `network_mode: "service:db"`, lo que permite conectar a PostgreSQL usando `localhost` sin exponer puertos entre contenedores

### Servicio `db`

PostgreSQL 17 como base de datos de desarrollo.

- **Volumen**: `postgres-data` para persistencia entre reinicios del contenedor
- **Variables de entorno**: cargadas desde `.env` en la raíz del proyecto
- **Puerto**: `5432` expuesto al host

### Variables de entorno esperadas en `.env`

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

## devcontainer.json

### Features instaladas

- **Node LTS** (`ghcr.io/devcontainers/features/node:1`) — necesario para el frontend React + Vite

### Puertos reenviados

| Puerto | Uso previsto |
|--------|-------------|
| 3000 | Frontend Vite |
| 3001 | Reservado |

### Comando de inicialización (`onCreateCommand`)

Se ejecuta una sola vez al crear el contenedor. Actualmente:

1. Copia `.env.example` a `.env`
2. Ejecuta `pipenv install` (dependencias Python del backend)
3. Ejecuta `database.sh` (script de inicialización de la BD)

Cada paso tiene fallback con `|| echo "... failed"` para que el contenedor arranque aunque alguno falle.

> ⚠️ Pendiente: añadir instalación de dependencias del frontend (`npm install` o similar dentro de `coex-dashboard/`) cuando el proyecto esté scaffoldeado.

### Extensiones de VS Code

| Extensión | Función |
|-----------|---------|
| `esbenp.prettier-vscode` | Formateo automático de código frontend |
| `ms-python.autopep8` | Formateo automático de código Python |

### Usuario

El contenedor opera como usuario `vscode` (no root).