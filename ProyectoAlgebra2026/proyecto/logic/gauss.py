
from fractions import Fraction
import copy

# Creación de la matriz aumentada
# Une la matriz A con el vector b
def crear_matriz_aumentada(A, b):
    m = []

    for i in range(len(A)):
        fila = []

        for j in range(len(A[i])):
            fila.append(Fraction(str(A[i][j])))

        fila.append(Fraction(str(b[i])))
        m.append(fila)

    return m


# Imprimir la matriz
def imprimir_matriz(m):
    for fila in m:
        for x in fila:
            print(f"{str(x):>8} ", end=" ")
        print()


# Buscar el pivote
def buscar_pivote(m, col, fila_inicio):
    mejor = fila_inicio

    for i in range(fila_inicio, len(m)):
        if abs(m[i][col]) > abs(m[mejor][col]):
            mejor = i

    return mejor


# Intercambio de filas
def intercambiar_filas(m, i, j):
    m[i], m[j] = m[j], m[i]


# Para eliminar los elementos debajo del pivote
def eliminar_debajo_pivote(m, fila_pivote, col):
    pasos = []
    matrices = []

    for i in range(fila_pivote + 1, len(m)):

        if m[i][col] != 0:

            mult = m[i][col] / m[fila_pivote][col]

            for k in range(col, len(m[i])):
                m[i][k] -= mult * m[fila_pivote][k]

            pasos.append(
                f"F{i+1} - ({mult}) F{fila_pivote+1} -> F{i+1}"
            )

            matrices.append(copy.deepcopy(m))

    return pasos, matrices


# Eliminación gaussiana
def eliminacion_gaussiana(m):
    pasos = []
    matrices = []
    columnas_pivote = []

    m = copy.deepcopy(m)

    filas = len(m)
    columnas = len(m[0]) - 1
    fila_pivote = 0

    for col in range(columnas):

        if fila_pivote >= filas:
            break

        mejor = buscar_pivote(m, col, fila_pivote)

        if m[mejor][col] == 0:
            continue

        if mejor != fila_pivote:

            intercambiar_filas(m, fila_pivote, mejor)

            pasos.append(
                f"F{fila_pivote+1} <-> F{mejor+1}"
            )

            matrices.append(copy.deepcopy(m))

        columnas_pivote.append(col)

        nuevos_pasos, nuevas_matrices = eliminar_debajo_pivote(
            m, fila_pivote, col
        )

        for i in range(len(nuevos_pasos)):
            pasos.append(nuevos_pasos[i])
            matrices.append(nuevas_matrices[i])

        fila_pivote += 1

    return m, pasos, matrices, columnas_pivote

#sustitucion hacia atras
#la idea de esta es que reciba la matriz escalonada y devuelve el valor de los Xn

def sustitucion_hacia_atras(m):
    n = len(m[0])-1
    x = [0] * n

    for i in range(n-1,-1,-1):
        suma =0
        for j in range(i+1, n):
            suma += m[i][j] * x[j]
        x[i] = (m[i][n] - suma) / m[i][i]
    
    return x

#Comprobacion de Ax=b
def comprobar_solucion(A, b, x, tolerancia=0.000001):
    Ax =[]
    for i in range(len(A)):
        suma = 0

        for j in range(len(A[i])):
            suma += A[i][j] * x[j]

        Ax.append(suma)
    correcto = True


    for i in range(len(b)): #Esto es si viene en float
        if abs(Ax[i] - b[i]) > tolerancia:
            correcto = False

    return correcto, Ax

