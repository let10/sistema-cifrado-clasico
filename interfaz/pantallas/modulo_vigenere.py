"""Pantalla del modulo de cifrado Vigenere."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Input, Label, Static

from algoritmos import vigenere


class PantallaModuloVigenere(Screen):

    BINDINGS = [("escape", "volver_menu", "Volver al menu")]

    def compose(self) -> ComposeResult:
        with Vertical(classes="contenedor-modulo modulo-vigenere"):
            yield Static("MODULO: VIGENERE", classes="nombre-modulo")
            yield Static(
                "Cifrado polialfabetico con clave de letras A-Z. Uso educativo; "
                "no protege informacion sensible.",
                classes="mensaje-pendiente",
            )
            yield Label("Mensaje:", classes="etiqueta")
            yield Input(placeholder="Escribe el mensaje...", id="input_mensaje")
            yield Label("Clave (letras A-Z):", classes="etiqueta")
            yield Input(placeholder="Ej. SOL", id="input_clave")
            yield Checkbox(
                "Mostrar procedimiento paso a paso",
                id="mostrar_procedimiento",
            )
            with Horizontal(classes="fila-botones"):
                yield Button("Cifrar", id="btn_cifrar", variant="primary")
                yield Button("Descifrar", id="btn_descifrar", variant="primary")
            with VerticalScroll(classes="panel-resultado panel-vigenere"):
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
        mostrar_procedimiento = self.query_one(
            "#mostrar_procedimiento", Checkbox
        ).value

        try:
            if es_cifrado:
                resultado = vigenere.cifrar(mensaje, clave)
                accion = "CIFRADO"
            else:
                resultado = vigenere.descifrar(mensaje, clave)
                accion = "DESCIFRADO"

            salida_texto = (
                f"METODO: Vigenere\n"
                f"ACCION: {accion}\n"
                f"ORIGINAL: {mensaje}\n"
                f"RESULTADO: {resultado}"
            )
            if mostrar_procedimiento:
                procedimiento = vigenere.obtener_procedimiento(
                    mensaje, clave, es_cifrado
                )
                salida_texto += f"\n\n{procedimiento}"
            salida.update(salida_texto)
        except ValueError as error:
            salida.update(f"Error: {error}")

    def action_volver_menu(self) -> None:
        self.app.pop_screen()
