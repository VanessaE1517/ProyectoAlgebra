from logic.lectura import convertir_a_fraccion #Este import no se borra

#vamos a validar
def validar_n(texto, minimo, maximo =None):
    texto = texto.strip() #eliminamos los espacios al inicio y al final

    if texto == "":
        return False, "El campo está vacío"

    try:
        numero = int(texto) #convertimos el texto en un número entero
    
    except ValueError:
        return False, "El número debe ser entero"

    if numero < minimo:
        return False, "El número debe ser al menos 2"

    if maximo is not None and numero > maximo:
        return False, "El número debe ser máximo 8"

    return True, numero

#ahora vamos a validar la forma, que tenga justamente n filas y que tenga n+1 columnas
def validar_forma(filas, n):

    if len(filas) != n:
        return False, "La matriz debe tener exactamente "+str(n)+" filas"

    for i in range(len(filas)):
        if len(filas[i]) != n+1:
            return False, "La fila " +str(i+1)+" debe tener "+str(n+1)+" columnas"

    return True, "La matriz es válida"

#vamos a validar la tabla
def validar_tabla(tabla_de_textos):
    tabla=[]
    for i in range(len(tabla_de_textos)):
        fila =[]

        for j in range(len(tabla_de_textos[i])):
            ok, resultado = convertir_a_fraccion(tabla_de_textos[i][j])

            if not ok:
                return False, "Error en la fila "+str(i+1)+", columna "+str(j+1)+": "+ resultado

            fila.append(resultado)
        tabla.append(fila)

    A =[]
    b=[]

    for fila in tabla:
        A.append(fila[:-1])
        b.append(fila[-1])

    return True, (A,b) #devolvemos ambas matrices listas

