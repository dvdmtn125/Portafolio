# Sabina — Asistente Virtual de Voz

Asistente de voz en español que responde a comandos hablados: abrir páginas web, dar la hora y el día, buscar en Wikipedia e internet, reproducir videos de YouTube, contar chistes y consultar precios de acciones.

Este proyecto fue refactorizado desde un script monolítico hacia **Clean Architecture**, separando la lógica de negocio de los detalles técnicos (síntesis de voz, reconocimiento de voz, APIs externas).

## Arquitectura

El proyecto está dividido en 4 capas, cada una dependiendo solo de la capa inmediatamente inferior:

```
src/
├── domain/
│   └── ports/              # Interfaces (contratos), sin dependencias externas
├── application/
│   └── use_cases/          # Una clase = una acción del asistente
├── infrastructure/         # Implementaciones concretas (pyttsx3, wikipedia, yfinance...)
└── controllers/            # Interpreta comandos de voz y despacha al use case correcto
```

**Regla de dependencia:** las capas internas (`domain`, `application`) nunca conocen las externas (`infrastructure`). Todo se conecta mediante inyección de dependencias en `main.py`, el *composition root* del proyecto.

### Domain — Ports

Contratos abstractos que definen capacidades sin implementarlas:

| Port | Responsabilidad |
|---|---|
| `SpeechRecognizer` | Convertir audio en texto |
| `SpeechSynthesizer` | Convertir texto en voz |
| `KnowledgeSource` | Buscar resúmenes (Wikipedia) |
| `WebSearcher` | Buscar en internet |
| `VideoPlayer` | Reproducir videos |
| `JokeProvider` | Obtener chistes |
| `StockPriceProvider` | Consultar precio de una acción |
| `TickerResolver` | Resolver el ticker bursátil a partir del nombre de una empresa |
| `WebLauncher` | Abrir una URL en el navegador |

### Application — Use Cases

Cada use case orquesta uno o más ports para lograr una acción completa, sin conocer ninguna librería externa: `SaludarInicialmente`, `InformarDiaSemana`, `InformarHora`, `BuscarEnWikipedia`, `BuscarEnInternet`, `ReproducirVideo`, `ContarChiste`, `ConsultarPrecioAccion`, `AbrirPaginaWeb`, `Despedirse`.

### Infrastructure — Adapters

Implementaciones reales de cada port:

| Adapter | Librería |
|---|---|
| `Pyttsx3SpeechSynthesizer` | pyttsx3 |
| `GoogleSpeechRecognizer` | speech_recognition |
| `WikipediaKnowledgeSource` | wikipedia |
| `PywhatkitWebSearcher` | pywhatkit |
| `PywhatkitVideoPlayer` | pywhatkit |
| `PyjokesJokeProvider` | pyjokes |
| `WebbrowserWebLauncher` | webbrowser (librería estándar) |
| `YfinanceStockPriceProvider` | yfinance |
| `YahooTickerResolver` | yfinance (`yf.Search`) |

### Controllers

`AsistenteController` escucha el micrófono en loop, interpreta el texto reconocido y despacha al use case correspondiente. No conoce ningún detalle de infraestructura.

## Requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/) como gestor de paquetes
- Windows (usa rutas de voz de `pyttsx3` específicas de Windows/SAPI5)
- Micrófono funcional

## Dependencias

| Paquete | Versión | Uso |
|---|---|---|
| `pyttsx3` | >=2.99 | Síntesis de voz (texto → audio) |
| `speechrecognition` | >=3.17.0 | Reconocimiento de voz (audio → texto) |
| `pyaudio` | >=0.2.14 | Acceso al micrófono, requerido por `speechrecognition` |
| `wikipedia` | >=1.4.0 | Búsqueda de resúmenes en Wikipedia |
| `pywhatkit` | >=5.4 | Búsqueda en internet y reproducción de video en YouTube |
| `pyjokes` | >=0.8.3 | Generación de chistes |
| `yfinance` | >=1.5.1 | Precio de acciones y resolución de ticker (`yf.Search`) |

> `webbrowser` no aparece en esta lista porque es un módulo de la librería estándar de Python — no se instala, ya viene incluido.

Dependencias de desarrollo (testing):

| Paquete | Uso |
|---|---|
| `pytest` | Framework de testing |
| `pytest-mock` | Fixture `mocker` para crear dobles de prueba |

## Instalación

```powershell
git clone <url-del-repo>
cd Virtual-assistant
uv sync
```

Si necesitas instalar las dependencias desde cero:

```powershell
uv add pyttsx3 speechrecognition pyaudio pywhatkit yfinance pyjokes wikipedia
uv add --dev pytest pytest-mock
```

> **Nota sobre `pyaudio` en Windows:** para Python 3.12 existen wheels precompilados en PyPI, por lo que `uv add pyaudio` debería instalarse sin necesitar un compilador de C++. Si tu versión de Python no tiene wheel disponible, puede fallar la compilación — en ese caso, buscar un wheel precompilado de terceros para tu versión exacta.

## Uso

```powershell
uv run main.py
```

El asistente saluda según la hora del día y queda escuchando. Comandos disponibles:

| Di... | Sabina hace... |
|---|---|
| "abre youtube" | Abre YouTube en el navegador |
| "abre el navegador" | Abre Google en el navegador |
| "qué día es hoy" | Dice el día de la semana |
| "qué hora es" | Dice la hora actual |
| "busca en wikipedia [tema]" | Busca y lee un resumen de Wikipedia |
| "busca en internet [consulta]" | Busca la consulta en Google |
| "reproduce [canción/video]" | Reproduce el video en YouTube |
| "cuéntame un chiste" | Cuenta un chiste |
| "precio de las acciones de [empresa]" | Dice el precio actual de la acción |
| "adiós" | Se despide y termina |

## Tests

El proyecto usa `pytest` + `pytest-mock`. La estrategia de testing es selectiva: se testea a fondo donde hay lógica de negocio real (use cases, controller, y los adapters de infraestructura con ramas condicionales o manejo de errores), y se omiten tests unitarios para adapters triviales de una sola línea que solo delegan a una librería externa.

```powershell
uv run pytest              # correr toda la suite
uv run pytest -v           # modo detallado
uv run pytest -v -s        # además muestra los print()
uv run pytest tests/application/     # solo una capa
```

**Cobertura actual: 34 tests**

- `tests/application/` (16): lógica de cada use case, sin ninguna librería externa real.
- `tests/controllers/` (11): interpretación de comandos y despacho al use case correcto.
- `tests/infrastructure/` (7): `GoogleSpeechRecognizer` (manejo de errores de reconocimiento) y `YahooTickerResolver` (resolución de ticker y manejo de fallos de API).

### `conftest.py`

En la raíz del proyecto (mismo nivel que `pyproject.toml`), resuelve el import de `src/` para pytest:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
```

## Proceso de aprendizaje

Este proyecto se desarrolló con Claude (Anthropic) como mentor de arquitectura: presentando opciones de diseño con sus ventajas y desventajas en cada decisión clave (por ejemplo, cómo resolver el ticker bursátil o qué tanto testear en infrastructure), mientras yo elegía el enfoque y transcribía, ejecutaba y depuraba el código manualmente. Los bugs de transcripción y su diagnóstico a partir de los tracebacks fueron parte activa de ese proceso de aprendizaje.

## Notas técnicas

- La lista de empresas reconocibles para consulta de precios se resuelve dinámicamente contra Yahoo Finance (`yf.Search`) en vez de un diccionario fijo, permitiendo consultar cualquier empresa listada, no solo un conjunto predefinido.
- `speech_recognition` emite `DeprecationWarning` por los módulos `aifc` y `audioop` (parte de la librería estándar, eliminados en Python 3.13). No afecta a Python 3.12; revisar compatibilidad antes de actualizar de versión.