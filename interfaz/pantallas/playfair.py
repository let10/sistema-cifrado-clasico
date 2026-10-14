"""Pantalla funcional del cifrado Playfair.

Permite cifrar y descifrar mensajes con Playfair, mostrando con
claridad el mensaje original, el mensaje normalizado (solo letras,
con I/J fusionadas) y el mensaje preparado en dígrafos, además del
resultado final.

Playfair no puede conservar espacios, números ni signos de
puntuación sin romper su estructura de dígrafos (ver docstring de
``algoritmos.playfair``); esta pantalla no oculta esa limitación,
sino que la muestra como advertencia explícita cuando corresponde.

Tras una operación exitosa, el botón "VER PASO A PASO" abre
``PantallaPlayfairPasos`` con la demostración interactiva de la
matriz y cada dígrafo (ver ``interfaz.pantallas.playfair_pasos``).
"""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, RadioButton, RadioSet, Static

from algoritmos import playfair
from algoritmos.playfair import OPERACION_CIFRAR, OPERACION_DESCIFRAR
from interfaz.pantallas.playfair_pasos import PantallaPlayfairPasos


class PantallaPlayfair(Screen):
    """Pantalla de cifrado y descifrado Playfair."""

    BINDINGS = [("escape", "volver_menu", "Volver al menú")]

    def __init__(self) -> None:
        super().__init__()
        self._ultimo_resultado_cifrado: str | None = None
        self._ultima_clave_usada: str = ""
        # Punto de extensión para la Fase 3: aquí se guardará la matriz,
        # los dígrafos y los pasos de la última operación ejecutada para
        # que un panel de visualización pueda reconstruirlos sin volver
        # a pedir datos al usuario.
        self._ultimo_calculo: dict | None = None

    def compose(self) -> ComposeResult:
        with Vertical(classes="contenedor-principal"):
            with Vertical(classes="panel-algoritmo"):
                yield Static("CIFRADO PLAYFAIR", classes="nombre-modulo")

                yield Static("Operación", classes="etiqueta-campo")
                with RadioSet(id="selector_operacion"):
                    yield RadioButton("Cifrar", id="opcion_cifrar", value=True)
                    yield RadioButton("Descifrar", id="opcion_descifrar")

                yield Static("Mensaje", classes="etiqueta-campo")
                yield Input(
                    placeholder="Escribe el mensaje a cifrar o descifrar",
                    id="input_mensaje",
                )

                yield Static("Clave", classes="etiqueta-campo")
                yield Input(
                    placeholder="Clave Playfair (solo letras)",
                    id="input_clave",
                )

                with Horizontal(classes="fila-botones"):
                    yield Button(
                        "CIFRAR MENSAJE", id="btn_ejecutar", classes="boton-accion"
                    )
                    yield Button(
                        "LIMPIAR", id="btn_limpiar", classes="boton-accion"
                    )

                yield Button(
                    "USAR RESULTADO PARA DESCIFRAR",
                    id="btn_usar_resultado",
                    classes="boton-secundario",
                    disabled=True,
                )

                yield Button(
                    "VER PASO A PASO",
                    id="btn_ver_pasos",
                    classes="boton-secundario",
                    disabled=True,
                )

                yield Static("", id="resultado", classes="panel-resultado")
                yield Static("", id="advertencias", classes="texto-advertencia")
                yield Static("", id="error_mensaje", classes="mensaje-error")

                yield Button(
                    "← VOLVER AL MENÚ PRINCIPAL",
                    id="btn_volver",
                    classes="boton-secundario",
                )
        yield Footer()

    def on_mount(self) -> None:
        self._actualizar_etiqueta_boton_ejecutar()
        # El foco automático inicial en el RadioSet hace que Textual
        # desplace el panel para mostrarlo, lo que oculta el título. Se
        # restaura la posición inicial del scroll tras ese desplazamiento.
        self.call_after_refresh(self._fijar_scroll_inicial)

    def _fijar_scroll_inicial(self) -> None:
        self.query_one(".panel-algoritmo").scroll_home(animate=False)

    def on_radio_set_changed(self, evento: RadioSet.Changed) -> None:
        if evento.radio_set.id == "selector_operacion":
            self._actualizar_etiqueta_boton_ejecutar()

    def on_button_pressed(self, evento: Button.Pressed) -> None:
        if evento.button.id == "btn_ejecutar":
            self._ejecutar_operacion()
        elif evento.button.id == "btn_limpiar":
            self._limpiar_formulario()
        elif evento.button.id == "btn_usar_resultado":
            self._usar_resultado_para_descifrar()
        elif evento.button.id == "btn_ver_pasos":
            self._ver_paso_a_paso()
        elif evento.button.id == "btn_volver":
            self.action_volver_menu()

    def _operacion_actual(self) -> str:
        selector = self.query_one("#selector_operacion", RadioSet)
        boton_presionado = selector.pressed_button
        if boton_presionado is not None and boton_presionado.id == "opcion_descifrar":
            return OPERACION_DESCIFRAR
        return OPERACION_CIFRAR

    def _actualizar_etiqueta_boton_ejecutar(self) -> None:
        boton = self.query_one("#btn_ejecutar", Button)
        if self._operacion_actual() == OPERACION_CIFRAR:
            boton.label = "CIFRAR MENSAJE"
        else:
            boton.label = "DESCIFRAR MENSAJE"

    def _ejecutar_operacion(self) -> None:
        mensaje = self.query_one("#input_mensaje", Input).value
        clave = self.query_one("#input_clave", Input).value
        operacion = self._operacion_actual()

        resultado_widget = self.query_one("#resultado", Static)
        advertencias_widget = self.query_one("#advertencias", Static)
        error_widget = self.query_one("#error_mensaje", Static)
        boton_usar_resultado = self.query_one("#btn_usar_resultado", Button)
        boton_ver_pasos = self.query_one("#btn_ver_pasos", Button)

        error_widget.update("")
        advertencias_widget.update("")

        try:
            mensaje_normalizado = playfair.normalizar_mensaje(mensaje)
            clave_normalizada = playfair.normalizar_clave(clave)

            if operacion == OPERACION_CIFRAR:
                digrafos = playfair.preparar_digrafos(mensaje_normalizado)
                mensaje_preparado = " ".join(digrafos)
                resultado = playfair.cifrar(mensaje, clave)
            else:
                if len(mensaje_normalizado) % 2 != 0:
                    raise ValueError(
                        "Un mensaje cifrado con Playfair debe tener una "
                        "cantidad par de letras."
                    )
                mensaje_preparado = " ".join(
                    mensaje_normalizado[indice : indice + 2]
                    for indice in range(0, len(mensaje_normalizado), 2)
                )
                resultado = playfair.descifrar(mensaje, clave)
        except ValueError as error:
            error_widget.update(str(error))
            resultado_widget.update("")
            boton_usar_resultado.disabled = True
            boton_ver_pasos.disabled = True
            self._ultimo_calculo = None
            return

        nombre_operacion = "Cifrado" if operacion == OPERACION_CIFRAR else "Descifrado"
        resultado_widget.update(
            f"Operación: {nombre_operacion} Playfair\n"
            f"Mensaje original: {mensaje}\n"
            f"Clave utilizada: {clave}  (normalizada: {clave_normalizada})\n"
            f"Mensaje normalizado (solo letras, I/J fusionadas): {mensaje_normalizado}\n"
            f"Mensaje preparado (dígrafos): {mensaje_preparado}\n"
            f"Resultado: {resultado}"
        )

        advertencias_widget.update(
            self._generar_advertencias(mensaje, mensaje_normalizado, mensaje_preparado)
        )

        self._ultimo_calculo = {
            "operacion": operacion,
            "mensaje_original": mensaje,
            "clave": clave,
            "clave_normalizada": clave_normalizada,
            "mensaje_normalizado": mensaje_normalizado,
            "digrafos": mensaje_preparado.split(),
            "resultado": resultado,
        }
        boton_ver_pasos.disabled = False

        if operacion == OPERACION_CIFRAR:
            self._ultimo_resultado_cifrado = resultado
            self._ultima_clave_usada = clave
            boton_usar_resultado.disabled = False
        else:
            boton_usar_resultado.disabled = True

    def _generar_advertencias(
        self, mensaje_original: str, mensaje_normalizado: str, mensaje_preparado: str
    ) -> str:
        advertencias = []

        if any(
            caracter.upper() not in playfair.ALFABETO_VALIDO
            for caracter in mensaje_original
        ):
            advertencias.append(
                "Playfair solo opera sobre las letras A-Z: los espacios, "
                "números, signos de puntuación y letras fuera de ese "
                "alfabeto (como Ñ o vocales con tilde: Á É Í Ó Ú) que "
                "ingresaste se descartaron y no aparecen en el resultado."
            )

        if "j" in mensaje_original.lower():
            advertencias.append(
                "La letra J no existe en la matriz Playfair: se trató como "
                "I (regla clásica del algoritmo)."
            )

        letras_preparadas = mensaje_preparado.replace(" ", "")
        if len(letras_preparadas) != len(mensaje_normalizado):
            advertencias.append(
                "Se insertaron letras de relleno (X o Q) para separar "
                "letras repetidas consecutivas o completar un dígrafo "
                "incompleto."
            )

        return "\n".join(f"⚠ {advertencia}" for advertencia in advertencias)

    def _limpiar_formulario(self) -> None:
        self.query_one("#input_mensaje", Input).value = ""
        self.query_one("#input_clave", Input).value = ""
        self.query_one("#resultado", Static).update("")
        self.query_one("#advertencias", Static).update("")
        self.query_one("#error_mensaje", Static).update("")
        self.query_one("#btn_usar_resultado", Button).disabled = True
        self.query_one("#btn_ver_pasos", Button).disabled = True
        self._ultimo_resultado_cifrado = None
        self._ultima_clave_usada = ""
        self._ultimo_calculo = None

    def _usar_resultado_para_descifrar(self) -> None:
        if self._ultimo_resultado_cifrado is None:
            return

        self.query_one("#opcion_descifrar", RadioButton).value = True
        self.query_one("#input_mensaje", Input).value = self._ultimo_resultado_cifrado
        self.query_one("#input_clave", Input).value = self._ultima_clave_usada

        self.query_one("#resultado", Static).update("")
        self.query_one("#advertencias", Static).update("")
        self.query_one("#error_mensaje", Static).update("")
        self.query_one("#btn_usar_resultado", Button).disabled = True
        self.query_one("#btn_ver_pasos", Button).disabled = True
        self._ultimo_calculo = None

        self._actualizar_etiqueta_boton_ejecutar()

    def _ver_paso_a_paso(self) -> None:
        if self._ultimo_calculo is None:
            return

        self.app.push_screen(
            PantallaPlayfairPasos(
                mensaje=self._ultimo_calculo["mensaje_original"],
                clave=self._ultimo_calculo["clave"],
                operacion=self._ultimo_calculo["operacion"],
            )
        )

    def action_volver_menu(self) -> None:
        self.app.pop_screen()
