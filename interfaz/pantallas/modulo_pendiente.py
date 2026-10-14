"""Pantalla genérica para un módulo de algoritmo aún no integrado.

Cada integrante del equipo reemplazará esta pantalla por la interfaz
real de su algoritmo (cifrar, descifrar, información educativa, etc.)
cuando su módulo esté listo.
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

RESPONSABLES = {
    "PLAYFAIR": "Integrante 1",
    "VIGENÈRE": "Integrante 2",
    "CÉSAR": "Por asignar",
    "SUSTITUCIÓN SIMPLE": "Por asignar",
}


class PantallaModuloPendiente(Screen):
    """Muestra el estado "pendiente de integración" de un módulo."""

    BINDINGS = [("escape", "volver_menu", "Volver al menú")]

    def __init__(self, nombre_modulo: str) -> None:
        super().__init__()
        self.nombre_modulo = nombre_modulo

    def compose(self) -> ComposeResult:
        responsable = RESPONSABLES.get(self.nombre_modulo, "Por asignar")
        with Vertical(classes="contenedor-principal"):
            with Vertical(classes="panel-modulo"):
                yield Static(f"MÓDULO: {self.nombre_modulo}", classes="nombre-modulo")
                yield Static(
                    "Este módulo está pendiente de integración.",
                    classes="mensaje-pendiente",
                )
                yield Static(
                    f"Responsable: {responsable}",
                    classes="responsable-modulo",
                )
                yield Button(
                    "← Volver al menú", id="btn_volver", classes="boton-menu"
                )
        yield Footer()

    def on_button_pressed(self, evento: Button.Pressed) -> None:
        if evento.button.id == "btn_volver":
            self.action_volver_menu()

    def action_volver_menu(self) -> None:
        self.app.pop_screen()
