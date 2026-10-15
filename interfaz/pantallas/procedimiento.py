"""Vista tabular e interactiva para explicar los algoritmos clásicos."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Static

from algoritmos.modelos import PasoProcedimiento


class PantallaProcedimiento(Screen):
    BINDINGS = [
        ("escape", "volver", "Volver"),
        ("left", "anterior", "Anterior"),
        ("right", "siguiente", "Siguiente"),
    ]

    def __init__(
        self,
        algoritmo: str,
        pasos: tuple[PasoProcedimiento, ...],
    ) -> None:
        super().__init__()
        self._algoritmo = algoritmo
        self._pasos = pasos
        self._indice = 0

    def compose(self) -> ComposeResult:
        with Vertical(classes="panel-pasos procedimiento-algoritmo"):
            yield Static(
                f"PROCEDIMIENTO PASO A PASO · {self._algoritmo.upper()}",
                classes="nombre-modulo",
            )
            yield Static("", id="indicador_progreso", classes="indicador-progreso")
            yield Static("", id="titulo_paso", classes="titulo-paso")
            yield Static("", id="explicacion_paso", classes="explicacion-paso")
            yield DataTable(
                id="tabla_procedimiento",
                cursor_type="row",
                zebra_stripes=True,
            )
            with Horizontal(classes="fila-controles-paso"):
                yield Button("ANTERIOR", id="btn_anterior", classes="boton-control")
                yield Button("SIGUIENTE", id="btn_siguiente", classes="boton-control")
            yield Button(
                "VOLVER AL RESULTADO",
                id="btn_volver",
                classes="boton-secundario",
            )
        yield Footer()

    def on_mount(self) -> None:
        self._mostrar_paso()

    def on_button_pressed(self, evento: Button.Pressed) -> None:
        if evento.button.id == "btn_anterior":
            self.action_anterior()
        elif evento.button.id == "btn_siguiente":
            self.action_siguiente()
        elif evento.button.id == "btn_volver":
            self.action_volver()

    def action_anterior(self) -> None:
        if self._indice > 0:
            self._indice -= 1
            self._mostrar_paso()

    def action_siguiente(self) -> None:
        if self._indice < len(self._pasos) - 1:
            self._indice += 1
            self._mostrar_paso()

    def action_volver(self) -> None:
        self.app.pop_screen()

    def _mostrar_paso(self) -> None:
        paso = self._pasos[self._indice]
        tabla = self.query_one("#tabla_procedimiento", DataTable)
        tabla.clear(columns=True)
        anchos = [
            min(
                36,
                max(
                    [len(encabezado) + 2]
                    + [len(fila[indice]) + 2 for fila in paso.filas]
                ),
            )
            for indice, encabezado in enumerate(paso.encabezados)
        ]
        for encabezado, ancho in zip(paso.encabezados, anchos):
            tabla.add_column(encabezado, width=ancho)
        for fila in paso.filas:
            tabla.add_row(*fila)

        self.query_one("#indicador_progreso", Static).update(
            f"PASO {self._indice + 1} DE {len(self._pasos)}"
        )
        self.query_one("#titulo_paso", Static).update(paso.titulo)
        self.query_one("#explicacion_paso", Static).update(paso.explicacion)
        self.query_one("#btn_anterior", Button).disabled = self._indice == 0
        self.query_one("#btn_siguiente", Button).disabled = (
            self._indice == len(self._pasos) - 1
        )
