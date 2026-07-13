# Portafolio

Repositorio central de mis proyectos, organizados por lenguaje/tecnología. Cada proyecto vive en su propia carpeta con su propio `README.md` detallando arquitectura, instalación y uso.

## Proyectos

### Python

| Proyecto | Descripción | Stack |
|---|---|---|
| [Virtual Assistant](./python/virtual-assistant) | Asistente virtual de voz en español: comandos por micrófono para abrir páginas web, consultar hora/día, buscar en Wikipedia/internet, reproducir videos, contar chistes y consultar precios de acciones. | pyttsx3, speech_recognition, yfinance, wikipedia, pywhatkit |
| [Asistencia Facial](./python/asistencia-facial) | Sistema de control de asistencia mediante reconocimiento facial. | face_recognition, opencv-python, numpy |
| [Web Scraper](./python/web-scraper) | Scraper de citas (quotes.toscrape.com) con Clean Architecture. | requests, BeautifulSoup |
| [Clima Colombia](./python/clima-colombia) | Pipeline de datos climáticos consumiendo la API de Open-Meteo, con dashboard en Streamlit y CLI. | pandas, requests, Streamlit |
| [Recibo Restaurante](./python/recibo-restaurante) | Aplicación de facturación para restaurante con interfaz de escritorio. | Tkinter |
| [Space Invaders](./python/space-invaders) | Juego estilo Space Invaders con arquitectura modular por capas. | Arcade |

### HTML / CSS / JavaScript

_Próximamente._

## Convenciones de este portafolio

Todos los proyectos de Python siguen los mismos principios:

- **Clean Architecture**: separación en capas domain / application / infrastructure / controllers (o adaptada según el tipo de proyecto), con inyección de dependencias manual en un composition root.
- **Gestión de dependencias con [`uv`](https://docs.astral.sh/uv/)**.
- **Tests con `pytest` + `pytest-mock`**, priorizando cobertura donde hay lógica de negocio real por sobre código "pegamento" trivial.
- **Desarrollo asistido por Claude (Anthropic)** como mentor de arquitectura: cada proyecto documenta este proceso en su propia sección "Proceso de aprendizaje" dentro de su README.

## Estructura del repositorio

```
portafolio/
├── README.md                  # este archivo
├── python/
│   ├── virtual-assistant/
│   ├── asistencia-facial/
│   ├── web-scraper/
│   ├── clima-colombia/
│   ├── recibo-restaurante/
│   └── space-invaders/
└── html-css-js/
    └── ...
