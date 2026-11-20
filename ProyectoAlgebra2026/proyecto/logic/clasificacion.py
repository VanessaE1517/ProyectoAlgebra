
#validamos si hay contradiccion
def hay_contradiccion(m):

    for fila in m:
        todos_cero = True  # supongo que la parte de A de esta fila es toda ceros

        # recorro solo las columnas de A (todas menos la última, que es b)
        for i in range(len(fila) - 1):
            if fila[i] != 0:
                todos_cero = False
                break  # ya hay un número distinto de cero, no sigo con esta fila

        # la parte de A es toda ceros pero b no es cero -> 0 = c
        if todos_cero and fila[-1] != 0:
            return True

    return False

#calculamos el rango que tiene
def calcular_rangos(m, columnas_pivote):
    rango_a = len(columnas_pivote)

    if hay_contradiccion(m):
        rango_aumentada = rango_a + 1
    else:
        rango_aumentada = rango_a

    return rango_a, rango_aumentada

#clasificamos la solucion

def clasificar(m, columnas_pivote):

    variables = len(m[0]) - 1  # n = cantidad de columnas de A (sin contar b)

    if hay_contradiccion(m):
        return "ninguna"

    if len(columnas_pivote) == variables:
        return "unica"

    return "infinitas"