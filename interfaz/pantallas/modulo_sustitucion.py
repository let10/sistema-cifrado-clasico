"""Pantalla del modulo de Sustitucion Simple."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Label, Static, Switch

from algoritmos import sustitucion
from algoritmos.modelos import PasoProcedimiento
from interfaz.pantallas.procedimiento import PantallaProcedimiento

CLAVE_EJEMPLO = "QWERTYUIOPASDFGHJKLZXCVBNM"


class PantallaModuloSustitucion(Screen):

    BINDINGS = [("escape", "volver_menu", "Volver al menu")]

    def __init__(self) -> None:
        super().__init__()
        self._pasos: tuple[PasoProcedimiento, ...] = ()

    def compose(self) -> ComposeResult:
        with Vertical(classes="contenedor-modulo"):
            yield Static("MODULO: SUSTITUCION SIMPLE", classes="nombre-modulo")
            yield Static(
                "Clave: 26 letras A-Z sin repetir.",
                classes="mensaje-pendiente",
            )
            yield Label("Mensaje:", classes="etiqueta")
            yield Input(placeholder="Escribe el mensaje...", id="input_mensaje")
            with Horizontal(classes="encabezado-clave"):
                yield Label("Clave (26 letras):", classes="etiqueta")
                yield Static("PASOS: NO", id="estado_procedimiento", classes="encabezado-estado")
            with Horizontal(classes="fila-clave"):
                yield Input(
                    value=CLAVE_EJEMPLO,
                    id="input_clave",
                    classes="input-clave",
                )
                yield Switch(
                    id="mostrar_procedimiento",
                    classes="switch-procedimiento",
                    tooltip="Abrir el procedimiento detallado después de operar",
                )
            with Horizontal(classes="fila-botones"):
                yield Button("Cifrar", id="btn_cifrar", variant="primary")
                yield Button("Descifrar", id="btn_descifrar", variant="primary")
            with VerticalScroll(classes="panel-resultado"):
                yield Static("Ingresa el mensaje y la clave.", id="resultado")
            yield Button(
                "VER PROCEDIMIENTO DETALLADO",
                id="btn_ver_procedimiento",
                disabled=True,
            )
            yield Button("<- Volver al menu", id="btn_volver")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "btn_volver":
            self.app.pop_screen()
            return
        if bid == "btn_ver_procedimiento":
            self._ver_procedimiento()
            return
        if bid == "btn_cifrar":
            self._procesar(True)
        elif bid == "btn_descifrar":
            self._procesar(False)

    def on_switch_changed(self, event: Switch.Changed) -> None:
        estado = self.query_one("#estado_procedimiento", Static)
        estado.update("PASOS: SI" if event.value else "PASOS: NO")
        estado.set_class(event.value, "procedimiento-activo")

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
            self._pasos = sustitucion.generar_pasos(mensaje, clave, es_cifrado)
            salida.update(
                f"ALGORITMO: Sustitución simple\n"
                f"OPERACIÓN: {et}\n"
                f"ORIGINAL: {mensaje}\n"
                f"RESULTADO: {res}"
            )
            boton_pasos = self.query_one("#btn_ver_procedimiento", Button)
            boton_pasos.disabled = False
            if self.query_one("#mostrar_procedimiento", Switch).value:
                self._ver_procedimiento()
        except ValueError as error:
            salida.update(f"Error: {error}")
            self._pasos = ()
            self.query_one("#btn_ver_procedimiento", Button).disabled = True

    def _ver_procedimiento(self) -> None:
        if self._pasos:
            self.app.push_screen(
                PantallaProcedimiento("Sustitución simple", self._pasos)
            )

    def action_volver_menu(self) -> None:
        self.app.pop_screen()