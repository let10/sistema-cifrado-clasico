# TRABAJO FINAL — Sistema de Encriptación Clásica

Proyecto universitario del curso de Criptografía. Aplicación de
terminal (TUI) que integrará los módulos de cifrado clásico
desarrollados por cada integrante del equipo.

> **Advertencia:** este sistema tiene fines educativos. Los cifrados
> clásicos que integrará (Playfair, Vigenère, César y sustitución
> simple) **no son seguros** para proteger información sensible real.
> Esta advertencia ya no se muestra en el menú principal; cada
> responsable de módulo deberá incluirla en la pantalla informativa
> de su algoritmo cuando la implemente.

## Estado actual

El sistema incluye una interfaz de terminal para César, sustitución
simple, Vigenère y Playfair. César, sustitución simple y Vigenère
muestran el resultado por separado del procedimiento educativo. El
procedimiento se presenta en una vista interactiva con tablas reales,
pasos navegables y contenido desplazable.

## Requisitos

- Python 3.9 o superior.
- Terminal con soporte de color (recomendado: Kitty en Kali Linux).

## Instalación

```bash
cd sistema-cifrado-clasico
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
source .venv/bin/activate
python3 main.py
```

## Navegación

- **Mouse:** clic directo sobre los botones.
- **Teclado:** flechas arriba/abajo (o Tab/Shift+Tab) para moverse
  entre botones, Enter para seleccionar.
- **Esc:** regresa al menú principal desde cualquier pantalla de
  módulo.
- **q:** sale del sistema desde el menú principal.

## Estructura del proyecto

```
sistema-cifrado-clasico/
├── main.py                        Punto de entrada
├── requirements.txt
├── interfaz/
│   ├── aplicacion.py               App principal (Textual)
│   ├── estilos.tcss                Tema oscuro violeta
│   └── pantallas/
│       ├── menu_principal.py       Menú con los 5 botones
│       ├── modulo_cesar.py         Interfaz de César
│       ├── modulo_sustitucion.py   Interfaz de sustitución simple
│       ├── modulo_vigenere.py      Interfaz de Vigenère
│       ├── procedimiento.py        Vista tabular paso a paso
│       ├── playfair.py             Interfaz de Playfair
│       ├── playfair_pasos.py       Procedimiento interactivo Playfair
│       └── modulo_pendiente.py     Pantalla genérica de módulo
├── algoritmos/
│   ├── modelos.py                  Tipos compartidos de procedimientos
│   ├── cesar.py                    Cifrado César
│   ├── sustitucion.py              Sustitución simple
│   ├── vigenere.py                 Cifrado Vigenère
│   └── playfair.py                 Cifrado Playfair
└── tests/
    ├── test_navegacion.py          Pruebas funcionales de navegación
    ├── test_vigenere.py            Pruebas del algoritmo Vigenère
    └── test_procedimiento_tabular.py Pruebas de procedimientos estructurados
```

Los módulos de algoritmos exponen `cifrar(mensaje, clave)` y
`descifrar(mensaje, clave)`. En César, sustitución simple y Vigenère
los espacios, números y signos se conservan. En Vigenère, la clave
debe contener letras A-Z y los caracteres que no son letras no avanzan
la clave. El interruptor «Mostrar procedimiento» permite abrir
automáticamente el desglose; también se puede consultar con el botón
«Ver procedimiento detallado» después de cada operación.

## Pruebas

```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

Las pruebas verifican navegación, algoritmos, validación de claves,
conservación de caracteres, generación de pasos tabulares e
integración de la vista interactiva.

## Nota sobre los requisitos del docente

El documento de la tarea exige explícitamente los algoritmos **César,
sustitución simple y Vigenère** (objetivo específico 1). Los tres están
implementados; Playfair también está disponible como módulo adicional.
