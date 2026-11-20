

from logic.gauss import (
    crear_matriz_aumentada,
    eliminacion_gaussiana,
    sustitucion_hacia_atras,
    comprobar_solucion
)
from logic.clasificacion import clasificar, calcular_rangos
from logic.solucion_general import solucion_general
from logic.gauss_seidel import gauss_seidel
from logic.validaciones import validar_n, validar_forma, validar_tabla
from logic.lectura import leer_csv
from logic.comparacion_tiempos import ComparacionTiempos
from logic.experimento import Experimento


class Dominio:

    # Constructor de la clase.
    def __init__(self):
        self.comparador = ComparacionTiempos()
        self.experimento = Experimento()

    # Validar la cantidad de incógnitas.
    def validar_n(self, texto, minimo=2, maximo=8):
        return validar_n(texto, minimo, maximo)

    # Validar la forma de una matriz.
    def validar_forma(self, filas, n):
        return validar_forma(filas, n)

    # Validar los datos de una tabla.
    def validar_tabla(self, tabla):
        return validar_tabla(tabla)

    # Leer un archivo CSV y preparar sus datos.
    def cargar_csv(self, ruta):
        correcto, filas = leer_csv(ruta)

        if not correcto:
            raise ValueError(filas)

        correcto, resultado = validar_tabla(filas)

        if not correcto:
            raise ValueError(resultado)

        return resultado

    # Resolver un sistema mediante eliminación gaussiana.
    def resolver_sistema(self, A, b):
        n = len(A)

        if n == 0 or len(b) != n:
            raise ValueError("Las dimensiones del sistema no son correctas.")

        # Comprobar que la matriz sea cuadrada.
        tabla = []

        for i in range(n):
            tabla.append(list(A[i]) + [b[i]])

        correcto, mensaje = validar_forma(tabla, n)

        if not correcto:
            raise ValueError(mensaje)

        # Construir la matriz aumentada.
        matriz = crear_matriz_aumentada(A, b)

        # Aplicar eliminación gaussiana.
        resultado, pasos, matrices, pivotes = eliminacion_gaussiana(matriz)

        # Clasificar el sistema y calcular sus rangos.
        tipo = clasificar(resultado, pivotes)
        rango_A, rango_aumentada = calcular_rangos(resultado, pivotes)

        # Inicializar los resultados.
        solucion = None
        verificacion = None
        Ax = None
        general = None
        libres = None

        # Si tiene solución única.
        if tipo == "unica":
            solucion = sustitucion_hacia_atras(resultado)
            verificacion, Ax = comprobar_solucion(A, b, solucion)

        # Si tiene infinitas soluciones.
        elif tipo == "infinitas":
            general, libres = solucion_general(resultado, pivotes)

        # Devolver los resultados.
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

    # Comprobar si la matriz es diagonalmente dominante.
    def validar_matriz_seidel(self, A):
        n = len(A)

        if n == 0:
            raise ValueError("La matriz está vacía.")

        for fila in A:
            if len(fila) != n:
                raise ValueError("La matriz debe ser cuadrada.")

        for i in range(n):
            if A[i][i] == 0:
                raise ValueError("La diagonal principal no puede tener ceros.")

        dominante = True

        for i in range(n):
            suma = 0

            for j in range(n):
                if i != j:
                    suma += abs(A[i][j])

            if abs(A[i][i]) < suma:
                dominante = False

        return dominante

    # Resolver un sistema mediante Gauss-Seidel.
    def resolver_seidel(self, A, b, x0=None, tolerancia=0.000001, max_iteraciones=1000):
        if x0 is None:
            x0 = [0] * len(A)

        return gauss_seidel(A, b, x0, tolerancia, max_iteraciones)

    # Comparar los tiempos de ambos métodos.
    def comparar_metodos(self, A, b, x0=None, tolerancia=0.000001, max_iteraciones=1000, repeticiones=1):
        return self.comparador.comparar_metodos(
            A, b, x0, tolerancia, max_iteraciones, repeticiones
        )

    # Ejecutar experimentos con diferentes tamaños de matrices.
    def ejecutar_experimento(self, tamanos=None, tolerancia=0.000001, max_iteraciones=1000, repeticiones=3):
        return self.experimento.ejecutar_experimento(
            tamanos, tolerancia, max_iteraciones, repeticiones
        )
