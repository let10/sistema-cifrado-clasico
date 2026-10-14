"""Punto de entrada del Sistema de Encriptación Clásica.

Ejecución: python3 main.py
"""

from interfaz.aplicacion import SistemaEncriptacionClasica


def main() -> None:
    aplicacion = SistemaEncriptacionClasica()
    aplicacion.run()


if __name__ == "__main__":
    main()
