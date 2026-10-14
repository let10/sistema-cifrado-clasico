"""Motor criptográfico del cifrado Playfair.

Responsable: Integrante 1.

Construye dinámicamente una matriz 5x5 a partir de la clave y aplica
las reglas clásicas de Playfair (misma fila, misma columna,
rectángulo) sobre el mensaje separado en dígrafos.

Playfair es un cifrado clásico que opera únicamente sobre las 26
letras del alfabeto inglés A-Z (con I/J fusionadas en una sola
celda). A diferencia de César, sustitución simple o Vigenère, no es
posible conservar espacios, números ni signos de puntuación sin
romper la estructura de dígrafos de 2 letras: por eso el mensaje se
normaliza eliminando todo carácter que no sea una letra A-Z. Esto
incluye letras propias del español que no existen en esa matriz de
25 celdas, como Ñ y las vocales con tilde (Á, É, Í, Ó, Ú, Ü): se
descartan igual que un espacio o un signo de puntuación, nunca
provocan un error. El descifrado recupera el mensaje "preparado" (el
que realmente se cifró, con posibles letras de relleno insertadas),
no necesariamente el texto exacto que el usuario escribió
originalmente si este contenía espacios, signos, números, letras
fuera de A-Z o letras dobles que requirieron relleno.

Flujo de transformación de un mensaje:
    mensaje original   -> tal como lo escribe el usuario.
    mensaje normalizado -> solo letras A-Z, en mayúsculas, J fundida en I.
    mensaje preparado   -> normalizado, separado en dígrafos válidos
                            (sin pares de letras repetidas, longitud par).
"""

import string

TAMANO_MATRIZ = 5
LETRA_RELLENO_PRINCIPAL = "X"
LETRA_RELLENO_ALTERNA = "Q"

OPERACION_CIFRAR = "cifrar"
OPERACION_DESCIFRAR = "descifrar"

NOMBRES_REGLA = {
    "misma_fila": "Misma fila",
    "misma_columna": "Misma columna",
    "rectangulo": "Rectángulo",
}

ALFABETO_VALIDO = frozenset(string.ascii_uppercase)


def normalizar_clave(clave: str) -> str:
    """Convierte la clave a mayúsculas, funde I/J y descarta no-letras y repetidas.

    Solo se consideran válidas las 26 letras A-Z. Cualquier otro
    carácter (espacios, números, signos, o letras fuera de ese
    alfabeto como Ñ o vocales con tilde) se descarta sin generar error.
    """
    if clave is None or not clave.strip():
        raise ValueError("La clave no puede estar vacía.")

    letras_sin_repetir = []
    for caracter in clave.upper():
        if caracter not in ALFABETO_VALIDO:
            continue
        letra = "I" if caracter == "J" else caracter
        if letra not in letras_sin_repetir:
            letras_sin_repetir.append(letra)

    if not letras_sin_repetir:
        raise ValueError("La clave debe contener al menos una letra A-Z.")

    return "".join(letras_sin_repetir)


def normalizar_mensaje(mensaje: str) -> str:
    """Convierte el mensaje a mayúsculas, funde I/J y conserva solo letras A-Z.

    Cualquier carácter fuera de A-Z (espacios, números, signos, o
    letras como Ñ y vocales con tilde) se descarta sin generar error,
    igual que para ``normalizar_clave``.
    """
    if mensaje is None or not mensaje.strip():
        raise ValueError("El mensaje no puede estar vacío.")

    letras = [
        "I" if caracter == "J" else caracter
        for caracter in mensaje.upper()
        if caracter in ALFABETO_VALIDO
    ]

    if not letras:
        raise ValueError(
            "El mensaje debe contener al menos una letra para aplicar Playfair."
        )

    return "".join(letras)


def construir_matriz(clave: str) -> list:
    """Genera la matriz 5x5 (lista de 5 filas de 5 letras) a partir de la clave."""
    clave_normalizada = normalizar_clave(clave)
    alfabeto_sin_j = [letra for letra in string.ascii_uppercase if letra != "J"]

    letras_matriz = list(clave_normalizada)
    for letra in alfabeto_sin_j:
        if letra not in letras_matriz:
            letras_matriz.append(letra)

    return [
        letras_matriz[fila * TAMANO_MATRIZ : (fila + 1) * TAMANO_MATRIZ]
        for fila in range(TAMANO_MATRIZ)
    ]


def localizar_letra(matriz: list, letra: str) -> tuple:
    """Devuelve la posición (fila, columna) de una letra dentro de la matriz."""
    for fila in range(TAMANO_MATRIZ):
        for columna in range(TAMANO_MATRIZ):
            if matriz[fila][columna] == letra:
                return fila, columna
    raise ValueError(f"La letra '{letra}' no pertenece al alfabeto de la matriz.")


def preparar_digrafos(mensaje_normalizado: str) -> list:
    """Separa el mensaje normalizado en dígrafos válidos para Playfair.

    Inserta una letra de relleno entre dos letras iguales consecutivas
    y, si queda una letra sola al final, la completa con relleno.
    """
    letras = list(mensaje_normalizado)
    digrafos = []
    indice = 0

    while indice < len(letras):
        primera = letras[indice]
        hay_siguiente = indice + 1 < len(letras)
        segunda = letras[indice + 1] if hay_siguiente else None

        if not hay_siguiente or primera == segunda:
            relleno = (
                LETRA_RELLENO_ALTERNA
                if primera == LETRA_RELLENO_PRINCIPAL
                else LETRA_RELLENO_PRINCIPAL
            )
            digrafos.append(primera + relleno)
            indice += 1
        else:
            digrafos.append(primera + segunda)
            indice += 2

    return digrafos


def _resolver_digrafo(matriz: list, digrafo: str, operacion: str) -> dict:
    """Aplica la regla geométrica de Playfair sobre un dígrafo.

    Es el único lugar donde viven las reglas de misma fila, misma
    columna y rectángulo; tanto ``cifrar``/``descifrar`` como
    ``generar_pasos`` reutilizan esta función para no duplicar la
    lógica geométrica.
    """
    fila1, columna1 = localizar_letra(matriz, digrafo[0])
    fila2, columna2 = localizar_letra(matriz, digrafo[1])
    paso = 1 if operacion == OPERACION_CIFRAR else -1

    if fila1 == fila2:
        regla = "misma_fila"
        columna1_resultado = (columna1 + paso) % TAMANO_MATRIZ
        columna2_resultado = (columna2 + paso) % TAMANO_MATRIZ
        resultado = matriz[fila1][columna1_resultado] + matriz[fila2][columna2_resultado]
        posiciones_resultado = [(fila1, columna1_resultado), (fila2, columna2_resultado)]

    elif columna1 == columna2:
        regla = "misma_columna"
        fila1_resultado = (fila1 + paso) % TAMANO_MATRIZ
        fila2_resultado = (fila2 + paso) % TAMANO_MATRIZ
        resultado = matriz[fila1_resultado][columna1] + matriz[fila2_resultado][columna2]
        posiciones_resultado = [(fila1_resultado, columna1), (fila2_resultado, columna2)]

    else:
        regla = "rectangulo"
        resultado = matriz[fila1][columna2] + matriz[fila2][columna1]
        posiciones_resultado = [(fila1, columna2), (fila2, columna1)]

    return {
        "resultado": resultado,
        "regla": regla,
        "posiciones_entrada": [(fila1, columna1), (fila2, columna2)],
        "posiciones_resultado": posiciones_resultado,
    }


def cifrar(mensaje: str, clave: str) -> str:
    """Cifra un mensaje con Playfair. Devuelve siempre longitud par."""
    matriz = construir_matriz(clave)
    mensaje_normalizado = normalizar_mensaje(mensaje)
    digrafos = preparar_digrafos(mensaje_normalizado)
    return "".join(
        _resolver_digrafo(matriz, digrafo, OPERACION_CIFRAR)["resultado"]
        for digrafo in digrafos
    )


def descifrar(mensaje: str, clave: str) -> str:
    """Descifra un mensaje cifrado con Playfair (debe tener longitud par)."""
    matriz = construir_matriz(clave)
    mensaje_normalizado = normalizar_mensaje(mensaje)

    if len(mensaje_normalizado) % 2 != 0:
        raise ValueError(
            "Un mensaje cifrado con Playfair debe tener una cantidad par de letras."
        )

    digrafos = [
        mensaje_normalizado[indice : indice + 2]
        for indice in range(0, len(mensaje_normalizado), 2)
    ]
    return "".join(
        _resolver_digrafo(matriz, digrafo, OPERACION_DESCIFRAR)["resultado"]
        for digrafo in digrafos
    )


def _explicar_regla(digrafo: str, analisis: dict, operacion: str) -> str:
    letra1, letra2 = digrafo[0], digrafo[1]
    resultado1, resultado2 = analisis["resultado"][0], analisis["resultado"][1]

    if analisis["regla"] == "misma_fila":
        direccion = "derecha" if operacion == OPERACION_CIFRAR else "izquierda"
        return (
            f"{letra1} y {letra2} están en la misma fila. Se desplaza cada "
            f"letra una posición hacia la {direccion}: "
            f"{letra1}→{resultado1}, {letra2}→{resultado2}."
        )

    if analisis["regla"] == "misma_columna":
        direccion = "abajo" if operacion == OPERACION_CIFRAR else "arriba"
        return (
            f"{letra1} y {letra2} están en la misma columna. Se desplaza "
            f"cada letra una posición hacia {direccion}: "
            f"{letra1}→{resultado1}, {letra2}→{resultado2}."
        )

    return (
        f"{letra1} y {letra2} forman un rectángulo (fila y columna "
        "distintas). Cada letra se reemplaza por la que está en su misma "
        f"fila, en la columna de la otra letra: {letra1}→{resultado1}, "
        f"{letra2}→{resultado2}."
    )


def generar_pasos(mensaje: str, clave: str, operacion: str) -> list:
    """Genera la secuencia de pasos educativos para visualizar Playfair.

    ``operacion`` debe ser ``OPERACION_CIFRAR`` o ``OPERACION_DESCIFRAR``.
    Cada paso es un diccionario con un campo ``"tipo"`` (``"matriz"``,
    ``"preparacion"`` o ``"digrafo"``) y los datos necesarios para que
    la interfaz lo dibuje: posiciones en la matriz, regla aplicada,
    explicación textual y resultado acumulado. No cifra ni descifra
    nada que ``cifrar``/``descifrar`` no calculen ya; solo expone el
    proceso intermedio para la demostración paso a paso.
    """
    if operacion not in (OPERACION_CIFRAR, OPERACION_DESCIFRAR):
        raise ValueError("La operación debe ser 'cifrar' o 'descifrar'.")

    clave_normalizada = normalizar_clave(clave)
    matriz = construir_matriz(clave)
    mensaje_normalizado = normalizar_mensaje(mensaje)

    pasos = [
        {
            "tipo": "matriz",
            "titulo": "Construcción de la matriz 5x5",
            "matriz": matriz,
            "clave_normalizada": clave_normalizada,
            "letras_clave": set(clave_normalizada),
            "explicacion": (
                f"Se toman las letras únicas de la clave «{clave_normalizada}» "
                "(sin repetir y con J fundida en I) y se colocan primero, "
                "fila por fila, de izquierda a derecha. Luego se completan "
                "las celdas restantes con el resto del alfabeto (sin la J) "
                "en orden alfabético."
            ),
        }
    ]

    if operacion == OPERACION_CIFRAR:
        digrafos = preparar_digrafos(mensaje_normalizado)
        hubo_relleno = len("".join(digrafos)) != len(mensaje_normalizado)
    else:
        if len(mensaje_normalizado) % 2 != 0:
            raise ValueError(
                "Un mensaje cifrado con Playfair debe tener una cantidad "
                "par de letras."
            )
        digrafos = [
            mensaje_normalizado[indice : indice + 2]
            for indice in range(0, len(mensaje_normalizado), 2)
        ]
        hubo_relleno = False

    explicacion_preparacion = (
        f"El mensaje «{mensaje}» se normaliza a «{mensaje_normalizado}» "
        "(solo letras, en mayúsculas, con J fundida en I) y se separa en "
        f"pares de letras (dígrafos): {' '.join(digrafos)}."
    )
    if hubo_relleno:
        explicacion_preparacion += (
            " Se insertó una letra de relleno (X, o Q cuando la repetida "
            "ya era X) porque el mensaje tenía letras iguales consecutivas "
            "o una cantidad impar de letras."
        )

    pasos.append(
        {
            "tipo": "preparacion",
            "titulo": "Preparación del mensaje en dígrafos",
            "mensaje_original": mensaje,
            "mensaje_normalizado": mensaje_normalizado,
            "digrafos": digrafos,
            "explicacion": explicacion_preparacion,
        }
    )

    resultado_acumulado = ""
    for indice, digrafo in enumerate(digrafos, start=1):
        analisis = _resolver_digrafo(matriz, digrafo, operacion)
        resultado_acumulado += analisis["resultado"]

        pasos.append(
            {
                "tipo": "digrafo",
                "titulo": f"Dígrafo {indice} de {len(digrafos)}: {digrafo}",
                "digrafo_entrada": digrafo,
                "digrafo_resultado": analisis["resultado"],
                "posiciones_entrada": analisis["posiciones_entrada"],
                "posiciones_resultado": analisis["posiciones_resultado"],
                "regla": analisis["regla"],
                "nombre_regla": NOMBRES_REGLA[analisis["regla"]],
                "explicacion": _explicar_regla(digrafo, analisis, operacion),
                "resultado_acumulado": resultado_acumulado,
            }
        )

    return pasos
