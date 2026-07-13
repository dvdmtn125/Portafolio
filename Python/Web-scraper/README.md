# Web Scraper

Scraper de citas (sitio de práctica [quotes.toscrape.com](https://quotes.toscrape.com))
construido con **Clean Architecture** y gestionado con **[uv](https://docs.astral.sh/uv/)**.

## Estructura

```
web-scraper/
├── pyproject.toml          # Dependencias y configuración del proyecto (uv)
├── uv.lock                 # Lockfile con versiones exactas (NO editar a mano)
├── .python-version         # Versión de Python fijada para el proyecto
├── main.py                 # Composition root: conecta capas + CLI
├── domain/
│   ├── __init__.py
│   └── entities.py         # Quote (entidad pura)
├── application/
│   ├── __init__.py
│   ├── interfaces.py       # Puertos: QuoteScraperPort, QuoteRepositoryPort
│   └── use_cases.py        # ScrapeQuotesUseCase
├── infrastructure/
│   ├── __init__.py
│   ├── scraper.py          # BeautifulSoupQuoteScraper
│   └── repository.py       # CsvQuoteRepository, JsonQuoteRepository
└── tests/
    └── test_scraper.py     # Test del parser con HTML de ejemplo (sin red)
```

La regla de dependencia va siempre **hacia adentro**:

```
infrastructure  →  application  →  domain
```

`domain` y `application` no importan nada de `infrastructure`. Es al revés:
`infrastructure` implementa las interfaces (`*Port`) que `application` define.

## Sobre este layout

Este proyecto es un **"virtual project"** de `uv`: no se empaqueta ni se
instala a sí mismo en el entorno (no hay `[project.scripts]` ni build
backend). `uv` solo se usa para resolver e instalar las dependencias
(`requests`, `beautifulsoup4`, `pytest`) en un `.venv` local.

Los imports como `from domain.entities import Quote` funcionan porque:
- Al ejecutar `python main.py`, Python agrega automáticamente el directorio
  del script (la raíz del proyecto) a `sys.path`.
- Al ejecutar `pytest`, la opción `pythonpath = ["."]` en `pyproject.toml`
  agrega la raíz del proyecto a `sys.path` antes de correr los tests.

## Setup

```bash
# Instala dependencias (runtime + dev) y crea/actualiza el .venv
uv sync
```

## Uso

```bash
# Scraping básico (5 páginas, salida CSV)
uv run python main.py

# Especificar número de páginas y formato
uv run python main.py --pages 3 --format json

# Ruta de salida personalizada
uv run python main.py --pages 10 --format csv --output output/mis_citas.csv

# Cambiar el delay entre requests (buenas prácticas / no saturar el servidor)
uv run python main.py --delay 1.5
```

## Tests

```bash
uv run pytest -v
```

## Gestión de dependencias

```bash
# Agregar una dependencia de runtime
uv add nombre-paquete

# Agregar una dependencia solo de desarrollo (tests, linters, etc.)
uv add --dev nombre-paquete

# Quitar una dependencia
uv remove nombre-paquete

# Actualizar el lockfile sin instalar
uv lock

# Ver el árbol de dependencias resueltas
uv tree
```

## Cómo extender este proyecto

- **Otro sitio web**: crea una nueva clase en `infrastructure/` que implemente
  `QuoteScraperPort` (o un nuevo puerto si el dominio cambia).
- **Otra forma de guardar datos**: crea una clase que implemente
  `QuoteRepositoryPort` (ej. `PostgresQuoteRepository`, `MongoQuoteRepository`).
- **Reintentos / rate limiting más robusto**: agrégalo dentro de
  `BeautifulSoupQuoteScraper`, sin afectar el resto del código.

## Buenas prácticas incluidas

- User-Agent realista (estilo Chrome) y delay configurable entre requests.
- Manejo de errores de red sin romper toda la ejecución.
- Logging estructurado en vez de `print`.
- Separación estricta de responsabilidades (testeable y mantenible).
- Gestión de dependencias reproducible vía `uv.lock`.

## Proceso de aprendizaje

Este proyecto se desarrolló con Claude (Anthropic) como mentor de arquitectura:
presentando las decisiones de diseño con sus ventajas y desventajas, mientras
yo elegía el enfoque y transcribía, ejecutaba y depuraba el código manualmente.
Los bugs de transcripción y su diagnóstico a partir de los tracebacks fueron
parte activa del proceso de aprendizaje.

Los errores encontrados durante el desarrollo cubrieron distintas categorías:
typos en nombres de métodos (`_parse_quote` vs `_parse_quotes`, `DicWriter` vs
`DictWriter`), errores de lógica (`>=` en vez de `<=` en el bucle de paginación),
inconsistencias en nombres de atributos (`self.session` vs `self._session`),
firmas de métodos incorrectas (`sefl` en vez de `self`) y desajustes entre la
interfaz abstracta y su implementación (`save_quotes` vs `save`). Cada uno se
diagnosticó leyendo el traceback de PowerShell e identificando la causa raíz
antes de corregirlo.

El mayor aprendizaje técnico fue entender cómo la regla de dependencia de Clean
Architecture (`infrastructure → application → domain`) permite cambiar el formato
de salida (CSV, JSON) o la librería de scraping sin tocar la lógica de negocio,
y cómo los puertos (`*Port`) son el mecanismo concreto que hace posible esa
separación.

> Nota: este scraper apunta a un sitio público creado específicamente para
> practicar (quotes.toscrape.com). Si adaptas esto a otro sitio, revisa
> siempre su `robots.txt` y términos de uso antes de scrapearlo.