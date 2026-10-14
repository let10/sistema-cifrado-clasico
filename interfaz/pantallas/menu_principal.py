"""Pantalla del menu principal."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from interfaz.pantallas.modulo_cesar import PantallaModuloCesar
from interfaz.pantallas.modulo_pendiente import PantallaModuloPendiente
from interfaz.pantallas.modulo_sustitucion import PantallaModuloSustitucion
from interfaz.pantallas.modulo_vigenere import PantallaModuloVigenere

PENDIENTES = {
    "btn_playfair": "PLAYFAIR",
}


class PantallaMenuPrincipal(Screen):

    BINDINGS = [
        ("up", "focus_previous", "Subir"),
        ("down", "focus_next", "Bajar"),
        ("q", "salir", "Salir"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(classes="contenedor-menu"):
            yield Static("TRABAJO FINAL", classes="titulo")
            yield Static("Sistema de Encriptacion Clasica", classes="subtitulo")
            with Vertical(classes="panel-menu"):
                yield Button("1. PLAYFAIR", id="btn_playfair")
                yield Button("2. VIGENERE", id="btn_vigenere")
                yield Button("3. CESAR", id="btn_cesar")
                yield Button("4. SUSTITUCION SIMPLE", id="btn_sustitucion")
                yield Button("SALIR DEL SISTEMA", id="btn_salir", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "btn_salir":
            self.app.exit()
        elif bid == "btn_cesar":
            self.app.push_screen(PantallaModuloCesar())
        elif bid == "btn_sustitucion":
            self.app.push_screen(PantallaModuloSustitucion())
        elif bid == "btn_vigenere":
            self.app.push_screen(PantallaModuloVigenere())
        else:
            nombre = PENDIENTES.get(bid)
            if nombre:
                self.app.push_screen(PantallaModuloPendiente(nombre))

    def action_salir(self) -> None:
        self.app.exit()
