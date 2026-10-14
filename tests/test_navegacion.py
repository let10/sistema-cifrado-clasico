"""Pruebas funcionales de navegación de la interfaz principal.

Ejecutar con: python3 -m pytest tests/ -v
"""

import pytest

from interfaz.aplicacion import SistemaEncriptacionClasica
from interfaz.pantallas.menu_principal import PantallaMenuPrincipal
from interfaz.pantallas.modulo_cesar import PantallaModuloCesar
from interfaz.pantallas.modulo_pendiente import PantallaModuloPendiente
from interfaz.pantallas.modulo_sustitucion import PantallaModuloSustitucion
from interfaz.pantallas.modulo_vigenere import PantallaModuloVigenere


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
async def test_boton_playfair_abre_pantalla_de_modulo():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_playfair")
        await pilot.pause()
        assert isinstance(app.screen, PantallaModuloPendiente)
        assert app.screen.nombre_modulo == "PLAYFAIR"


@pytest.mark.asyncio
async def test_boton_vigenere_abre_pantalla_de_modulo():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_vigenere")
        await pilot.pause()
        assert isinstance(app.screen, PantallaModuloVigenere)


@pytest.mark.asyncio
async def test_boton_cesar_abre_pantalla_de_modulo():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_cesar")
        await pilot.pause()
        assert isinstance(app.screen, PantallaModuloCesar)


@pytest.mark.asyncio
async def test_boton_sustitucion_abre_pantalla_de_modulo():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_sustitucion")
        await pilot.pause()
        assert isinstance(app.screen, PantallaModuloSustitucion)


@pytest.mark.asyncio
async def test_volver_al_menu_desde_modulo_pendiente():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
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
async def test_vigenere_cifra_y_muestra_procedimiento_solo_si_se_activa():
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=(110, 45)) as pilot:
        await pilot.click("#btn_vigenere")
        await pilot.pause()
        app.screen.query_one("#input_mensaje").value = "CRIPTOGRAFIA"
        app.screen.query_one("#input_clave").value = "SOL"
        await pilot.click("#btn_cifrar")
        await pilot.pause()

        resultado = str(app.screen.query_one("#resultado").render())
        assert "METODO: Vigenere" in str(resultado)
        assert "PROCEDIMIENTO" not in str(resultado)

        await pilot.click("#mostrar_procedimiento")
        await pilot.click("#btn_cifrar")
        await pilot.pause()
        resultado = str(app.screen.query_one("#resultado").render())
        assert "PROCEDIMIENTO - CIFRADO VIGENERE" in str(resultado)
        assert "TRANSFORMACION CARACTER POR CARACTER" in str(resultado)


@pytest.mark.asyncio
async def test_boton_salir_cierra_la_aplicacion():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_salir")
        await pilot.pause()
        assert not app.is_running
