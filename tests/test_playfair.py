"""Pruebas unitarias del motor criptográfico Playfair."""

import pytest

from algoritmos import playfair


def test_construir_matriz_elimina_duplicados_y_funde_i_j():
    matriz = playfair.construir_matriz("RADIO")
    letras_planas = [letra for fila in matriz for letra in fila]
    assert len(letras_planas) == 25
    assert len(set(letras_planas)) == 25
    assert "J" not in letras_planas

    matriz_con_repetidas = playfair.construir_matriz("BALLENA")
    letras_planas_repetidas = [letra for fila in matriz_con_repetidas for letra in fila]
    assert len(set(letras_planas_repetidas)) == 25


def test_matriz_radio_coincide_con_la_esperada():
    matriz = playfair.construir_matriz("RADIO")
    assert matriz == [
        list("RADIO"),
        list("BCEFG"),
        list("HKLMN"),
        list("PQSTU"),
        list("VWXYZ"),
    ]


def test_ejemplo_obligatorio_puesta_radio():
    cifrado = playfair.cifrar("PUESTA", "RADIO")
    assert cifrado == "QPLXQI"
    assert playfair.descifrar(cifrado, "RADIO") == "PUESTA"


def test_regla_misma_fila_desplaza_a_la_derecha():
    # P y U están en la misma fila de la matriz RADIO -> PU cifra a QP.
    assert playfair.cifrar("PU", "RADIO") == "QP"
    assert playfair.descifrar("QP", "RADIO") == "PU"


def test_regla_misma_columna_desplaza_hacia_abajo():
    # E y S comparten columna en la matriz RADIO -> ES cifra a LX.
    assert playfair.cifrar("ES", "RADIO") == "LX"
    assert playfair.descifrar("LX", "RADIO") == "ES"


def test_regla_rectangulo_intercambia_columnas():
    # T y A forman un rectángulo en la matriz RADIO -> TA cifra a QI.
    assert playfair.cifrar("TA", "RADIO") == "QI"
    assert playfair.descifrar("QI", "RADIO") == "TA"


def test_letras_repetidas_consecutivas_reciben_relleno():
    digrafos = playfair.preparar_digrafos("BALLENA")
    assert digrafos == ["BA", "LX", "LE", "NA"]


def test_relleno_alterno_cuando_la_repetida_es_la_letra_de_relleno_principal():
    digrafos = playfair.preparar_digrafos("TAXXON")
    assert digrafos == ["TA", "XQ", "XO", "NX"]


def test_mensaje_de_longitud_impar_recibe_relleno_final():
    digrafos = playfair.preparar_digrafos("AMOR")
    assert digrafos[-1][1] != digrafos[-1][0]

    digrafos_impar = playfair.preparar_digrafos("AMO")
    assert digrafos_impar == ["AM", "OX"]


def test_cifrado_ignora_espacios_numeros_y_signos():
    cifrado_con_formato = playfair.cifrar("PUE, STA 123!", "RADIO")
    cifrado_sin_formato = playfair.cifrar("PUESTA", "RADIO")
    assert cifrado_con_formato == cifrado_sin_formato


def test_clave_vacia_lanza_error():
    with pytest.raises(ValueError):
        playfair.cifrar("MENSAJE", "")


def test_clave_sin_letras_lanza_error():
    with pytest.raises(ValueError):
        playfair.cifrar("MENSAJE", "1234")


def test_mensaje_vacio_lanza_error():
    with pytest.raises(ValueError):
        playfair.cifrar("", "RADIO")


def test_mensaje_sin_letras_lanza_error():
    with pytest.raises(ValueError):
        playfair.cifrar("123 456", "RADIO")


def test_descifrar_mensaje_de_longitud_impar_lanza_error():
    with pytest.raises(ValueError):
        playfair.descifrar("ABC", "RADIO")


def test_cifrar_y_descifrar_es_consistente_con_distintas_claves():
    for clave in ("SOL", "CRIPTOGRAFIA", "LLUVIA", "ZORRO"):
        mensaje = "ENCRIPTACIONCLASICA"
        cifrado = playfair.cifrar(mensaje, clave)
        assert len(cifrado) % 2 == 0
        descifrado = playfair.descifrar(cifrado, clave)
        assert len(descifrado) == len(cifrado)


# --- Pruebas de generar_pasos (visualización educativa, Fase 3) ---


def test_generar_pasos_incluye_matriz_preparacion_y_un_paso_por_digrafo():
    pasos = playfair.generar_pasos("PUESTA", "RADIO", "cifrar")
    tipos = [paso["tipo"] for paso in pasos]
    assert tipos == ["matriz", "preparacion"] + ["digrafo"] * 3


def test_generar_pasos_paso_matriz_coincide_con_construir_matriz():
    pasos = playfair.generar_pasos("PUESTA", "RADIO", "cifrar")
    paso_matriz = pasos[0]
    assert paso_matriz["matriz"] == playfair.construir_matriz("RADIO")
    assert paso_matriz["clave_normalizada"] == "RADIO"
    assert paso_matriz["letras_clave"] == set("RADIO")


def test_generar_pasos_preparacion_muestra_los_digrafos_correctos():
    pasos = playfair.generar_pasos("PUESTA", "RADIO", "cifrar")
    paso_preparacion = pasos[1]
    assert paso_preparacion["mensaje_normalizado"] == "PUESTA"
    assert paso_preparacion["digrafos"] == ["PU", "ES", "TA"]


def test_generar_pasos_cifrar_reproduce_el_resultado_oficial_paso_a_paso():
    pasos = playfair.generar_pasos("PUESTA", "RADIO", "cifrar")
    pasos_digrafo = [paso for paso in pasos if paso["tipo"] == "digrafo"]

    assert [paso["digrafo_resultado"] for paso in pasos_digrafo] == ["QP", "LX", "QI"]
    assert [paso["regla"] for paso in pasos_digrafo] == [
        "misma_fila",
        "misma_columna",
        "rectangulo",
    ]
    assert pasos_digrafo[-1]["resultado_acumulado"] == "QPLXQI"
    assert pasos_digrafo[-1]["resultado_acumulado"] == playfair.cifrar("PUESTA", "RADIO")


def test_generar_pasos_descifrar_reproduce_el_mensaje_original_paso_a_paso():
    pasos = playfair.generar_pasos("QPLXQI", "RADIO", "descifrar")
    pasos_digrafo = [paso for paso in pasos if paso["tipo"] == "digrafo"]

    assert [paso["digrafo_resultado"] for paso in pasos_digrafo] == ["PU", "ES", "TA"]
    assert pasos_digrafo[-1]["resultado_acumulado"] == "PUESTA"
    assert pasos_digrafo[-1]["resultado_acumulado"] == playfair.descifrar(
        "QPLXQI", "RADIO"
    )


def test_generar_pasos_posiciones_coinciden_con_la_matriz():
    pasos = playfair.generar_pasos("PUESTA", "RADIO", "cifrar")
    matriz = pasos[0]["matriz"]
    paso_pu = next(p for p in pasos if p.get("digrafo_entrada") == "PU")

    fila1, columna1 = paso_pu["posiciones_entrada"][0]
    fila2, columna2 = paso_pu["posiciones_entrada"][1]
    assert matriz[fila1][columna1] == "P"
    assert matriz[fila2][columna2] == "U"

    fila1_r, columna1_r = paso_pu["posiciones_resultado"][0]
    fila2_r, columna2_r = paso_pu["posiciones_resultado"][1]
    assert matriz[fila1_r][columna1_r] == "Q"
    assert matriz[fila2_r][columna2_r] == "P"


def test_generar_pasos_marca_relleno_en_la_explicacion_de_preparacion():
    pasos = playfair.generar_pasos("BALLENA", "RADIO", "cifrar")
    paso_preparacion = pasos[1]
    assert "relleno" in paso_preparacion["explicacion"].lower()
    assert paso_preparacion["digrafos"] == ["BA", "LX", "LE", "NA"]


def test_generar_pasos_sin_relleno_no_lo_menciona():
    pasos = playfair.generar_pasos("PUESTA", "RADIO", "cifrar")
    paso_preparacion = pasos[1]
    assert "relleno" not in paso_preparacion["explicacion"].lower()


def test_generar_pasos_operacion_invalida_lanza_error():
    with pytest.raises(ValueError):
        playfair.generar_pasos("PUESTA", "RADIO", "voltear")


def test_generar_pasos_propaga_errores_de_clave_y_mensaje():
    with pytest.raises(ValueError):
        playfair.generar_pasos("PUESTA", "", "cifrar")
    with pytest.raises(ValueError):
        playfair.generar_pasos("", "RADIO", "cifrar")


def test_generar_pasos_descifrar_longitud_impar_lanza_error():
    with pytest.raises(ValueError):
        playfair.generar_pasos("ABC", "RADIO", "descifrar")


# --- Letras fuera de A-Z: Ñ y vocales con tilde (bug encontrado en uso real) ---


@pytest.mark.parametrize("palabra", ["NIÑO", "MAÑANA", "CAFÉ", "ÁRBOL", "ÚNICO"])
def test_letras_fuera_de_a_z_se_descartan_sin_lanzar_error(palabra):
    cifrado = playfair.cifrar(palabra, "RADIO")
    assert playfair.descifrar(cifrado, "RADIO")


def test_enie_no_pertenece_al_mensaje_normalizado():
    assert "Ñ" not in playfair.normalizar_mensaje("NIÑO")


def test_vocales_con_tilde_no_pertenecen_al_mensaje_normalizado():
    normalizado = playfair.normalizar_mensaje("ÁÉÍÓÚÜ CASA")
    assert normalizado == "CASA"


def test_clave_con_enie_descarta_la_enie_y_usa_el_resto():
    assert playfair.normalizar_clave("AÑO") == "AO"
