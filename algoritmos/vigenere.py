"""Cifrado Vigenere sobre el alfabeto A-Z."""

from algoritmos.modelos import PasoProcedimiento

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


def generar_pasos(
    mensaje: str,
    clave: str,
    es_cifrado: bool,
) -> tuple[PasoProcedimiento, ...]:
    clave_normalizada = _validar_clave(clave)
    resultado, transformaciones = _transformar(
        mensaje, clave_normalizada, es_cifrado
    )
    alineacion = []
    posicion_clave = 0
    for indice, entrada, letra_clave, _, salida in transformaciones:
        if letra_clave == "-":
            alineacion.append(
                (indice, entrada, "-", "Se conserva; no consume clave", salida)
            )
        else:
            posicion_clave += 1
            alineacion.append(
                (
                    indice,
                    entrada,
                    letra_clave,
                    f"Posición {posicion_clave}",
                    salida,
                )
            )

    datos = PasoProcedimiento(
        titulo="Datos de la operación",
        explicacion="Vigenère suma la posición de la letra de clave al cifrar y la resta al descifrar (A=0 ... Z=25).",
        encabezados=("Dato", "Valor"),
        filas=(
            ("Operación", "CIFRAR" if es_cifrado else "DESCIFRAR"),
            ("Mensaje de entrada", mensaje),
            ("Clave", clave_normalizada),
            ("Resultado", resultado),
        ),
    )
    tabla_clave = PasoProcedimiento(
        titulo="Alineación de la clave",
        explicacion="La clave se repite solo al encontrar letras A-Z. Los espacios, signos y números no consumen posiciones.",
        encabezados=("#", "Entrada", "Letra de clave", "Uso de la clave", "Salida"),
        filas=tuple(alineacion),
    )
    calculos = PasoProcedimiento(
        titulo="Cálculo carácter por carácter",
        explicacion="Para cada letra se calculan los índices A=0 ... Z=25 y se aplica la fórmula módulo 26.",
        encabezados=("#", "Entrada", "Letra de clave", "Cálculo", "Salida"),
        filas=tuple(
            (indice, entrada, letra_clave, operacion, salida)
            for indice, entrada, letra_clave, operacion, salida in transformaciones
        ),
    )
    return datos, tabla_clave, calculos


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
