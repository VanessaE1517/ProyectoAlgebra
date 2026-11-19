import time
import copy
import random

from logic.solucion_general import solucion_general
from logic.gauss_seidel import gauss_seidel
from logic.gauss import (
    crear_matriz_aumentada,
    eliminacion_gaussiana,
    sustitucion_hacia_atras,
    comprobar_solucion
)
from logic.clasificacion import clasificar


class Dominio:

    def __init__(self):
        pass

    def resolver_sistema(self, A, b):
        matriz = crear_matriz_aumentada(A, b)
        resultado, pasos, matrices, pivotes = eliminacion_gaussiana(matriz)
        tipo = clasificar(resultado, pivotes)
        rango_A = len(pivotes)
        rango_aumentada = rango_A + 1 if tipo == "ninguna" else rango_A

        solucion = verificacion = Ax = general = libres = None

        if tipo == "unica":
            solucion = sustitucion_hacia_atras(resultado)
            verificacion, Ax = comprobar_solucion(A, b, solucion)
        elif tipo == "infinitas":
            general, libres = solucion_general(resultado, pivotes)

        return {
            "tipo": tipo,
            "matriz": resultado,
            "pasos": pasos,
            "matrices": matrices,
            "pivotes": pivotes,
            "rango_A": rango_A,
            "rango_aumentada": rango_aumentada,
            "solucion": solucion,
            "verificacion": verificacion,
            "Ax": Ax,
            "general": general,
            "libres": libres
        }

    def validar_matriz_seidel(self, A):
        n = len(A)

        if n < 2 or any(len(fila) != n for fila in A):
            raise ValueError("La matriz debe ser cuadrada y tener al menos 2 filas.")

        for i in range(n):
            if A[i][i] == 0:
                raise ValueError(f"El elemento A[{i+1},{i+1}] de la diagonal principal no puede ser cero.")

        dominante = True

        for i in range(n):
            suma = sum(abs(A[i][j]) for j in range(n) if j != i)
            if abs(A[i][i]) < suma:
                dominante = False
                break

        return dominante

    def resolver_seidel(self, A, b, x0=None, tolerancia=0.000001, max_iteraciones=1000):
        n = len(A)
        if x0 is None: x0 = [0] * n

        resultado = gauss_seidel(A, b, x0, tolerancia, max_iteraciones)
        return resultado

    def comparar_metodos(self, A, b, x0=None, tolerancia=0.000001, max_iteraciones=1000, repeticiones=1):
        n = len(A)

        if n < 2 or len(b) != n:
            raise ValueError("Las dimensiones de A y b no son correctas.")

        if tolerancia <= 0:
            raise ValueError("La tolerancia debe ser positiva.")

        if not isinstance(max_iteraciones, int) or max_iteraciones <= 0:
            raise ValueError("El máximo de iteraciones debe ser un entero positivo.")

        if not isinstance(repeticiones, int) or repeticiones <= 0:
            raise ValueError("Las repeticiones deben ser un entero positivo.")

        if x0 is None: x0 = [0] * n

        if len(x0) != n:
            raise ValueError("El vector inicial debe tener exactamente n valores.")

        dominante = self.validar_matriz_seidel(A)
        resultado_gauss = self.resolver_sistema(A, b)

        if resultado_gauss["tipo"] == "infinitas":
            raise ValueError("El sistema tiene infinitas soluciones. No se puede realizar la comparación.")

        if resultado_gauss["tipo"] == "ninguna":
            raise ValueError("El sistema no tiene solución. No se puede realizar la comparación.")

        tiempos_gauss = []
        solucion = None

        for _ in range(repeticiones):
            matriz = crear_matriz_aumentada(copy.deepcopy(A), copy.deepcopy(b))
            inicio = time.perf_counter()
            resultado, pasos, matrices, pivotes = eliminacion_gaussiana(matriz)
            solucion = sustitucion_hacia_atras(resultado)
            fin = time.perf_counter()
            tiempos_gauss.append(fin - inicio)

        tiempos_seidel = []
        resultado_seidel = None

        for _ in range(repeticiones):
            inicio = time.perf_counter()
            resultado_seidel = self.resolver_seidel(
                copy.deepcopy(A),
                copy.deepcopy(b),
                copy.deepcopy(x0),
                tolerancia,
                max_iteraciones
            )
            fin = time.perf_counter()
            tiempos_seidel.append(fin - inicio)

        diferencias = [
            abs(float(g) - float(s))
            for g, s in zip(solucion, resultado_seidel["solucion"])
        ]

        tiempo_gauss_total = sum(tiempos_gauss)
        tiempo_seidel_total = sum(tiempos_seidel)
        promedio_gauss = tiempo_gauss_total / repeticiones
        promedio_seidel = tiempo_seidel_total / repeticiones

        if promedio_gauss < promedio_seidel:
            metodo_mas_rapido = "Eliminación gaussiana"
            factor_rapidez = promedio_seidel / promedio_gauss if promedio_gauss > 0 else None
        elif promedio_seidel < promedio_gauss:
            metodo_mas_rapido = "Gauss-Seidel"
            factor_rapidez = promedio_gauss / promedio_seidel if promedio_seidel > 0 else None
        else:
            metodo_mas_rapido = "Ambos métodos tardaron lo mismo"
            factor_rapidez = 1

        return {
            "solucion_gauss": solucion,
            "solucion_seidel": resultado_seidel["solucion"],
            "diferencias": diferencias,
            "iteraciones": resultado_seidel["iteraciones"],
            "error": resultado_seidel["error"],
            "convergencia": resultado_seidel["convergencia"],
            "tiempo_gauss_total": tiempo_gauss_total,
            "tiempo_gauss_promedio": promedio_gauss,
            "tiempo_seidel_total": tiempo_seidel_total,
            "tiempo_seidel_promedio": promedio_seidel,
            "metodo_mas_rapido": metodo_mas_rapido,
            "factor_rapidez": factor_rapidez,
            "diagonalmente_dominante": dominante
        }

    def generar_sistema_aleatorio(self, n):
        if n < 2:
            raise ValueError("El tamaño debe ser al menos 2.")

        A = []

        for i in range(n):
            fila = []

            for j in range(n):
                if i == j:
                    fila.append(0)
                else:
                    fila.append(random.randint(-5, 5))

            suma = sum(abs(valor) for valor in fila)
            fila[i] = suma + random.randint(5, 10)
            A.append(fila)

        solucion_real = [random.randint(-5, 5) for _ in range(n)]
        b = []

        for i in range(n):
            valor = sum(A[i][j] * solucion_real[j] for j in range(n))
            b.append(valor)

        return A, b

    def ejecutar_experimento(self, tamanos=None, tolerancia=0.000001, max_iteraciones=1000, repeticiones=3):
        if tamanos is None: tamanos = [10, 20, 50, 100, 300, 500]

        resultados = []

        for n in tamanos:
            A, b = self.generar_sistema_aleatorio(n)
            x0 = [0] * n
            resultado = self.comparar_metodos(A, b, x0, tolerancia, max_iteraciones, repeticiones)

            resultados.append({
                "n": n,
                "tiempo_gauss": resultado["tiempo_gauss_promedio"],
                "tiempo_seidel": resultado["tiempo_seidel_promedio"],
                "iteraciones_seidel": resultado["iteraciones"],
                "convergencia": resultado["convergencia"]
            })

        return resultados


if __name__ == "__main__":
    dominio = Dominio()
    A = [[10, 1, 1], [1, 10, 1], [1, 1, 10]]
    b = [12, 12, 12]
    x0 = [0, 0, 0]

    resultado = dominio.comparar_metodos(
        A, b, x0,
        tolerancia=0.000001,
        max_iteraciones=1000,
        repeticiones=3
    )

    print("SOLUCIÓN GAUSSIANA:")
    print(resultado["solucion_gauss"])
    print("\nSOLUCIÓN GAUSS-SEIDEL:")
    print(resultado["solucion_seidel"])
    print("\nDIFERENCIAS:")
    print(resultado["diferencias"])
    print("\nITERACIONES:")
    print(resultado["iteraciones"])
    print("\n¿CONVERGIÓ?")
    print(resultado["convergencia"])
    print("\n¿ES DIAGONALMENTE DOMINANTE?")
    print(resultado["diagonalmente_dominante"])
    print("\nMÉTODO MÁS RÁPIDO:")
    print(resultado["metodo_mas_rapido"])
    print("\nFACTOR DE RAPIDEZ:")
    print(resultado["factor_rapidez"])
    print("\nTIEMPO GAUSSIANO PROMEDIO:")
    print(resultado["tiempo_gauss_promedio"])
    print("\nTIEMPO GAUSS-SEIDEL PROMEDIO:")
    print(resultado["tiempo_seidel_promedio"])