# Asistencia Facial

Sistema de control de asistencia mediante reconocimiento facial. Detecta el rostro de un empleado a través de la cámara web, lo compara contra una base de datos de fotos conocidas y registra el ingreso con hora exacta en un archivo CSV.

Incluye también un modo de comparación 1 a 1, útil como demo independiente del algoritmo de reconocimiento facial sin necesidad de cámara ni base de empleados.

## Características

- Reconocimiento facial en tiempo real desde webcam.
- Comparación contra una base de datos de fotos de empleados.
- Registro automático de ingresos con marca de hora en `data/files/registro.csv`.
- Evita duplicar el registro de una misma persona en la misma sesión.
- Modo demo de comparación entre dos fotos puntuales (sin webcam).
- CLI con subcomandos (`asistencia` / `comparar`).

## Estructura del proyecto

```
asistencia-facial/
├── data/
│   ├── empleados/        # Fotos de referencia de cada empleado (una cara por foto)
│   ├── files/
│   │   └── registro.csv  # Salida generada: registro de ingresos
│   └── img/               # Fotos de prueba para el modo "comparar"
├── src/
│   ├── empleados.py       # Carga y codificación de las fotos de empleados
│   ├── registro.py        # Registro de ingresos en el CSV
│   ├── camara.py          # Apertura de cámara y utilidades de reconocimiento
│   └── comparar.py        # Comparación 1 a 1 entre dos fotos (demo)
├── tests/
│   ├── test_camara.py      # Tests de buscar_coincidencia() y dibujar_etiqueta()
│   └── test_registro.py    # Tests de registrar_acesso()
├── main.py                # Punto de entrada del CLI
├── pyproject.toml
└── README.md
```

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) para gestión de dependencias
- Una cámara web (solo necesaria para el modo `asistencia`)
- Git instalado (necesario para resolver la dependencia `face-recognition-models`)

## Instalación

```bash
git clone <url-del-repositorio>
cd asistencia-facial
uv sync
```

`uv sync` instala todas las dependencias declaradas en `pyproject.toml`, incluida `face-recognition-models` desde su repositorio en GitHub.

### Nota técnica: por qué se fija `setuptools<82`

`face-recognition-models` depende internamente de `pkg_resources` para ubicar los archivos de modelos pre-entrenados (`.dat`). A partir de la versión 82 de `setuptools` (febrero de 2026), `pkg_resources` fue eliminado por completo del paquete, lo que rompe esta dependencia con un error de `ModuleNotFoundError`.

Como `face-recognition-models` no se ha actualizado desde 2017 y no migró a las alternativas modernas (`importlib.resources` / `importlib.metadata`), la solución mientras tanto es fijar una versión de `setuptools` anterior a la 82:

```toml
dependencies = [
    "setuptools<82",
]
```

Si en el futuro `face-recognition-models` se actualiza (o se reemplaza por una alternativa mantenida), esta restricción puede eliminarse.

## Preparar los datos

1. Coloca una foto por empleado en `data/empleados/`, nombrada con el nombre de la persona (por ejemplo `David Muneton.jpg`). El nombre del archivo, sin la extensión, se usa como el nombre mostrado al reconocer a la persona.
2. Cada foto debe contener una sola cara claramente visible.
3. Para el modo `comparar`, coloca las fotos de prueba en `data/img/`.

## Uso

### Modo asistencia (reconocimiento en vivo con webcam)

```bash
uv run python main.py asistencia
```

El programa:
1. Carga y codifica las fotos de `data/empleados/`.
2. Toma una imagen de la cámara web.
3. Compara la(s) cara(s) detectada(s) contra la base de empleados.
4. Si encuentra una coincidencia (distancia ≤ 0.6), dibuja un recuadro con el nombre y registra el ingreso en `data/files/registro.csv`.
5. Si no encuentra coincidencia, lo indica en consola sin registrar nada.

### Modo comparar (demo de comparación entre dos fotos)

```bash
uv run python main.py comparar FotoA.jpg FotoB.jpg
```

Carga ambas fotos desde `data/img/`, detecta la cara principal de cada una, las compara y muestra el resultado (`True`/`False` y la distancia calculada) superpuesto en la imagen de prueba.

## Cómo funciona el reconocimiento

El proyecto usa la librería [`face_recognition`](https://github.com/ageitgey/face_recognition), que internamente representa cada rostro como un vector de 128 medidas faciales (codificación). Dos rostros se consideran la misma persona si la distancia euclidiana entre sus codificaciones es menor o igual a un umbral (por defecto `0.6`); a menor distancia, mayor similitud.

## Limitaciones conocidas

- El reconocimiento funciona mejor con buena iluminación y una sola cara por foto de referencia.
- Si una foto en `data/empleados/` no contiene una cara detectable, la codificación de esa foto fallará.
- El umbral de distancia (`0.6`) es un valor general; en escenarios con muchos empleados similares puede requerir ajuste.

## Tests

El proyecto incluye tests automatizados con [`pytest`](https://docs.pytest.org/), enfocados en la lógica pura del sistema (búsqueda de coincidencias, dibujo de etiquetas y registro de ingresos). Quedan fuera de los tests automáticos las funciones que dependen de hardware real (captura de webcam) o que abren ventanas interactivas (`cv2.imshow`), ya que no son adecuadas para correr sin una cámara o entorno gráfico disponible.

### Instalación

`pytest` está declarado como dependencia de desarrollo en `pyproject.toml` (grupo `dev`), por lo que ya se instala junto con el resto del proyecto al correr `uv sync`. Si necesitas instalarlo de forma explícita:

```bash
uv add --dev pytest
```

### Ejecutar los tests

```bash
uv run pytest
```

Para ver el detalle de cada test ejecutado:

```bash
uv run pytest -v
```

### Qué cubre cada archivo

| Archivo | Qué prueba |
|---|---|
| `tests/test_camara.py` | `buscar_coincidencia()`: coincidencia correcta, sin match, umbral personalizado. `dibujar_etiqueta()`: no lanza errores y modifica la imagen. |
| `tests/test_registro.py` | `registrar_acesso()`: registra un nuevo ingreso, evita duplicados, soporta múltiples personas y guarda la hora en el formato esperado. Usa el fixture `tmp_path` de pytest para escribir en un archivo temporal y no afectar el `registro.csv` real. |

### Configuración relevante en `pyproject.toml`

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

`pythonpath = ["."]` agrega la raíz del proyecto al path de Python al correr los tests, permitiendo que `tests/` importe los módulos de `src/` (por ejemplo, `from src.camara import buscar_coincidencia`) sin depender de la carpeta desde la que se ejecute el comando.

## Proceso de aprendizaje

Este proyecto se desarrolló con Claude (Anthropic) como mentor de arquitectura: presentando opciones de diseño con sus ventajas y desventajas en cada decisión clave, mientras yo elegía el enfoque y transcribía, ejecutaba y depuraba el código manualmente. Los bugs de transcripción y su diagnóstico a partir de los tracebacks fueron parte activa de ese proceso de aprendizaje.

El mayor reto de este refactor fue convertir un script monolítico de reconocimiento facial en módulos separados por responsabilidad (`empleados.py`, `camara.py`, `registro.py`, `comparar.py`), resolviendo además una cadena de problemas de compatibilidad de dependencias: `face_recognition_models` no se detectaba correctamente por un conflicto entre `pkg_resources` y `setuptools>=82`, un cambio de ecosistema de febrero de 2026 que rompió paquetes no mantenidos desde 2017.

## Próximas mejoras posibles

- Manejo de errores cuando una foto no contiene una cara detectable.
- Soporte para múltiples cámaras o selección de cámara por índice.
- Exportar el registro de ingresos a otros formatos (Excel, base de datos).