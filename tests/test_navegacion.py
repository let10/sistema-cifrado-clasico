"""Pruebas funcionales de navegación de la interfaz principal.

Ejecutar con: python3 -m pytest tests/ -v
"""

import pytest
from textual.widgets import Static, Switch
from textual.widgets import DataTable

from interfaz.aplicacion import SistemaEncriptacionClasica
from interfaz.pantallas.menu_principal import PantallaMenuPrincipal
from interfaz.pantallas.modulo_cesar import PantallaModuloCesar
from interfaz.pantallas.playfair import PantallaPlayfair
from interfaz.pantallas.modulo_sustitucion import PantallaModuloSustitucion
from interfaz.pantallas.modulo_vigenere import PantallaModuloVigenere
from interfaz.pantallas.procedimiento import PantallaProcedimiento


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
async def test_volver_al_menu_desde_playfair():
    # La pantalla de Playfair es un formulario más alto que el menú y usa
    # overflow-y: auto; se prueba con un tamaño realista en vez del
    # tamaño mínimo por defecto (80x24) para que el botón sea clickeable.
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=(100, 45)) as pilot:
        await pilot.click("#btn_playfair")
        await pilot.pause()
        boton = app.screen.query_one("#btn_volver")
        boton.scroll_visible(animate=False, immediate=True)
        await pilot.pause()
        assert await pilot.click("#btn_volver")
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
        interruptor = app.screen.query_one("#mostrar_procedimiento", Switch)
        estado = app.screen.query_one("#estado_procedimiento", Static)
        assert not interruptor.value
        assert str(estado.render()) == "PASOS: NO"

        app.screen.query_one("#input_mensaje").value = "CRIPTOGRAFIA"
        app.screen.query_one("#input_clave").value = "SOL"
        await pilot.click("#btn_cifrar")
        await pilot.pause()

        resultado = str(app.screen.query_one("#resultado").render())
        assert "ALGORITMO: Vigenère" in str(resultado)
        assert "PROCEDIMIENTO" not in str(resultado)
        assert not isinstance(app.screen, PantallaProcedimiento)
        assert not app.screen.query_one("#btn_ver_procedimiento").disabled

        await pilot.click("#mostrar_procedimiento")
        await pilot.pause()
        assert interruptor.value
        assert str(estado.render()) == "PASOS: SI"
        assert estado.has_class("procedimiento-activo")
        await pilot.click("#btn_cifrar")
        await pilot.pause()
        assert isinstance(app.screen, PantallaProcedimiento)
        assert str(app.screen.query_one("#titulo_paso", Static).render()) == (
            "Datos de la operación"
        )
        tabla = app.screen.query_one("#tabla_procedimiento", DataTable)
        assert tabla.row_count == 4

        await pilot.click("#btn_siguiente")
        await pilot.pause(0.25)
        assert str(app.screen.query_one("#titulo_paso", Static).render()) == (
            "Alineación de la clave"
        )
        assert app.screen.query_one("#tabla_procedimiento", DataTable).row_count == 12

        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, PantallaModuloVigenere)

        await pilot.click("#mostrar_procedimiento")
        await pilot.pause()
        assert not interruptor.value
        assert str(estado.render()) == "PASOS: NO"
        assert not estado.has_class("procedimiento-activo")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("boton_menu", "mensaje", "clave", "algoritmo"),
    [
        ("#btn_cesar", "HOLA", "3", "César"),
        (
            "#btn_sustitucion",
            "HOLA",
            "QWERTYUIOPASDFGHJKLZXCVBNM",
            "Sustitución simple",
        ),
    ],
)
async def test_cesar_y_sustitucion_muestran_procedimiento_en_tabla(
    boton_menu, mensaje, clave, algoritmo
):
    app = SistemaEncriptacionClasica()
    async with app.run_test(size=(110, 50)) as pilot:
        await pilot.click(boton_menu)
        await pilot.pause()
        app.screen.query_one("#input_mensaje").value = mensaje
        app.screen.query_one("#input_clave").value = clave
        await pilot.click("#btn_cifrar")
        await pilot.pause()

        resultado = str(app.screen.query_one("#resultado").render())
        assert f"ALGORITMO: {algoritmo}" in resultado
        assert not isinstance(app.screen, PantallaProcedimiento)

        await pilot.click("#btn_ver_procedimiento")
        await pilot.pause()
        assert isinstance(app.screen, PantallaProcedimiento)
        assert app.screen.query_one("#tabla_procedimiento", DataTable).row_count > 0


@pytest.mark.asyncio
async def test_boton_salir_cierra_la_aplicacion():
    app = SistemaEncriptacionClasica()
    async with app.run_test() as pilot:
        await pilot.click("#btn_salir")
        await pilot.pause()
        assert not app.is_running
