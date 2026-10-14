"""Visualización interactiva paso a paso del cifrado Playfair.

Reconstruye, a partir del mensaje y la clave ya validados en
``PantallaPlayfair``, la secuencia completa de pasos que genera
``algoritmos.playfair.generar_pasos``: construcción de la matriz,
preparación del mensaje en dígrafos y, para cada dígrafo, la regla
aplicada con las posiciones de entrada y resultado resaltadas.

No vuelve a pedir datos al usuario ni repite el cifrado/descifrado:
solo expone, con fines educativos, el proceso intermedio que
``cifrar``/``descifrar`` ya calculan internamente.
"""

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from algoritmos import playfair

ESTILO_TITULO = "bold #c4b5fd"
ESTILO_TEXTO = "#ede9fe"
ESTILO_REGLA = "bold #a78bfa"
ESTILO_RESULTADO_ACUMULADO = "bold #5eead4"
ESTILO_SEPARADOR = "#4c1d95"
ESTILO_ERROR = "bold #f87171"

ESTILO_LETRA_CLAVE = "bold #1b1030 on #c4b5fd"
ESTILO_LETRA_ENTRADA = "bold white on #7c3aed"
ESTILO_LETRA_RESULTADO = "bold #1b1030 on #5eead4"
ESTILO_LETRA_ENTRADA_Y_RESULTADO = "bold white on #a21caf"


class PantallaPlayfairPasos(Screen):
    """Demostración paso a paso de la matriz y las reglas de Playfair."""

    BINDINGS = [
        ("escape", "volver_resultado", "Volver al resultado"),
        ("left", "anterior", "Anterior"),
        ("right", "siguiente", "Siguiente"),
    ]

    def __init__(self, mensaje: str, clave: str, operacion: str) -> None:
        super().__init__()
        self._mensaje = mensaje
        self._clave = clave
        self._operacion = operacion
        self._pasos: list | None = None
        self._error: str | None = None
        self._matriz: list | None = None
        self._indice = 0
        self._mostrar_todo = False

    def compose(self) -> ComposeResult:
        with Vertical(classes="contenedor-principal"):
            with Vertical(classes="panel-pasos"):
                yield Static(
                    "VISUALIZACIÓN PASO A PASO · PLAYFAIR", classes="nombre-modulo"
                )
                yield Static("", id="indicador_progreso", classes="indicador-progreso")
                # Solo este contenedor hace scroll: así los controles de
                # navegación quedan siempre visibles, incluso con "MOSTRAR
                # TODO" (que concatena los 5+ pasos y puede ser muy largo).
                with VerticalScroll(classes="contenido-paso-scroll"):
                    yield Static(Text(""), id="contenido_paso", classes="contenido-paso")
                with Horizontal(classes="fila-controles-paso"):
                    yield Button("ANTERIOR", id="btn_anterior", classes="boton-control")
                    yield Button(
                        "SIGUIENTE", id="btn_siguiente", classes="boton-control"
                    )
                    yield Button(
                        "MOSTRAR TODO", id="btn_mostrar_todo", classes="boton-control"
                    )
                yield Button(
                    "VOLVER AL RESULTADO",
                    id="btn_volver_resultado",
                    classes="boton-secundario",
                )
        yield Footer()

    def on_mount(self) -> None:
        try:
            self._pasos = playfair.generar_pasos(
                self._mensaje, self._clave, self._operacion
            )
            self._matriz = self._pasos[0]["matriz"]
        except ValueError as error:
            self._error = str(error)

        self._mostrar_estado()
        self.call_after_refresh(self._fijar_scroll_inicial)

    def _fijar_scroll_inicial(self) -> None:
        self.query_one(".contenido-paso-scroll").scroll_home(animate=False)

    def on_button_pressed(self, evento: Button.Pressed) -> None:
        if evento.button.id == "btn_anterior":
            self.action_anterior()
        elif evento.button.id == "btn_siguiente":
            self.action_siguiente()
        elif evento.button.id == "btn_mostrar_todo":
            self._mostrar_todo = not self._mostrar_todo
            self._mostrar_estado()
        elif evento.button.id == "btn_volver_resultado":
            self.action_volver_resultado()

    def action_anterior(self) -> None:
        if self._pasos and not self._mostrar_todo and self._indice > 0:
            self._indice -= 1
            self._mostrar_estado()

    def action_siguiente(self) -> None:
        if (
            self._pasos
            and not self._mostrar_todo
            and self._indice < len(self._pasos) - 1
        ):
            self._indice += 1
            self._mostrar_estado()

    def action_volver_resultado(self) -> None:
        self.app.pop_screen()

    def _mostrar_estado(self) -> None:
        contenido_widget = self.query_one("#contenido_paso", Static)
        indicador_widget = self.query_one("#indicador_progreso", Static)
        boton_anterior = self.query_one("#btn_anterior", Button)
        boton_siguiente = self.query_one("#btn_siguiente", Button)
        boton_mostrar_todo = self.query_one("#btn_mostrar_todo", Button)

        if self._error is not None or not self._pasos:
            contenido_widget.update(
                Text(
                    self._error or "No hay pasos disponibles para mostrar.",
                    style=ESTILO_ERROR,
                )
            )
            indicador_widget.update("")
            boton_anterior.disabled = True
            boton_siguiente.disabled = True
            boton_mostrar_todo.disabled = True
            return

        if self._mostrar_todo:
            contenido_widget.update(self._construir_texto_todos_los_pasos())
            indicador_widget.update(f"Mostrando los {len(self._pasos)} pasos")
        else:
            contenido_widget.update(self._construir_contenido_paso(self._pasos[self._indice]))
            indicador_widget.update(f"Paso {self._indice + 1} de {len(self._pasos)}")

        boton_anterior.disabled = self._mostrar_todo or self._indice == 0
        boton_siguiente.disabled = (
            self._mostrar_todo or self._indice == len(self._pasos) - 1
        )
        boton_mostrar_todo.label = (
            "VER PASO A PASO" if self._mostrar_todo else "MOSTRAR TODO"
        )
        self.query_one(".contenido-paso-scroll").scroll_home(animate=False)

    def _construir_texto_todos_los_pasos(self) -> Text:
        texto_completo = Text()
        for indice, paso in enumerate(self._pasos):
            if indice > 0:
                texto_completo.append("\n" + "─" * 60 + "\n\n", style=ESTILO_SEPARADOR)
            texto_completo.append_text(self._construir_contenido_paso(paso))
        return texto_completo

    def _construir_contenido_paso(self, paso: dict) -> Text:
        contenido = Text()
        contenido.append(paso["titulo"] + "\n\n", style=ESTILO_TITULO)

        if paso["tipo"] == "matriz":
            resaltados = {
                (fila, columna): ESTILO_LETRA_CLAVE
                for fila, fila_letras in enumerate(paso["matriz"])
                for columna, letra in enumerate(fila_letras)
                if letra in paso["letras_clave"]
            }
            contenido.append_text(self._construir_texto_matriz(paso["matriz"], resaltados))
            contenido.append("\n\n")
            contenido.append(
                "Resaltado: letras tomadas de la clave «"
                f"{paso['clave_normalizada']}».\n\n",
                style=ESTILO_REGLA,
            )
            contenido.append(paso["explicacion"], style=ESTILO_TEXTO)

        elif paso["tipo"] == "preparacion":
            contenido.append(f"Mensaje original: {paso['mensaje_original']}\n", style=ESTILO_TEXTO)
            contenido.append(
                f"Mensaje normalizado: {paso['mensaje_normalizado']}\n", style=ESTILO_TEXTO
            )
            contenido.append(
                f"Dígrafos: {' '.join(paso['digrafos'])}\n\n", style=ESTILO_TEXTO
            )
            contenido.append(paso["explicacion"], style=ESTILO_TEXTO)

        elif paso["tipo"] == "digrafo":
            resaltados = self._resaltar_digrafo(paso)
            contenido.append_text(self._construir_texto_matriz(self._matriz, resaltados))
            contenido.append("\n\n")
            contenido.append("Resaltado: ", style=ESTILO_TEXTO)
            contenido.append("letras de entrada", style=ESTILO_LETRA_ENTRADA)
            contenido.append("  ·  ", style=ESTILO_TEXTO)
            contenido.append("letras resultantes", style=ESTILO_LETRA_RESULTADO)
            contenido.append("\n\n")
            contenido.append(f"Regla aplicada: {paso['nombre_regla']}\n", style=ESTILO_REGLA)
            contenido.append(paso["explicacion"] + "\n\n", style=ESTILO_TEXTO)
            contenido.append(
                f"{paso['digrafo_entrada']} → {paso['digrafo_resultado']}\n",
                style="bold " + ESTILO_TEXTO,
            )
            contenido.append(
                f"Resultado acumulado: {paso['resultado_acumulado']}",
                style=ESTILO_RESULTADO_ACUMULADO,
            )

        return contenido

    @staticmethod
    def _resaltar_digrafo(paso: dict) -> dict:
        posiciones_entrada = set(paso["posiciones_entrada"])
        posiciones_resultado = set(paso["posiciones_resultado"])

        resaltados = {}
        for posicion in posiciones_entrada | posiciones_resultado:
            es_entrada = posicion in posiciones_entrada
            es_resultado = posicion in posiciones_resultado
            if es_entrada and es_resultado:
                resaltados[posicion] = ESTILO_LETRA_ENTRADA_Y_RESULTADO
            elif es_entrada:
                resaltados[posicion] = ESTILO_LETRA_ENTRADA
            else:
                resaltados[posicion] = ESTILO_LETRA_RESULTADO
        return resaltados

    @staticmethod
    def _construir_texto_matriz(matriz: list, resaltados: dict) -> Text:
        texto = Text()
        tamano = len(matriz)
        for fila in range(tamano):
            for columna in range(tamano):
                estilo = resaltados.get((fila, columna), ESTILO_TEXTO)
                texto.append(f" {matriz[fila][columna]} ", style=estilo)
                if columna < tamano - 1:
                    texto.append(" ")
            if fila < tamano - 1:
                texto.append("\n")
        return texto
