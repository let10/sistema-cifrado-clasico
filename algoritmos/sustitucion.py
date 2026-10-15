"""Sustitucion Simple con procedimiento tecnico en tablas ASCII."""

from algoritmos.modelos import PasoProcedimiento

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _validar_clave(clave):
    if clave is None:
        raise ValueError("La clave no puede estar vacia.")
    clave = clave.strip().upper()
    if len(clave) != 26:
        raise ValueError("La clave debe tener exactamente 26 letras.")
    if not clave.isalpha() or not clave.isascii():
        raise ValueError("La clave solo puede contener letras A-Z.")
    if len(set(clave)) != 26:
        raise ValueError("La clave no puede tener letras repetidas.")
    return clave


def _sustituir(texto, mapa):
    out = []
    for c in texto:
        if c.isalpha() and c.isascii():
            nuevo = mapa[c.upper()]
            out.append(nuevo if c.isupper() else nuevo.lower())
        else:
            out.append(c)
    return "".join(out)


def cifrar(mensaje, clave):
    clave = _validar_clave(clave)
    mapa = {ALFABETO[i]: clave[i] for i in range(26)}
    return _sustituir(mensaje, mapa)


def descifrar(mensaje, clave):
    clave = _validar_clave(clave)
    mapa = {clave[i]: ALFABETO[i] for i in range(26)}
    return _sustituir(mensaje, mapa)


def generar_pasos(
    mensaje: str,
    clave: str,
    es_cifrado: bool,
) -> tuple[PasoProcedimiento, ...]:
    clave_validada = _validar_clave(clave)
    origen, destino = (
        (ALFABETO, clave_validada) if es_cifrado else (clave_validada, ALFABETO)
    )
    mapa = {origen[indice]: destino[indice] for indice in range(26)}
    salida = _sustituir(mensaje, mapa)
    equivalencias = PasoProcedimiento(
        titulo="Alfabeto de sustitución",
        explicacion=(
            "La clave es una permutación de A-Z. En descifrado se invierte "
            "la correspondencia entre ambos alfabetos."
        ),
        encabezados=("Posición", "Letra de entrada", "Letra de salida"),
        filas=tuple(
            (str(indice), origen[indice], destino[indice])
            for indice in range(26)
        ),
    )

    filas_caracteres = []
    for indice, caracter in enumerate(mensaje, start=1):
        if caracter.isascii() and caracter.isalpha():
            letra = caracter.upper()
            transformado = mapa[letra]
            caracter_salida = (
                transformado if caracter.isupper() else transformado.lower()
            )
            explicacion = "Sustitución directa"
        else:
            caracter_salida = caracter
            explicacion = "Se conserva; no es letra A-Z"
        filas_caracteres.append(
            (str(indice), caracter, explicacion, caracter_salida)
        )

    transformacion = PasoProcedimiento(
        titulo="Transformación de cada carácter",
        explicacion="Se sustituye cada letra usando la tabla; los demás caracteres se mantienen sin cambios.",
        encabezados=("#", "Entrada", "Regla aplicada", "Salida"),
        filas=tuple(filas_caracteres),
    )
    parametros = PasoProcedimiento(
        titulo="Datos de la operación",
        explicacion="El alfabeto de entrada se empareja posición por posición con la clave (o con A-Z al descifrar).",
        encabezados=("Dato", "Valor"),
        filas=(
            ("Operación", "CIFRAR" if es_cifrado else "DESCIFRAR"),
            ("Mensaje de entrada", mensaje),
            ("Clave validada", clave_validada),
            ("Resultado", salida),
        ),
    )
    return parametros, equivalencias, transformacion


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
    clave = _validar_clave(clave)
    origen, destino = (ALFABETO, clave) if es_cifrado else (clave, ALFABETO)
    mapa = {origen[i]: destino[i] for i in range(26)}

    lineas = []
    lineas.append("PROCEDIMIENTO - SUSTITUCION SIMPLE")
    lineas.append("=" * 60)
    lineas.append("")
    lineas.append("1. PARAMETROS DE ENTRADA")
    lineas.append("")
    lineas.append(_tabla(
        ["Parametro", "Valor"],
        [
            ["Accion", "CIFRAR" if es_cifrado else "DESCIFRAR"],
            ["Mensaje", mensaje],
            ["Alfabeto origen", origen],
            ["Alfabeto destino", destino],
        ],
        [20, 40],
    ))
    lineas.append("")
    lineas.append("2. TABLA DE EQUIVALENCIAS")
    lineas.append("")
    filas = []
    for i in range(13):
        j = i + 13
        filas.append([str(i), origen[i], destino[i],
                      str(j), origen[j], destino[j]])
    lineas.append(_tabla(["Pos", "Origen", "Destino", "Pos", "Origen", "Destino"],
                         filas, [4, 7, 8, 4, 7, 8]))
    lineas.append("")
    lineas.append("3. SUSTITUCION LETRA POR LETRA")
    lineas.append("")
    filas = []
    for idx, c in enumerate(mensaje, 1):
        if c.isalpha() and c.isascii():
            mayus = c.upper()
            nueva = mapa[mayus]
            if c.islower():
                nueva = nueva.lower()
            filas.append([str(idx), c, mayus, str(ALFABETO.index(mayus)), nueva])
        else:
            filas.append([str(idx), c, "-", "-", c])
    lineas.append(_tabla(["#", "Entrada", "Mayus", "Pos", "Salida"],
                         filas, [4, 8, 7, 5, 8]))
    lineas.append("")
    lineas.append("4. RESULTADO FINAL")
    lineas.append("")
    resultado = _sustituir(mensaje, mapa)
    lineas.append(_tabla(["Entrada", "Salida"], [[mensaje, resultado]], [30, 30]))
    return "\n".join(lineas)