"""Pruebas funcionales de la visualización paso a paso de Playfair.

Nota técnica: Button de Textual ignora una segunda pulsación sobre el
mismo botón mientras dura su animación "activa" (~0.2s, ver
``Button.active_effect_duration``). Esto no afecta el uso real (un
clic humano siempre tarda más que eso), pero en las pruebas hay que
esperar ese tiempo entre dos clics consecutivos al MISMO botón con
``await pilot.pause(0.25)`` en vez de ``await pilot.pause()`` sin
argumentos.
"""

import pytest

from interfaz.aplicacion import SistemaEncriptacionClasica
from interfaz.pantallas.playfair import PantallaPlayfair
from textual.widgets import Button, Static

TAMANO_PANTALLA = (110, 50)
ESPERA_ENTRE_CLICS_AL_MISMO_BOTON = 0.25


async def _preparar_cifrado_y_abrir_pasos(pilot, mensaje="PUESTA", clave="RADIO"):
    await pilot.click("#btn_playfair")
    await pilot.pause()
    pilot.app.screen.query_one("#input_mensaje").value = mensaje
    pilot.app.screen.query_one("#input_clave").value = clave
    await pilot.pause()
    await pilot.click("#btn_ejecutar")
    await pilot.pause()
    await pilot.click("#btn_ver_pasos")
    await pilot.pause()


@pytest.mark.asyncio
async def test_boton_ver_pasos_deshabilitado_hasta_ejecutar_una_operacion():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await pilot.click("#btn_playfair")
        await pilot.pause()
        assert pilot.app.screen.query_one("#btn_ver_pasos", Button).disabled


@pytest.mark.asyncio
async def test_ver_pasos_abre_la_pantalla_de_visualizacion():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        from interfaz.pantallas.playfair_pasos import PantallaPlayfairPasos

        assert isinstance(app.screen, PantallaPlayfairPasos)


@pytest.mark.asyncio
async def test_primer_paso_muestra_la_construccion_de_la_matriz():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        contenido = str(pilot.app.screen.query_one("#contenido_paso", Static).content)
        assert "Construcción de la matriz" in contenido
        assert "Paso 1 de 5" in str(
            pilot.app.screen.query_one("#indicador_progreso", Static).content
        )


@pytest.mark.asyncio
async def test_boton_anterior_deshabilitado_en_el_primer_paso():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        assert pilot.app.screen.query_one("#btn_anterior", Button).disabled
        assert not pilot.app.screen.query_one("#btn_siguiente", Button).disabled


@pytest.mark.asyncio
async def test_siguiente_avanza_por_todos_los_pasos_en_orden():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        pantalla = pilot.app.screen

        titulos_esperados = [
            "Construcción de la matriz",
            "Preparación del mensaje",
            "Dígrafo 1 de 3: PU",
            "Dígrafo 2 de 3: ES",
            "Dígrafo 3 de 3: TA",
        ]

        for indice, fragmento in enumerate(titulos_esperados):
            contenido = str(pantalla.query_one("#contenido_paso", Static).content)
            assert fragmento in contenido
            if indice < len(titulos_esperados) - 1:
                await pilot.click("#btn_siguiente")
                await pilot.pause(ESPERA_ENTRE_CLICS_AL_MISMO_BOTON)

        assert pantalla.query_one("#btn_siguiente", Button).disabled


@pytest.mark.asyncio
async def test_anterior_retrocede_despues_de_avanzar():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        pantalla = pilot.app.screen

        await pilot.click("#btn_siguiente")
        await pilot.pause(ESPERA_ENTRE_CLICS_AL_MISMO_BOTON)
        await pilot.click("#btn_siguiente")
        await pilot.pause(ESPERA_ENTRE_CLICS_AL_MISMO_BOTON)
        assert pantalla._indice == 2

        await pilot.click("#btn_anterior")
        await pilot.pause(ESPERA_ENTRE_CLICS_AL_MISMO_BOTON)
        assert pantalla._indice == 1
        contenido = str(pantalla.query_one("#contenido_paso", Static).content)
        assert "Preparación del mensaje" in contenido


@pytest.mark.asyncio
async def test_flechas_del_teclado_navegan_los_pasos():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        pantalla = pilot.app.screen

        await pilot.press("right")
        await pilot.pause()
        assert pantalla._indice == 1

        await pilot.press("right")
        await pilot.pause()
        assert pantalla._indice == 2

        await pilot.press("left")
        await pilot.pause()
        assert pantalla._indice == 1


@pytest.mark.asyncio
async def test_mostrar_todo_concatena_todos_los_pasos_y_deshabilita_navegacion():
    # "Mostrar todo" concatena los 5 pasos y el contenido crece mucho más
    # que con un solo paso, así que se usa una terminal más alta para que
    # los botones sigan siendo clickeables sin necesidad de hacer scroll.
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=(110, 90)) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        await pilot.click("#btn_mostrar_todo")
        await pilot.pause(ESPERA_ENTRE_CLICS_AL_MISMO_BOTON)

        pantalla = pilot.app.screen
        contenido = str(pantalla.query_one("#contenido_paso", Static).content)
        assert "Construcción de la matriz" in contenido
        assert "Dígrafo 1 de 3: PU" in contenido
        assert "Dígrafo 2 de 3: ES" in contenido
        assert "Dígrafo 3 de 3: TA" in contenido
        assert pantalla.query_one("#btn_anterior", Button).disabled
        assert pantalla.query_one("#btn_siguiente", Button).disabled

        await pilot.click("#btn_mostrar_todo")
        await pilot.pause(ESPERA_ENTRE_CLICS_AL_MISMO_BOTON)
        assert not pantalla._mostrar_todo


@pytest.mark.asyncio
async def test_volver_al_resultado_regresa_a_pantalla_playfair():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        await pilot.click("#btn_volver_resultado")
        await pilot.pause()
        assert isinstance(app.screen, PantallaPlayfair)


@pytest.mark.asyncio
async def test_escape_vuelve_al_resultado():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _preparar_cifrado_y_abrir_pasos(pilot)
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, PantallaPlayfair)


@pytest.mark.asyncio
async def test_pasos_funciona_tambien_para_descifrar():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await pilot.click("#btn_playfair")
        await pilot.pause()
        pilot.app.screen.query_one("#opcion_descifrar").value = True
        await pilot.pause()
        pilot.app.screen.query_one("#input_mensaje").value = "QPLXQI"
        pilot.app.screen.query_one("#input_clave").value = "RADIO"
        await pilot.pause()
        await pilot.click("#btn_ejecutar")
        await pilot.pause()
        await pilot.click("#btn_ver_pasos")
        await pilot.pause()

        pantalla = pilot.app.screen
        for _ in range(4):
            await pilot.click("#btn_siguiente")
            await pilot.pause(ESPERA_ENTRE_CLICS_AL_MISMO_BOTON)

        contenido = str(pantalla.query_one("#contenido_paso", Static).content)
        assert "Resultado acumulado: PUESTA" in contenido
