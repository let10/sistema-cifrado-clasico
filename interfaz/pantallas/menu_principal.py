"""Pantalla del menú principal del sistema.

Muestra únicamente los cinco botones autorizados: PLAYFAIR, VIGENÈRE,
CÉSAR, SUSTITUCIÓN SIMPLE y SALIR DEL SISTEMA. No agregar botones
adicionales sin autorización explícita del equipo.
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from interfaz.pantallas.modulo_pendiente import PantallaModuloPendiente
from interfaz.pantallas.playfair import PantallaPlayfair

MODULOS_PENDIENTES = {
    "btn_vigenere": "VIGENÈRE",
    "btn_cesar": "CÉSAR",
    "btn_sustitucion": "SUSTITUCIÓN SIMPLE",
}


class PantallaMenuPrincipal(Screen):
    """Pantalla inicial con la navegación hacia los módulos del equipo."""

    BINDINGS = [
        ("up", "enfocar_anterior", "Subir"),
        ("down", "enfocar_siguiente", "Bajar"),
        ("q", "salir_sistema", "Salir"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(classes="contenedor-principal"):
            yield Static("TRABAJO FINAL", classes="titulo")
            yield Static("Sistema de Encriptación Clásica", classes="subtitulo")
            with Vertical(classes="panel-menu"):
                with Vertical(classes="grupo-botones"):
                    yield Button(
                        "1. PLAYFAIR", id="btn_playfair", classes="boton-menu"
                    )
                    yield Button(
                        "2. VIGENÈRE", id="btn_vigenere", classes="boton-menu"
                    )
                    yield Button("3. CÉSAR", id="btn_cesar", classes="boton-menu")
                    yield Button(
                        "4. SUSTITUCIÓN SIMPLE",
                        id="btn_sustitucion",
                        classes="boton-menu",
                    )
                    yield Button(
                        "SALIR DEL SISTEMA",
                        id="btn_salir",
                        classes="boton-salir",
                    )
        yield Footer()

    def on_button_pressed(self, evento: Button.Pressed) -> None:
        id_boton = evento.button.id

        if id_boton == "btn_salir":
            self.action_salir_sistema()
            return

        if id_boton == "btn_playfair":
            self.app.push_screen(PantallaPlayfair())
            return

        nombre_modulo = MODULOS_PENDIENTES.get(id_boton)
        if nombre_modulo is not None:
            self.app.push_screen(PantallaModuloPendiente(nombre_modulo))

    def action_enfocar_siguiente(self) -> None:
        self.focus_next()

    def action_enfocar_anterior(self) -> None:
        self.focus_previous()

    def action_salir_sistema(self) -> None:
        self.app.exit()
