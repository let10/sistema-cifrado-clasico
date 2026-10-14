"""Pantalla del modulo de Sustitucion Simple."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Label, Static

from algoritmos import sustitucion

CLAVE_EJEMPLO = "QWERTYUIOPASDFGHJKLZXCVBNM"


class PantallaModuloSustitucion(Screen):

    BINDINGS = [("escape", "volver_menu", "Volver al menu")]

    def compose(self) -> ComposeResult:
        with Vertical(classes="contenedor-modulo"):
            yield Static("MODULO: SUSTITUCION SIMPLE", classes="nombre-modulo")
            yield Static(
                "Clave: 26 letras A-Z sin repetir.",
                classes="mensaje-pendiente",
            )
            yield Label("Mensaje:", classes="etiqueta")
            yield Input(placeholder="Escribe el mensaje...", id="input_mensaje")
            yield Label("Clave (26 letras):", classes="etiqueta")
            yield Input(value=CLAVE_EJEMPLO, id="input_clave")
            with Horizontal(classes="fila-botones"):
                yield Button("Cifrar", id="btn_cifrar", variant="primary")
                yield Button("Descifrar", id="btn_descifrar", variant="primary")
            with VerticalScroll(classes="panel-resultado"):
                yield Static("Esperando accion...", id="resultado")
            yield Button("<- Volver al menu", id="btn_volver")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "btn_volver":
            self.app.pop_screen()
            return
        if bid == "btn_cifrar":
            self._procesar(True)
        elif bid == "btn_descifrar":
            self._procesar(False)

    def _procesar(self, es_cifrado: bool) -> None:
        salida = self.query_one("#resultado", Static)
        mensaje = self.query_one("#input_mensaje", Input).value
        clave = self.query_one("#input_clave", Input).value
        try:
            if es_cifrado:
                res = sustitucion.cifrar(mensaje, clave)
                et = "CIFRADO"
            else:
                res = sustitucion.descifrar(mensaje, clave)
                et = "DESCIFRADO"
            proc = sustitucion.obtener_procedimiento(mensaje, clave, es_cifrado)
            salida.update(f"{et}: {res}\n\n{proc}")
        except ValueError as e:
            salida.update(f"Error: {e}")
        except Exception as e:
            salida.update(f"Error inesperado: {type(e).__name__}: {e}")

    def action_volver_menu(self) -> None:
        self.app.pop_screen()