
def clasificar(m, columnas_pivote):
    variables = len(m[0]) -1

    #revisamos si hay o no contradiccion
    for i in range(len(m)):
         todos_ceros = True

         for j in range (variables):
              if m[i][j] !=  0:
                   todos_ceros = False

         if todos_ceros and m[i][variables] != 0: 
                return "ninguna"

    #revisamos la cantidad de pivotes 
    if len(columnas_pivote) == variables:
         return "unica"

    else:
         return "infinitas"         


#Revisamos si hay contradiccion
def hay_contradiccion(m):
     for fila in m:
          todos_cero = True
          for i in range(len(fila)-1):
               if fila[i] != 0:
                    todos_cero = False
                    break
          if todos_cero and fila[-1] != 0:
               return True
     return False

#calculamos los rangos
def calcular_rangos(m, columnas_pivote):
     rango_a = len(columnas_pivote)
     if hay_contradiccion(m):
          rango_aumentada = rango_a +1
     else:
          rango_aumentada = rango_a

     return rango_a, rango_aumentada

#clsificaamos el sistema
def clasificar(m, columnas_pivote):
     variables = len(m[0])-1

     if hay_contradiccion(m):
          return "ninguna"

     if len(columnas_pivote) == variables:
          return "unica"

     return "infinitas"



#Este es código de prueba solamente, hecho por IA, luego se borra
#La union de esto con gauss es en dominio
from logic.gauss import crear_matriz_aumentada, eliminacion_gaussiana


if __name__ == "__main__":

    # Ejemplo 1: Solucion unica
     A1 = [
           [3, 2, 1],
           [1, 2, 1],
           [1, 1, 2]
       ]
   
     b1 = [48, 28, 31]
   
     m1 = crear_matriz_aumentada(A1, b1)
     resultado1, pasos1, matrices1, pivotes1 = eliminacion_gaussiana(m1)

     print("Ejemplo 1:", clasificar(resultado1, pivotes1))


    # Ejemplo 2: Infinitas soluciones
     A2 = [
           [1, 2, -1],
           [2, 4, -2],
           [1, 1, 1]
       ]
   
     b2 = [3, 6, 6]

     m2 = crear_matriz_aumentada(A2, b2)
     resultado2, pasos2, matrices2, pivotes2 = eliminacion_gaussiana(m2)

     print("Ejemplo 2:", clasificar(resultado2, pivotes2))


    # Ejemplo 3: Ninguna solucion
     A3 = [
            [1, 1, 1],
            [2, 2, 2],
            [1, -1, 0]
        ]
    
     b3 = [1, 3, 0]
    
     m3 = crear_matriz_aumentada(A3, b3)
     resultado3, pasos3, matrices3, pivotes3 = eliminacion_gaussiana(m3)

     print("Ejemplo 3:", clasificar(resultado3, pivotes3))


#aca probasmos lo de las contradciiones

     from logic.gauss import crear_matriz_aumentada, eliminacion_gaussiana

     # Ejemplo 1
     A = [
          [1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]
     ]
     b = [1, 2, 4]

     m = crear_matriz_aumentada(A, b)
     m, pasos, matrices, columnas_pivote = eliminacion_gaussiana(m)

     print("Ejemplo 1")
     print("¿Hay contradicción?", hay_contradiccion(m))
     print("Rangos:", calcular_rangos(m, columnas_pivote))
     print("Clasificación:", clasificar(m, columnas_pivote))