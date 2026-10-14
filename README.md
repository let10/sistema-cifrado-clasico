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

El sistema incluye la interfaz principal y los módulos funcionales de
César, sustitución simple y Vigenère. Playfair permanece pendiente de
integración. Vigenère permite cifrar y descifrar desde su pantalla y
mostrar, opcionalmente, el procedimiento carácter por carácter.

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
│       └── modulo_pendiente.py     Pantalla genérica de módulo
├── algoritmos/
│   ├── cesar.py                    Cifrado César
│   ├── sustitucion.py              Sustitución simple
│   ├── vigenere.py                 Cifrado Vigenère
│   └── playfair.py                 Pendiente
└── tests/
    ├── test_navegacion.py          Pruebas funcionales de navegación
    └── test_vigenere.py            Pruebas del algoritmo Vigenère
```

Los módulos de algoritmos exponen `cifrar(mensaje, clave)` y
`descifrar(mensaje, clave)`, conservando espacios, números y signos
según las reglas de cada algoritmo. En Vigenère la clave debe contener
solo letras A-Z; los caracteres que no son letras se conservan y no
avanzan la clave. Su casilla de procedimiento está desactivada por
defecto.

## Pruebas

```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

Las pruebas verifican navegación, el cifrado/descifrado de Vigenère,
la validación de la clave, la conservación de caracteres y la
visualización opcional del procedimiento.

## Nota sobre los requisitos del docente

El documento de la tarea exige explícitamente los algoritmos **César,
sustitución simple y Vigenère** (objetivo específico 1). Los tres están
implementados; Playfair aparece en el menú, pero todavía está pendiente.
