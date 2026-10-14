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

Esta etapa entrega únicamente el **punto de entrada (`main.py`) y la
interfaz principal**: el menú con los cinco botones y la navegación
entre pantallas. Ningún algoritmo de cifrado/descifrado está
implementado todavía; cada módulo muestra una pantalla de "pendiente
de integración" hasta que su responsable complete el código en
`algoritmos/`.

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
│       └── modulo_pendiente.py     Pantalla genérica de módulo
├── algoritmos/
│   ├── playfair.py                 Pendiente
│   └── vigenere.py                 Pendiente
└── tests/
    └── test_navegacion.py          Pruebas funcionales de navegación
```

Los módulos de `algoritmos/` expondrán el contrato `cifrar(mensaje,
clave)` / `descifrar(mensaje, clave)` cuando se implementen, conservando
espacios, números y signos de puntuación según las reglas de cada
algoritmo. César y sustitución simple todavía no tienen archivo en
`algoritmos/`: solo existen como botones del menú con pantalla
"pendiente de integración".

## Pruebas

```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

Las pruebas actuales verifican que el menú principal se muestre al
iniciar, que existan los cinco botones esperados, que cada botón
navegue a la pantalla de módulo correcta, que sea posible volver al
menú (con el botón o con Esc) y que "Salir del sistema" cierre la
aplicación.

## Nota sobre los requisitos del docente

El documento de la tarea exige explícitamente los algoritmos **César,
sustitución simple y Vigenère** (objetivo específico 1), aunque la
rúbrica de la sección 16 permite un mínimo de dos algoritmos y admite
Playfair y Afín como alternativas válidas. El menú principal ya cubre
los cuatro algoritmos (Playfair, Vigenère, César y sustitución simple),
satisfaciendo tanto el objetivo específico 1 como la rúbrica.
