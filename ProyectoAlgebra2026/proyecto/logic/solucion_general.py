#Estos import se borran luego. solo es para prueba
from fractions import Fraction
from logic.gauss import crear_matriz_aumentada, eliminacion_gaussiana


#Lo que hace es recibir las columnas pivote y las cant de incógnitas 
def variables_libres(columnas_pivote, incognitas):
     libres =[]
     for i in range(incognitas):
           if i not in columnas_pivote:
                 libres.append(i)  

     return libres

#esta evalua la solucion general y los valor que queremos asignar
def evaluar_solucion_general(general, valores):
     resultado = []
     for variable in general: 
          suma = variable[0]
          for i in range(len(valores)):
               suma += variable[i+1] * valores[i]
          resultado.append(suma)
     return resultado


#Acá multiplicamos cada elemento de la lista por un n y devuelve una lista nueva
def escalar_lista(lista, k):
     resultado = []
     for x in lista: 
          resultado.append(x * k)

     return resultado


#acá sumamos ambas listas en la misma posicion
def sumar_listas(a,b):
     resultado = []
     for x, y in zip(a,b): #el zip es una funcion que hace que recorra amabs listas al mismo tiempo
            resultado.append(x+y)

     return resultado 


def solucion_general(m, columnas_pivote):
     n = len(m[0])-1
     libres = variables_libres(columnas_pivote, n)
     p = len(libres)
     general = []

     #creamos una lista para cada variable
     for i in range(n):
          general.append([0]*(p+1)) #la primera posicion es el valor de la variable, luego los valores de las variables libres

     #asignamos los parametros a las variables libres
     for i in range(p):
          general[libres[i]][i+1] = Fraction(1)

    #recorremos las filas de abajo hacia arriba
     for r in range(len(columnas_pivote)-1,-1,-1):
        col = columnas_pivote[r]
        expresion =[Fraction(0)] * (p+1)
        expresion[0] = m[r][-1] 

        #restar las variables de la derecha
        for j in range(col+1, n):
            coeficiente = m[r][j]
            multiplicacion = escalar_lista(general[j], -coeficiente)

            expresion = sumar_listas(expresion, multiplicacion)
            
        #dividimos entre el pivote
        pivote = m[r][col]
        expresion = escalar_lista(expresion, Fraction(1)/pivote)
        general[col] = expresion

     return general, libres




   #Test para ver si las varibles libres y solucion general funciona
    #Esto se borra luego
if __name__ == "__main__":
        columnas_pivote = [0, 1]
        n = 3

        libres = variables_libres(columnas_pivote, n)

        print("Variables libres:", libres)

        general = [
            [9, -3],
            [-3, 2],
            [0, 1]
        ]

        valores = [2]

        resultado = evaluar_solucion_general(general, valores)

        print("Solucion evaluada:", resultado)


    #estos print son para probar las funciones de escalar y sumar listas
        print(escalar_lista([9, -3], 2))
        print(sumar_listas([1, 2], [3, 4]))


            #acá estos probando ya la solucion general

        A = [
            [1, 1, 1, 1],
            [0, 1, 1, 0]
        ]

        b = [4, 1]

        m = crear_matriz_aumentada(A, b)

        m, pasos, matrices, columnas_pivote = eliminacion_gaussiana(m)

        print("Matriz después de Gauss:")
        print(m)

        print("Columnas pivote:")
        print(columnas_pivote)

        general, libres = solucion_general(m, columnas_pivote)

        print("Solución general:")
        print(general)

        print("Variables libres:")
        print(libres)