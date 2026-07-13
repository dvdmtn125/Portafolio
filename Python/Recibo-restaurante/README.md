# Mi Restaurante — Sistema de Facturación

Aplicación de escritorio en **Python + Tkinter** para gestionar la facturación
de un restaurante: selección de comida, bebidas y postres, cálculo de
subtotales/IVA/total, calculadora integrada, generación de un recibo en
texto y guardado a disco.

El proyecto se implementó siguiendo principios de **arquitectura limpia**: 
la lógica de negocio nodepende de Tkinter, por lo que se puede probar con 
`pytest` sin abrir ninguna ventana.

## Características

- Selección de productos por categoría (comida, bebida, postres), cada uno
  con su checkbox y cantidad.
- Cálculo automático de subtotal por categoría, IVA (19%) y total general.
- Calculadora integrada para operaciones rápidas.
- Generación de un recibo en texto con el detalle de los productos comprados.
- Guardado del recibo como archivo `.txt` mediante un diálogo nativo del
  sistema operativo.
- Botón de reseteo que limpia todos los campos para una nueva factura.

## Requisitos

- Python 3.10 o superior.
- Tkinter (incluido en la instalación estándar de Python; en Linux puede
  requerir instalar el paquete del sistema `python3-tk` aparte).
- [uv](https://docs.astral.sh/uv/) como gestor de entornos y dependencias.

## Instalación y ejecución

```bash
# Clonar el repositorio y entrar a la carpeta del proyecto
cd Recibo-restaurante

# Instalar dependencias (uv crea el entorno virtual automáticamente)
uv sync

# Ejecutar la aplicación
uv run python main.py
```

También se puede instalar como paquete editable y usar el comando definido
en `pyproject.toml`:

```bash
uv pip install -e .
mi-restaurante
```

## Estructura del proyecto

```
mi_restaurante/
│
├── main.py                          # Punto de entrada: arma toda la app y arranca mainloop()
├── pyproject.toml                   # Metadatos del proyecto y configuración de build
│
├── data/
│   └── productos.py                 # Catálogo de productos (nombres y precios)
│
├── domain/                          # Lógica de negocio pura, sin Tkinter
│   ├── calculadora.py               # Lógica de la calculadora (acumular/resolver expresión)
│   ├── facturacion.py               # Cálculo de subtotales, IVA y total
│   └── recibo.py                    # Construcción del texto del recibo
│
├── infrastructure/
│   └── almacenamiento.py            # Guardado del recibo a disco (diálogo + escritura)
│
├── ui/
│   ├── ventana_principal.py         # Ventana raíz y contenedores estructurales
│   ├── panel_productos.py           # Checkboxes y cantidades de comida/bebida/postres
│   ├── panel_costos.py              # Etiquetas y campos de costos/subtotal/IVA/total
│   ├── panel_calculadora.py         # Visor y botones de la calculadora
│   ├── panel_recibo.py              # Área de texto donde se muestra el recibo
│   └── panel_botones.py             # Botones Total / Recibo / Guardar / Resetear
│
├── controllers/
│   ├── controlador_facturacion.py   # Conecta domain/infrastructure con la UI de facturación
│   └── controlador_calculadora.py   # Conecta domain/calculadora.py con la UI de la calculadora
│
└── tests/
    ├── test_calculadora.py          # 9 tests de domain/calculadora.py
    ├── test_facturacion.py          # 10 tests de domain/facturacion.py
    ├── test_recibo.py               # 7 tests de domain/recibo.py
    └── test_almacenamiento.py       # 4 tests de infrastructure/almacenamiento.py
```

## Arquitectura

El proyecto separa responsabilidades en capas, de modo que cada módulo solo
conoce a sus vecinos directos:

- **`data/`** — Fuente de verdad de los datos del catálogo. No depende de
  nada más.
- **`domain/`** — Reglas de negocio puras: reciben y devuelven números o
  strings simples, sin tocar ningún widget. Son las únicas piezas con
  cobertura de tests con sentido (no requieren Tkinter para probarse).
- **`infrastructure/`** — Operaciones de entrada/salida (en este caso,
  escritura a disco). Aislada para poder simularla en tests sin abrir
  diálogos reales del sistema operativo.
- **`ui/`** — Construcción de widgets de Tkinter. No contiene lógica de
  negocio: cada panel recibe *callbacks* y expone las referencias que el
  controlador necesita leer o escribir.
- **`controllers/`** — El "pegamento": traducen eventos de la UI en llamadas
  a `domain`/`infrastructure`, y llevan los resultados de vuelta a la UI.
- **`main.py`** — El único módulo que conoce todo el árbol del proyecto;
  arma la ventana, los paneles y los controladores, y los conecta entre sí.

## Tests

La capa de `domain/` e `infrastructure/` tiene cobertura completa con `pytest`.
Los tests no requieren Tkinter ni abrir ninguna ventana — prueban la lógica
pura directamente.

| Archivo | Módulo cubierto | Tests |
|---|---|---|
| `tests/test_calculadora.py` | `domain/calculadora.py` | 9 |
| `tests/test_facturacion.py` | `domain/facturacion.py` | 10 |
| `tests/test_recibo.py` | `domain/recibo.py` | 7 |
| `tests/test_almacenamiento.py` | `infrastructure/almacenamiento.py` | 4 |
| **Total** | | **30** |

Para correr la suite completa:

```powershell
uv run pytest -v
```

Para ver el reporte de cobertura:

```powershell
uv run pytest --cov=domain --cov=infrastructure tests/
```

Técnicas usadas en los tests:

- **`pytest.approx`** para comparar floats sin errores de redondeo binario.
- **Inyección de parámetros opcionales** (`numero_recibo`, `fecha`,
  `abrir_dialogo`) para fijar resultados no deterministas (random, datetime)
  y simular el diálogo "Guardar como" sin abrir ninguna ventana real.
- **`io.StringIO`** como archivo en memoria para probar escritura a disco
  sin tocar el sistema de archivos.
- **`pytest.raises`** para verificar que los casos de error (expresión vacía,
  división por cero, categorías inconsistentes) lanzan excepciones claras en
  vez de reventar con errores crípticos.

  ## Proceso de aprendizaje

Este proyecto se desarrolló con Claude (Anthropic) como mentor de arquitectura: presentando opciones de diseño con sus ventajas y desventajas en cada decisión clave, mientras yo elegía el enfoque y transcribía, ejecutaba y depuraba el código manualmente. Los bugs de transcripción y su diagnóstico a partir de los tracebacks fueron parte activa de ese proceso de aprendizaje. El mayor reto de este refactor fue convertir un script monolítico de Tkinter en las 4 capas de Clean Architecture, separando la interfaz gráfica y la lógica de facturación que originalmente estaban mezcladas en un solo archivo.

## Mejoras futuras

- [ ] Validación de entradas no numéricas en las cantidades (actualmente
  `calcular_total()` truena con `ValueError` si se escribe texto en una
  casilla de cantidad).
- [ ] Historial de recibos generados en la sesión.
- [ ] Tests de integración para `controllers/` usando mocks de los widgets
  de Tkinter.