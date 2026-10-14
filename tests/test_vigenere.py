import pytest

from algoritmos import vigenere


def test_cifrar_y_descifrar_mensaje_de_referencia():
    mensaje = "CRIPTOGRAFIA"
    cifrado = vigenere.cifrar(mensaje, "SOL")

    assert cifrado == "UFTHHZYFLXWL"
    assert vigenere.descifrar(cifrado, "SOL") == mensaje


def test_conserva_mayusculas_minusculas_y_no_letras_sin_avanzar_clave():
    mensaje = "A, b! 2c"

    cifrado = vigenere.cifrar(mensaje, "BC")

    assert cifrado == "B, d! 2d"
    assert vigenere.descifrar(cifrado, "BC") == mensaje


@pytest.mark.parametrize("clave", ["", "   ", "CLAVE 2", "SOL!"])
def test_rechaza_claves_vacias_o_que_no_sean_solo_letras_ascii(clave):
    with pytest.raises(ValueError):
        vigenere.cifrar("MENSAJE", clave)


def test_procedimiento_indica_clave_y_caracteres_que_no_avanzan():
    procedimiento = vigenere.obtener_procedimiento("A B", "SOL", True)

    assert "Clave normalizada" in procedimiento
    assert "no letras no avanzan la clave" in procedimiento
    assert any(
        fila.startswith("| 2 ") and "no aplica" in fila
        for fila in procedimiento.splitlines()
    )
