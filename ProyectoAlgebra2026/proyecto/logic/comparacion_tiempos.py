import time

from logic.gauss import (
    crear_matriz_aumentada,
    eliminacion_gaussiana,
    sustitucion_hacia_atras
)
from logic.gauss_seidel import gauss_seidel
from logic.validaciones import validar_forma


class ComparacionTiempos:

    def comparar_metodos(
        self, A, b, x0=None,
        tolerancia=0.000001,
        max_iteraciones=1000,
        repeticiones=1
    ):
        n = len(A)

        # Validar las dimensiones del sistema.
        if n < 2 or len(b) != n:
            raise ValueError("Las dimensiones no son correctas.")

        tabla = []

        for i in range(n):
            tabla.append(list(A[i]) + [b[i]])

        correcto, mensaje = validar_forma(tabla, n)

        if not correcto:
            raise ValueError(mensaje)

        # Validar los parámetros.
        if tolerancia <= 0 or max_iteraciones <= 0 or repeticiones <= 0:
            raise ValueError("Los parámetros deben ser positivos.")

        # Utilizar ceros como aproximación inicial.
        if x0 is None:
            x0 = [0] * n

        if len(x0) != n:
            raise ValueError("El vector inicial tiene dimensiones incorrectas.")

        # Comprobar si la matriz es diagonalmente dominante.
        dominante = True

        for i in range(n):
            suma = 0

            for j in range(n):
                if i != j:
                    suma += abs(A[i][j])

            if abs(A[i][i]) < suma:
                dominante = False

        # Preparar la matriz aumentada.
        matriz = crear_matriz_aumentada(A, b)

        # Comprobar que el sistema tenga solución única.
        resultado, pasos, matrices, pivotes = eliminacion_gaussiana(matriz)

        if len(pivotes) != n:
            raise ValueError("El sistema debe tener solución única para comparar los métodos.")

        # Medir el tiempo de eliminación gaussiana.
        tiempos_gauss = []

        for _ in range(repeticiones):
            matriz = crear_matriz_aumentada(A, b)

            inicio = time.perf_counter()

            resultado, pasos, matrices, pivotes = eliminacion_gaussiana(matriz)
            solucion_gauss = sustitucion_hacia_atras(resultado)

            fin = time.perf_counter()

            tiempos_gauss.append(fin - inicio)

        # Medir el tiempo de Gauss-Seidel.
        tiempos_seidel = []

        for _ in range(repeticiones):
            inicio = time.perf_counter()

            resultado_seidel = gauss_seidel(
                A, b, x0, tolerancia, max_iteraciones
            )

            fin = time.perf_counter()

            tiempos_seidel.append(fin - inicio)

        # Calcular los tiempos promedio.
        promedio_gauss = sum(tiempos_gauss) / repeticiones
        promedio_seidel = sum(tiempos_seidel) / repeticiones

        # Comparar las soluciones.
        diferencias = []

        for i in range(n):
            diferencia = abs(
                float(solucion_gauss[i]) -
                resultado_seidel["solucion"][i]
            )

            diferencias.append(diferencia)

        # Determinar cuál método fue más rápido.
        if promedio_gauss < promedio_seidel:
            metodo = "Eliminación gaussiana"
            factor = promedio_seidel / promedio_gauss

        elif promedio_seidel < promedio_gauss:
            metodo = "Gauss-Seidel"
            factor = promedio_gauss / promedio_seidel

        else:
            metodo = "Ambos métodos tardaron lo mismo"
            factor = 1

        # Devolver los resultados.
        return {
            "solucion_gauss": solucion_gauss,
            "solucion_seidel": resultado_seidel["solucion"],
            "diferencias": diferencias,
            "iteraciones": resultado_seidel["iteraciones"],
            "error": resultado_seidel["error"],
            "convergencia": resultado_seidel["convergencia"],
            "tiempo_gauss_total": sum(tiempos_gauss),
            "tiempo_gauss_promedio": promedio_gauss,
            "tiempo_seidel_total": sum(tiempos_seidel),
            "tiempo_seidel_promedio": promedio_seidel,
            "metodo_mas_rapido": metodo,
            "factor_rapidez": factor,
            "diagonalmente_dominante": dominante
        }
