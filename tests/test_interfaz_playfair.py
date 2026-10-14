"""Pruebas funcionales de la pantalla de Playfair.

Ejecutar con: python3 -m pytest tests/test_interfaz_playfair.py -v
"""

import pytest

from interfaz.aplicacion import SistemaEncriptacionClasica
from interfaz.pantallas.menu_principal import PantallaMenuPrincipal
from interfaz.pantallas.playfair import PantallaPlayfair
from textual.widgets import Button, Input, Static

TAMANO_PANTALLA = (100, 45)


async def _abrir_pantalla_playfair(pilot):
    await pilot.click("#btn_playfair")
    await pilot.pause()


async def _escribir(pilot, id_campo: str, texto: str) -> None:
    campo = pilot.app.screen.query_one(id_campo, Input)
    campo.value = texto
    await pilot.pause()


@pytest.mark.asyncio
async def test_cifrar_mensaje_muestra_resultado_correcto():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)
        await _escribir(pilot, "#input_mensaje", "PUESTA")
        await _escribir(pilot, "#input_clave", "RADIO")
        await pilot.click("#btn_ejecutar")
        await pilot.pause()

        resultado = pilot.app.screen.query_one("#resultado", Static).content
        assert "QPLXQI" in str(resultado)
        assert "Cifrado Playfair" in str(resultado)


@pytest.mark.asyncio
async def test_descifrar_mensaje_recupera_el_original():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)

        pilot.app.screen.query_one("#opcion_descifrar").value = True
        await pilot.pause()

        await _escribir(pilot, "#input_mensaje", "QPLXQI")
        await _escribir(pilot, "#input_clave", "RADIO")
        await pilot.click("#btn_ejecutar")
        await pilot.pause()

        resultado = str(pilot.app.screen.query_one("#resultado", Static).content)
        assert "PUESTA" in resultado
        assert "Descifrado Playfair" in resultado


@pytest.mark.asyncio
async def test_boton_ejecutar_cambia_de_etiqueta_segun_la_operacion():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)
        boton = pilot.app.screen.query_one("#btn_ejecutar", Button)
        assert str(boton.label) == "CIFRAR MENSAJE"

        pilot.app.screen.query_one("#opcion_descifrar").value = True
        await pilot.pause()
        assert str(boton.label) == "DESCIFRAR MENSAJE"


@pytest.mark.asyncio
async def test_clave_vacia_muestra_error_y_no_rompe_la_aplicacion():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)
        await _escribir(pilot, "#input_mensaje", "HOLA")
        await _escribir(pilot, "#input_clave", "")
        await pilot.click("#btn_ejecutar")
        await pilot.pause()

        error = str(pilot.app.screen.query_one("#error_mensaje", Static).content)
        assert "clave" in error.lower()
        assert pilot.app.is_running


@pytest.mark.asyncio
async def test_advertencia_por_caracteres_descartados():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)
        await _escribir(pilot, "#input_mensaje", "HOLA, MUNDO 123!")
        await _escribir(pilot, "#input_clave", "RADIO")
        await pilot.click("#btn_ejecutar")
        await pilot.pause()

        advertencias = str(
            pilot.app.screen.query_one("#advertencias", Static).content
        )
        assert "descartaron" in advertencias.lower()


@pytest.mark.asyncio
async def test_mensaje_con_enie_y_tildes_no_produce_error_y_avisa_el_descarte():
    # Bug real encontrado en uso: .isalpha() de Python acepta Ñ/Á/É/Í/Ó/Ú
    # como "letra", pero la matriz Playfair solo tiene A-Z, así que el
    # motor lanzaba un error al cifrar cualquier palabra en español con
    # tilde o eñe. Debe descartarse como cualquier otro carácter fuera
    # de A-Z, sin error, y la advertencia debe mencionarlo.
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)
        await _escribir(pilot, "#input_mensaje", "NIÑO PEQUEÑO")
        await _escribir(pilot, "#input_clave", "RADIO")
        await pilot.click("#btn_ejecutar")
        await pilot.pause()

        error = str(pilot.app.screen.query_one("#error_mensaje", Static).content)
        assert error == ""

        resultado = str(pilot.app.screen.query_one("#resultado", Static).content)
        assert "Ñ" not in resultado.split("Resultado:")[-1]

        advertencias = str(
            pilot.app.screen.query_one("#advertencias", Static).content
        )
        assert "Ñ" in advertencias


@pytest.mark.asyncio
async def test_boton_usar_resultado_cambia_a_descifrar_con_el_texto_cifrado():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)
        await _escribir(pilot, "#input_mensaje", "PUESTA")
        await _escribir(pilot, "#input_clave", "RADIO")
        await pilot.click("#btn_ejecutar")
        await pilot.pause()

        boton_usar_resultado = pilot.app.screen.query_one("#btn_usar_resultado", Button)
        assert not boton_usar_resultado.disabled

        await pilot.click("#btn_usar_resultado")
        await pilot.pause()

        assert pilot.app.screen.query_one("#opcion_descifrar").value is True
        assert pilot.app.screen.query_one("#input_mensaje", Input).value == "QPLXQI"
        assert pilot.app.screen.query_one("#input_clave", Input).value == "RADIO"

        await pilot.click("#btn_ejecutar")
        await pilot.pause()

        resultado = str(pilot.app.screen.query_one("#resultado", Static).content)
        assert "PUESTA" in resultado


@pytest.mark.asyncio
async def test_boton_limpiar_resetea_el_formulario():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)
        await _escribir(pilot, "#input_mensaje", "PUESTA")
        await _escribir(pilot, "#input_clave", "RADIO")
        await pilot.click("#btn_ejecutar")
        await pilot.pause()

        await pilot.click("#btn_limpiar")
        await pilot.pause()

        assert pilot.app.screen.query_one("#input_mensaje", Input).value == ""
        assert pilot.app.screen.query_one("#input_clave", Input).value == ""
        assert str(pilot.app.screen.query_one("#resultado", Static).content) == ""
        assert pilot.app.screen.query_one("#btn_usar_resultado", Button).disabled


@pytest.mark.asyncio
async def test_escape_vuelve_al_menu_desde_playfair():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=TAMANO_PANTALLA) as pilot:
        await _abrir_pantalla_playfair(pilot)
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, PantallaMenuPrincipal)
