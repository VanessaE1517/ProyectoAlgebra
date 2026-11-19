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




if __name__ == "__main__":
#prueba de la validacion
    pruebas = ["5", "", "abc", "3.5", "1", "9", " 4 "]

    print("Pruebas con mínimo 2 y máximo 8:")

    for texto in pruebas:
        resultado = validar_n(texto, 2, 8)
        print(texto, "->", resultado)

    print("\nPrueba sin máximo:")

    print("9 ->", validar_n("9", 2))

    #validacion de la forma
    print("\nPruebas de validar_forma:")

    filas = [
        ["1", "2", "3"],
        ["4", "5", "6"]
    ]

    print("Matriz correcta:", validar_forma(filas, 2))

    filas = [
        ["1", "2", "3"]
    ]

    print("Cantidad incorrecta de filas:", validar_forma(filas, 2))

    filas = [
        ["1", "2", "3"],
        ["4", "5"]
    ]

    print("Cantidad incorrecta de columnas:", validar_forma(filas, 2))
    
#validar tabla
    print("\nPruebas de validar_tabla:")

    tabla = [
        ["1", "2", "5"],
        ["3", "4", "7"]
    ]

    print("Tabla correcta:", validar_tabla(tabla))

    tabla = [
        ["1", "abc", "5"],
        ["3", "4", "7"]
    ]

    print("Tabla con error:", validar_tabla(tabla))


    # Error en la ultima columna
print("\nPrueba con error en la ultima columna:")

tabla = [
    ["1", "2", "x"],
    ["3", "4", "7"]
]

print(validar_tabla(tabla))


# Comprobar que se separen correctamente A y b
print("\nPrueba de separacion de A y b:")

tabla = [
    ["1", "2", "5"],
    ["3", "4", "7"]
]

print(validar_tabla(tabla))