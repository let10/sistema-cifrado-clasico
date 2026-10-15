"""Cifrado Cesar con procedimiento tecnico en tablas ASCII."""

from algoritmos.modelos import PasoProcedimiento

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _validar_clave(clave):
    if clave is None or str(clave).strip() == "":
        raise ValueError("La clave (desplazamiento) no puede estar vacia.")
    try:
        return int(str(clave).strip()) % 26
    except ValueError:
        raise ValueError("La clave debe ser un numero entero.")


def _desplazar(texto, desplazamiento):
    salida = []
    for c in texto:
        if c.isalpha() and c.isascii():
            base = ord('A') if c.isupper() else ord('a')
            salida.append(chr(base + (ord(c) - base + desplazamiento) % 26))
        else:
            salida.append(c)
    return "".join(salida)


def cifrar(mensaje, clave):
    return _desplazar(mensaje, _validar_clave(clave))


def descifrar(mensaje, clave):
    return _desplazar(mensaje, -_validar_clave(clave))


def generar_pasos(
    mensaje: str,
    clave: str,
    es_cifrado: bool,
) -> tuple[PasoProcedimiento, ...]:
    desplazamiento = _validar_clave(clave)
    if not es_cifrado:
        desplazamiento = -desplazamiento
    accion = "CIFRAR" if es_cifrado else "DESCIFRAR"
    salida = _desplazar(mensaje, desplazamiento)

    parametros = PasoProcedimiento(
        titulo="Datos de la operación",
        explicacion="El desplazamiento se reduce módulo 26. A cada letra se le suma para cifrar o se le resta para descifrar.",
        encabezados=("Dato", "Valor"),
        filas=(
            ("Operación", accion),
            ("Mensaje de entrada", mensaje),
            ("Clave ingresada", str(clave)),
            ("Desplazamiento efectivo", str(desplazamiento % 26)),
            ("Resultado", salida),
        ),
    )
    alfabeto = PasoProcedimiento(
        titulo="Correspondencia de alfabetos",
        explicacion="Cada letra del alfabeto de entrada se transforma en la letra situada el desplazamiento indicado.",
        encabezados=("Posición", "Entrada", "Posición salida", "Salida"),
        filas=tuple(
            (
                str(indice),
                ALFABETO[indice],
                str((indice + desplazamiento) % 26),
                ALFABETO[(indice + desplazamiento) % 26],
            )
            for indice in range(26)
        ),
    )

    filas_caracteres = []
    for indice, caracter in enumerate(mensaje, start=1):
        if caracter.isascii() and caracter.isalpha():
            posicion = ord(caracter.upper()) - ord("A")
            posicion_salida = (posicion + desplazamiento) % 26
            base = ord("A") if caracter.isupper() else ord("a")
            caracter_salida = chr(base + posicion_salida)
            operacion = (
                f"({posicion} {'+' if es_cifrado else '-'} "
                f"{abs(desplazamiento)}) mod 26 = {posicion_salida}"
            )
        else:
            posicion = "-"
            operacion = "Se conserva; no es letra A-Z"
            caracter_salida = caracter
        filas_caracteres.append(
            (str(indice), caracter,             str(posicion), operacion, caracter_salida)
        )

    transformacion = PasoProcedimiento(
        titulo="Transformación de cada carácter",
        explicacion="Los espacios, números, signos y caracteres fuera de A-Z se conservan sin aplicar desplazamiento.",
        encabezados=("#", "Entrada", "Posición", "Cálculo", "Salida"),
        filas=tuple(filas_caracteres),
    )
    return parametros, alfabeto, transformacion


def _tabla(encabezados, filas, anchos):
    def linea(i, m, d, r="-"):
        return i + m.join(r * (a + 2) for a in anchos) + d

    def fila(vals):
        celdas = [" " + str(v).ljust(a) + " " for v, a in zip(vals, anchos)]
        return "|" + "|".join(celdas) + "|"

    out = [linea("+", "+", "+"), fila(encabezados), linea("+", "+", "+", "=")]
    for f in filas:
        out.append(fila(f))
    out.append(linea("+", "+", "+"))
    return "\n".join(out)


def obtener_procedimiento(mensaje, clave, es_cifrado):
    desp = _validar_clave(clave)
    if not es_cifrado:
        desp = -desp

    alf_cifrado = "".join(ALFABETO[(i + desp) % 26] for i in range(26))
    lineas = []
    lineas.append("PROCEDIMIENTO - CIFRADO CESAR")
    lineas.append("=" * 60)
    lineas.append("")
    lineas.append("1. PARAMETROS DE ENTRADA")
    lineas.append("")
    lineas.append(_tabla(
        ["Parametro", "Valor"],
        [
            ["Accion", "CIFRAR" if es_cifrado else "DESCIFRAR"],
            ["Mensaje", mensaje],
            ["Clave (k)", str(clave)],
            ["Desplazamiento mod 26", str(desp % 26)],
        ],
        [24, 30],
    ))
    lineas.append("")
    lineas.append("2. ALFABETOS")
    lineas.append("")
    filas = [[str(i), ALFABETO[i], str((i + desp) % 26), alf_cifrado[i]]
             for i in range(26)]
    lineas.append(_tabla(["Pos", "Plano", "Pos+k", "Cifrado"], filas, [4, 6, 6, 8]))
    lineas.append("")
    lineas.append("3. SUSTITUCION LETRA POR LETRA")
    lineas.append("")
    filas = []
    for idx, c in enumerate(mensaje, 1):
        if c.isalpha() and c.isascii():
            mayus = c.upper()
            pos = ALFABETO.index(mayus)
            nueva_pos = (pos + desp) % 26
            nueva = alf_cifrado[pos]
            if c.islower():
                nueva = nueva.lower()
            op = "(%d + %d) mod 26 = %d" % (pos, desp, nueva_pos)
            filas.append([str(idx), c, str(pos), op, nueva])
        else:
            filas.append([str(idx), c, "-", "no aplica (no es letra)", c])
    lineas.append(_tabla(["#", "Entrada", "Pos", "Operacion", "Salida"],
                         filas, [3, 8, 4, 28, 7]))
    lineas.append("")
    lineas.append("4. RESULTADO FINAL")
    lineas.append("")
    resultado = _desplazar(mensaje, desp)
    lineas.append(_tabla(["Entrada", "Salida"], [[mensaje, resultado]], [30, 30]))
    return "\n".join(lineas)