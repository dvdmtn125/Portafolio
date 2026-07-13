# Clima Colombia

Proyecto de analisis de datos climaticos de ciudades colombianas, construido con Clean Architecture. Consume la API publica de [Open-Meteo](https://open-meteo.com/) (sin necesidad de API key) para obtener clima actual e historico de cualquier ciudad del pais, con interfaz de linea de comandos y un dashboard interactivo en Streamlit.

## Caracteristicas

- Busqueda dinamica de ciudades colombianas por nombre (geocoding, sin catalogo fijo)
- Consulta de clima actual (temperatura, precipitacion, humedad)
- Consulta de historial climatico por rango de fechas
- Interfaz de linea de comandos (CLI)
- Dashboard interactivo con graficos (Streamlit)
- 44 tests automatizados con pytest, incluyendo mocks de llamadas HTTP
- Arquitectura limpia (Clean Architecture) con 4 capas independientes

## Arquitectura

El proyecto sigue los principios de Clean Architecture, separando responsabilidades en capas independientes:

src/
??? domain/              # Entidades e interfaces del negocio (sin dependencias externas)
?   ??? entities.py       # City, WeatherRecord
?   ??? repositories.py   # Interfaces abstractas (WeatherRepository, CityRepository)
??? application/          # Casos de uso: orquestan reglas de negocio
?   ??? use_cases/
?       ??? fetch_weather.py
??? infrastructure/        # Implementaciones concretas de las interfaces del dominio
?   ??? open_meteo_client.py         # Consume la API de clima de Open-Meteo
?   ??? geocoding_city_repository.py # Consume la API de geocoding de Open-Meteo
??? interface/             # Puntos de entrada de la aplicacion
??? cli.py             # Interfaz de linea de comandos
??? dashboard.py        # Dashboard interactivo con Streamlit

La regla de dependencia se cumple en una sola direccion: `interface` depende de `application`, que depende de `domain`. La capa `infrastructure` implementa las interfaces definidas en `domain`, pero `domain` nunca sabe que `infrastructure` existe. Esto permite testear la logica de negocio con implementaciones falsas (fakes/mocks), sin hacer llamadas reales a ninguna API.

## Stack tecnologico

- **Python 3.12**
- **uv** ? gestor de dependencias y entornos virtuales
- **requests** ? cliente HTTP para consumir la API de Open-Meteo
- **pandas** ? procesamiento de datos (usado en el dashboard)
- **Streamlit** ? dashboard interactivo
- **pytest** + **pytest-mock** + **pytest-cov** ? testing

## Instalacion

Clona el repositorio e instala las dependencias con `uv`:

```bash
git clone https://github.com/tu-usuario/clima-colombia.git
cd clima-colombia
uv sync
```

## Uso

### CLI

Consultar el clima actual de una ciudad:

```bash
uv run python main.py actual --ciudad Medellin
```

Consultar el historial climatico en un rango de fechas:

```bash
uv run python main.py historial --ciudad Bogota --desde 2026-06-01 --hasta 2026-06-07
```

### Dashboard interactivo

```bash
uv run streamlit run src/interface/dashboard.py
```

Esto abre el dashboard en `http://localhost:8501`, donde puedes buscar cualquier ciudad colombiana, ver su clima actual en tarjetas de metricas, y explorar el historial climatico con graficos interactivos.

## Testing

Correr toda la suite de tests:

```bash
uv run pytest -v
```

Correr tests con reporte de cobertura:

```bash
uv run pytest --cov=src --cov-report=term-missing
```

Correr tests de una capa especifica:

```bash
uv run pytest tests/domain/ -v
uv run pytest tests/application/ -v
uv run pytest tests/infrastructure/ -v
uv run pytest tests/interface/ -v
```

Todos los tests de `infrastructure` e `interface` usan `pytest-mock` para simular respuestas HTTP, por lo que la suite completa corre sin necesidad de conexion a internet.

## Decisiones de diseno

- **Geocoding dinamico en vez de catalogo fijo**: en lugar de limitar la busqueda a una lista predefinida de ciudades, el proyecto consulta la API de geocoding de Open-Meteo en tiempo real, filtrando resultados por Colombia (`country=CO`). Esto permite buscar cualquier ciudad o municipio del pais sin mantener una lista manual.
- **Inyeccion de dependencias por constructor**: los casos de uso reciben sus dependencias (repositorios) en el constructor, nunca las crean internamente. Esto es lo que permite testear la logica de negocio con implementaciones falsas.
- **Entidades inmutables**: `City` y `WeatherRecord` usan `dataclass(frozen=True)`, validando sus propios datos en `__post_init__` para proteger las invariantes del dominio.
- **Sin build-system en pyproject.toml**: el proyecto usa el patron `uv init --no-package`, evitando la complejidad de empaquetar el proyecto como una libreria distribuible, ya que no es el objetivo de este portafolio.

## Proceso de aprendizaje

Este proyecto se desarrolló con Claude (Anthropic) como mentor de arquitectura: presentando opciones de diseño con sus ventajas y desventajas en cada decisión clave, mientras yo elegía el enfoque y transcribía, ejecutaba y depuraba el código manualmente. Los bugs de transcripción y su diagnóstico a partir de los tracebacks fueron parte activa de ese proceso de aprendizaje. Un desafío particular fue resolver problemas de encoding en Windows/PowerShell al crear archivos con acentos y caracteres especiales del español — la solución consistió en usar heredocs de PowerShell (`@'...'@`) junto con `Set-Content -Encoding ASCII` como método confiable de creación de archivos.

## Notas tecnicas y aprendizajes

Durante el desarrollo se encontro un caso limite no documentado explicitamente en la API de Open-Meteo: el endpoint de geocoding (`/v1/search`) no soporta un parametro `country` para filtrar resultados por pais en la consulta misma. Aunque intuitivamente parece un parametro valido, la API lo ignora silenciosamente y devuelve resultados de cualquier pais ordenados por relevancia/poblacion.

Esto se detecto al buscar ciudades como "Madrid" o "Pekin": la API devolvia Madrid (España) o Pekin (China) antes que cualquier resultado colombiano real, ya que son ciudades mucho mas pobladas que sus homonimos colombianos (existe un municipio "Madrid" en Cundinamarca).

La solucion fue filtrar los resultados del lado del cliente, usando el campo `country_code` que la API si devuelve en cada resultado:

```python
colombian_results = [
    r for r in results if r.get("country_code") == "CO"
]
```

Esto quedo cubierto con tests especificos (`test_filtra_resultados_de_otros_paises`, `test_retorna_none_si_ningun_resultado_es_de_colombia`) que documentan el comportamiento esperado y previenen regresiones futuras.
## Autor

David ? [tu perfil de GitHub o LinkedIn aqui]

