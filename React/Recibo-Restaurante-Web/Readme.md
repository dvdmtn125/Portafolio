# Recibo Restaurante — Web

Migración full-stack de [Recibo-Restaurante](../../python/Recibo-Restaurante) (aplicación de escritorio en Tkinter) a una arquitectura web moderna con **FastAPI** en el backend y **React + TypeScript** en el frontend.

El proyecto original calculaba cuentas de restaurante con una interfaz de escritorio. Esta versión conserva toda la lógica de negocio original (cálculo de subtotales, IVA y generación de recibos) migrada a **Clean Architecture**, y la expone como una API REST consumida por una aplicación web con gestión completa de productos y categorías.

## Arquitectura

El backend sigue el mismo patrón de cuatro capas usado en el resto de mi portafolio de Python:

```
domain/          → Entidades y reglas de negocio puras, sin dependencias externas
application/     → Casos de uso, interfaces de repositorios, excepciones de negocio
infrastructure/  → Implementaciones concretas (SQLAlchemy + SQLite)
controllers/     → Routers de FastAPI, schemas de Pydantic (DTOs)
```

La regla que sostiene todo: `domain/` no sabe que existen FastAPI, SQLAlchemy, ni HTTP. Cada capa solo conoce a la que tiene inmediatamente debajo, conectadas mediante inyección de dependencias (`composicion.py` como composition root).

**Decisión de diseño clave:** las categorías de productos se modelaron como una entidad propia con relación real a `productos` (foreign key + regla de integridad: no se puede eliminar una categoría con productos asociados), en vez de una lista fija de valores — la app original tenía categorías fijas (comida/bebida/postres); esta versión las hace completamente dinámicas y editables desde la interfaz.

## Stack técnico

**Backend**
- FastAPI + Uvicorn
- SQLAlchemy 2.0 (ORM) + SQLite
- Pydantic (validación y schemas)
- pytest + pytest-mock (41 tests: dominio, aplicación con mocks, infraestructura contra SQLite real, endpoints end-to-end)
- `uv` como gestor de paquetes

**Frontend**
- React + TypeScript (Vite)
- Tailwind CSS v4
- Context API para estado compartido entre componentes
- Vitest + React Testing Library (14 tests)

## Funcionalidades

- **Categorías**: crear, listar y eliminar (con protección ante categorías que tienen productos asociados)
- **Productos**: CRUD completo (crear, listar, editar, eliminar), asociados a una categoría
- **Facturación**: armado de pedido por categoría → producto → cantidad, cálculo de subtotal/IVA/total, y generación de un recibo de texto formateado
- Validación de reglas de negocio de punta a punta (frontend → API → dominio), con manejo de errores HTTP semánticamente correctos (400 para datos inválidos, 404 para recursos inexistentes, 409 para conflictos de integridad)

## Cómo correr el proyecto

### Backend

```powershell
cd Backend
uv sync
uv run uvicorn recibo_restaurante.main:app --reload
```

La API queda disponible en `http://localhost:8000`, con documentación interactiva en `http://localhost:8000/docs`.

### Frontend

```powershell
cd Frontend
npm install
npm run dev
```

La aplicación queda disponible en `http://localhost:5173`.

### Tests

```powershell
# Backend
cd Backend
uv run pytest -v

# Frontend
cd Frontend
npm test -- --run
```

## Estructura del repositorio

```
Recibo-Restaurante-Web/
├── Backend/
│   ├── src/recibo_restaurante/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   ├── controllers/
│   │   ├── composicion.py
│   │   └── main.py
│   └── tests/
└── Frontend/
    └── src/
        ├── api/          # Cliente HTTP, tipos TypeScript, funciones por recurso
        ├── assets/
        ├── context/      # DatosContext: estado compartido de categorías y productos
        ├── features/     # Componentes de cada dominio (categorias, productos, facturacion)
        └── tests/        # Configuración de Vitest (setup.ts)
```

## Nota sobre el uso de IA

Este proyecto fue desarrollado con la asistencia de Claude (Anthropic) como herramienta de aprendizaje y mentoría técnica. Cada archivo fue transcrito manualmente por mí como método deliberado de estudio — no copiado y pegado — como forma de interiorizar los patrones de arquitectura, detectar errores propios mediante tracebacks reales, y entender el razonamiento detrás de cada decisión de diseño (por ejemplo, por qué separar interfaces de implementaciones, o cómo manejar inyección de dependencias en FastAPI). Todo el código fue revisado, probado y corregido de forma iterativa hasta confirmar su funcionamiento real, no solo su apariencia correcta.