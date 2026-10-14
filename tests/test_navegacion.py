"""Pruebas funcionales de navegación de la interfaz principal.

Ejecutar con: python3 -m pytest tests/ -v
"""

import pytest

from interfaz.aplicacion import SistemaEncriptacionClasica
from interfaz.pantallas.menu_principal import PantallaMenuPrincipal
from interfaz.pantallas.modulo_pendiente import PantallaModuloPendiente
from interfaz.pantallas.playfair import PantallaPlayfair


@pytest.mark.asyncio
async def test_menu_principal_se_muestra_al_iniciar():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.screen, PantallaMenuPrincipal)


@pytest.mark.asyncio
async def test_menu_principal_tiene_los_cinco_botones():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.pause()
        ids_esperados = {
            "btn_playfair",
            "btn_vigenere",
            "btn_cesar",
            "btn_sustitucion",
            "btn_salir",
        }
        ids_encontrados = {boton.id for boton in app.screen.query("Button")}
        assert ids_esperados == ids_encontrados


@pytest.mark.asyncio
async def test_boton_playfair_abre_la_pantalla_funcional_de_playfair():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_playfair")
        await pilot.pause()
        assert isinstance(app.screen, PantallaPlayfair)


@pytest.mark.asyncio
async def test_boton_vigenere_abre_pantalla_de_modulo():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_vigenere")
        await pilot.pause()
        assert isinstance(app.screen, PantallaModuloPendiente)
        assert app.screen.nombre_modulo == "VIGENÈRE"


@pytest.mark.asyncio
async def test_boton_cesar_abre_pantalla_de_modulo():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_cesar")
        await pilot.pause()
        assert isinstance(app.screen, PantallaModuloPendiente)
        assert app.screen.nombre_modulo == "CÉSAR"


@pytest.mark.asyncio
async def test_boton_sustitucion_abre_pantalla_de_modulo():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_sustitucion")
        await pilot.pause()
        assert isinstance(app.screen, PantallaModuloPendiente)
        assert app.screen.nombre_modulo == "SUSTITUCIÓN SIMPLE"


@pytest.mark.asyncio
async def test_volver_al_menu_desde_playfair():
    # La pantalla de Playfair es un formulario más alto que el menú y usa
    # overflow-y: auto; se prueba con un tamaño realista en vez del
    # tamaño mínimo por defecto (80x24) para que el botón sea clickeable.
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=(100, 45)) as pilot:
        await pilot.click("#btn_playfair")
        await pilot.pause()
        await pilot.click("#btn_volver")
        await pilot.pause()
        assert isinstance(app.screen, PantallaMenuPrincipal)


@pytest.mark.asyncio
async def test_escape_vuelve_al_menu_desde_modulo_pendiente():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_vigenere")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, PantallaMenuPrincipal)


@pytest.mark.asyncio
async def test_boton_salir_cierra_la_aplicacion():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_salir")
        await pilot.pause()
        assert not app.is_running
