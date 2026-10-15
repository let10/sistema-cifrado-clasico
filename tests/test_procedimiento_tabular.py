from algoritmos import cesar, sustitucion, vigenere


def test_pasos_de_cesar_incluyen_mapeo_y_operacion_por_caracter():
    pasos = cesar.generar_pasos("A B!", "3", True)

    assert len(pasos) == 3
    assert len(pasos[1].filas) == 26
    assert pasos[2].filas[0] == ("1", "A", "0", "(0 + 3) mod 26 = 3", "D")
    assert pasos[2].filas[1][-1] == " "
    assert pasos[2].filas[3][-1] == "!"


def test_pasos_de_sustitucion_muestran_equivalencias_y_caracteres():
    clave = "QWERTYUIOPASDFGHJKLZXCVBNM"
    pasos = sustitucion.generar_pasos("Ab!", clave, True)

    assert len(pasos) == 3
    assert len(pasos[1].filas) == 26
    assert pasos[1].filas[0] == ("0", "A", "Q")
    assert pasos[2].filas[0] == ("1", "A", "Sustitución directa", "Q")
    assert pasos[2].filas[-1][-1] == "!"


def test_pasos_de_vigenere_no_avanzan_clave_en_signos_y_espacios():
    pasos = vigenere.generar_pasos("A, B!", "SOL", True)

    assert len(pasos) == 3
    assert pasos[1].filas[0][2:4] == ("S", "Posición 1")
    assert pasos[1].filas[1][2:4] == ("-", "Se conserva; no consume clave")
    assert pasos[1].filas[3][2:4] == ("O", "Posición 2")
    assert pasos[2].filas[0][-1] == "S"
    assert pasos[2].filas[3][-1] == "P"
