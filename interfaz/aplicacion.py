"""Aplicación principal (Textual App) del sistema.

Centraliza la configuración global de la interfaz y el registro de
pantallas. Los módulos de algoritmos no se importan aquí todavía: cada
pantalla de módulo los integrará cuando estén implementados.
"""

from textual.app import App

from interfaz.pantallas.menu_principal import PantallaMenuPrincipal


class SistemaEncriptacionClasica(App):
    """Aplicación de consola para el Sistema de Encriptación Clásica."""

    TITLE = "TRABAJO FINAL"
    SUB_TITLE = "Sistema de Encriptación Clásica"
    CSS_PATH = "estilos.tcss"

    def on_mount(self) -> None:
        self.push_screen(PantallaMenuPrincipal())
