
import random

from logic.comparacion_tiempos import ComparacionTiempos


class Experimento:

    def __init__(self, comparador=None):

        # Recibe el comparador para reutilizar sus métodos.
        self.comparador = (
            comparador if comparador is not None
            else ComparacionTiempos()
        )

    # Genera un sistema aleatorio diagonalmente dominante.
    def generar_sistema_aleatorio(self, n):

        if not isinstance(n, int) or n < 2:
            raise ValueError(
                "El tamaño debe ser un entero de al menos 2."
            )

        A = []

        # Construye una matriz diagonalmente dominante.
        for i in range(n):

            fila = []

            for j in range(n):

                if i == j:
                    fila.append(0)
                else:
                    fila.append(random.randint(-5, 5))

            # La diagonal será mayor que la suma de los demás elementos.
            suma = sum(abs(valor) for valor in fila)

            fila[i] = suma + random.randint(5, 10)

            A.append(fila)

        # Genera una solución real conocida.
        solucion_real = [
            random.randint(-5, 5)
            for _ in range(n)
        ]

        # Calcula b mediante la multiplicación A*x.
        b = []

        for i in range(n):

            valor = sum(
                A[i][j] * solucion_real[j]
                for j in range(n)
            )

            b.append(valor)

        return A, b

    # Ejecuta las comparaciones para diferentes tamaños de sistemas.
    def ejecutar_experimento(
        self,
        tamanos=None,
        tolerancia=0.000001,
        max_iteraciones=1000,
        repeticiones=3
    ):

        # Utiliza los tamaños establecidos en el proyecto.
        if tamanos is None:
            tamanos = [10, 20, 50, 100, 300, 500]

        if not tamanos:
            raise ValueError(
                "Debe proporcionar al menos un tamaño de sistema."
            )

        resultados = []

        # Ejecuta una prueba para cada tamaño.
        for n in tamanos:

            # Genera el sistema correspondiente.
            A, b = self.generar_sistema_aleatorio(n)

            # Utiliza el vector cero como aproximación inicial.
            x0 = [0] * n

            # Solicita la comparación a la clase especializada.
            resultado = self.comparador.comparar_metodos(
                A,
                b,
                x0,
                tolerancia,
                max_iteraciones,
                repeticiones
            )

            # Conserva los datos que necesita la tabla de la GUI.
            resultados.append({
                "n": n,
                "tiempo_gauss": resultado["tiempo_gauss_promedio"],
                "tiempo_seidel": resultado["tiempo_seidel_promedio"],
                "iteraciones_seidel": resultado["iteraciones"],
                "convergencia": resultado["convergencia"]
            })

        return resultados
