"""Cifrado Cesar con procedimiento tecnico en tablas ASCII."""

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