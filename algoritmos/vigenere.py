"""Cifrado Vigenere sobre el alfabeto A-Z."""

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _validar_clave(clave: str) -> str:
    if not isinstance(clave, str) or not clave.strip():
        raise ValueError("La clave no puede estar vacia.")

    clave_normalizada = clave.strip()
    if not clave_normalizada.isascii() or not clave_normalizada.isalpha():
        raise ValueError("La clave solo puede contener letras A-Z.")

    return clave_normalizada.upper()


def _transformar(
    mensaje: str,
    clave: str,
    es_cifrado: bool,
) -> tuple[str, list[tuple[str, str, str, str, str]]]:
    clave_normalizada = _validar_clave(clave)
    resultado = []
    pasos = []
    posicion_clave = 0

    for indice, caracter in enumerate(mensaje, start=1):
        if caracter.isascii() and caracter.isalpha():
            letra_clave = clave_normalizada[posicion_clave % len(clave_normalizada)]
            base = ord("A") if caracter.isupper() else ord("a")
            posicion_mensaje = ord(caracter.upper()) - ord("A")
            desplazamiento = ord(letra_clave) - ord("A")
            if not es_cifrado:
                desplazamiento = -desplazamiento

            posicion_salida = (posicion_mensaje + desplazamiento) % 26
            transformado = chr(base + posicion_salida)
            operacion = (
                f"({posicion_mensaje} {'+' if es_cifrado else '-'} "
                f"{abs(desplazamiento)}) mod 26 = {posicion_salida}"
            )
            pasos.append(
                (
                    str(indice),
                    caracter,
                    letra_clave,
                    operacion,
                    transformado,
                )
            )
            posicion_clave += 1
        else:
            transformado = caracter
            pasos.append((str(indice), caracter, "-", "no aplica", caracter))
        resultado.append(transformado)

    return "".join(resultado), pasos


def cifrar(mensaje: str, clave: str) -> str:
    """Cifra letras A-Z y conserva intactos los demas caracteres."""
    return _transformar(mensaje, clave, True)[0]


def descifrar(mensaje: str, clave: str) -> str:
    """Descifra letras A-Z y conserva intactos los demas caracteres."""
    return _transformar(mensaje, clave, False)[0]


def _tabla(encabezados: list[str], filas: list[tuple[str, ...]]) -> str:
    anchos = [
        max(len(encabezado), *(len(fila[indice]) for fila in filas))
        for indice, encabezado in enumerate(encabezados)
    ]

    def linea(separador: str) -> str:
        return (
            "+"
            + "+".join(separador * (ancho + 2) for ancho in anchos)
            + "+"
        )

    def fila(valores: tuple[str, ...] | list[str]) -> str:
        celdas = [
            " " + valor.ljust(ancho) + " "
            for valor, ancho in zip(valores, anchos)
        ]
        return "|" + "|".join(celdas) + "|"

    return "\n".join(
        [
            linea("-"),
            fila(encabezados),
            linea("="),
            *(fila(fila_actual) for fila_actual in filas),
            linea("-"),
        ]
    )


def obtener_procedimiento(mensaje: str, clave: str, es_cifrado: bool) -> str:
    """Devuelve el detalle didactico de la transformacion aplicada."""
    clave_normalizada = _validar_clave(clave)
    resultado, pasos = _transformar(mensaje, clave_normalizada, es_cifrado)
    accion = "CIFRAR" if es_cifrado else "DESCIFRAR"

    return "\n".join(
        [
            "PROCEDIMIENTO - CIFRADO VIGENERE",
            "=" * 60,
            "",
            "1. PARAMETROS DE ENTRADA",
            _tabla(
                ["Parametro", "Valor"],
                [
                    ("Accion", accion),
                    ("Mensaje", mensaje),
                    ("Clave normalizada", clave_normalizada),
                    ("Regla", "A=0 ... Z=25; no letras no avanzan la clave"),
                ],
            ),
            "",
            "2. TRANSFORMACION CARACTER POR CARACTER",
            _tabla(["#", "Entrada", "Clave", "Operacion", "Salida"], pasos),
            "",
            "3. RESULTADO FINAL",
            _tabla(["Entrada", "Salida"], [(mensaje, resultado)]),
        ]
    )
