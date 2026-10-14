"""Pantalla del menú principal del sistema.

Muestra únicamente los cinco botones autorizados: PLAYFAIR, VIGENÈRE,
CÉSAR, SUSTITUCIÓN SIMPLE y SALIR DEL SISTEMA. No agregar botones
adicionales sin autorización explícita del equipo.
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from interfaz.pantallas.modulo_cesar import PantallaModuloCesar
from interfaz.pantallas.modulo_sustitucion import PantallaModuloSustitucion
from interfaz.pantallas.modulo_vigenere import PantallaModuloVigenere
from interfaz.pantallas.playfair import PantallaPlayfair

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

        pantallas = {
            "btn_vigenere": PantallaModuloVigenere,
            "btn_cesar": PantallaModuloCesar,
            "btn_sustitucion": PantallaModuloSustitucion,
        }
        pantalla = pantallas.get(id_boton)
        if pantalla is not None:
            self.app.push_screen(pantalla())

    def action_enfocar_siguiente(self) -> None:
        self.focus_next()

    def action_enfocar_anterior(self) -> None:
        self.focus_previous()

    def action_salir_sistema(self) -> None:
        self.app.exit()
