
def gauss_seidel(A, b, x0, tolerancia, max_iteraciones=1000):
    # Obtiene la cantidad de filas de la matriz A.
    n = len(A)

    # Verifica que la matriz no esté vacía y que los vectores b y x0
    # tengan la misma cantidad de elementos que la matriz.
    if n == 0 or len(b) != n or len(x0) != n:
        raise ValueError("Las dimensiones de A, b y x0 no coinciden.")

    # Comprueba que la matriz sea cuadrada.
    for fila in A:
        if len(fila) != n:
            raise ValueError("La matriz debe ser cuadrada.")

    # Convierte todos los elementos de la matriz y los vectores a números decimales.
    A = [[float(valor) for valor in fila] for fila in A]
    b = [float(valor) for valor in b]
    x = [float(valor) for valor in x0]

    # Verifica que la tolerancia sea un número positivo.
    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    # Verifica que el máximo de iteraciones sea positivo.
    if max_iteraciones <= 0:
        raise ValueError("El máximo de iteraciones debe ser positivo.")

    # Comprueba que ningún elemento de la diagonal principal sea cero,
    # ya que se necesita dividir entre esos valores.
    for i in range(n):
        if A[i][i] == 0:
            raise ValueError(
                "Hay un cero en la diagonal principal. "
                "No se puede aplicar Gauss-Seidel directamente."
            )

    # Inicializa el error con infinito para comenzar las iteraciones.
    error = float("inf")

    # Repite el proceso hasta alcanzar la tolerancia o el máximo de iteraciones.
    for iteracion in range(1, max_iteraciones + 1):

        # Guarda una copia de los valores anteriores de las incógnitas.
        x_anterior = x.copy()

        # Recorre cada ecuación del sistema para actualizar las incógnitas.
        for i in range(n):
            suma = 0

            # Calcula la suma de los demás términos de la ecuación,
            # utilizando los valores más recientes disponibles de x.
            for j in range(n):
                if j != i:
                    suma += A[i][j] * x[j]

            # Calcula el nuevo valor de la incógnita correspondiente.
            x[i] = (b[i] - suma) / A[i][i]

        # Calcula el error máximo entre los valores nuevos y los anteriores.
        error = max(abs(x[i] - x_anterior[i]) for i in range(n))

        # Comprueba si el error es menor o igual que la tolerancia establecida.
        if error <= tolerancia:

            # Devuelve los resultados si el método logró converger.
            return {
                "solucion": x,
                "iteraciones": iteracion,
                "error": error,
                "convergencia": True
            }

    # Si se alcanza el máximo de iteraciones sin cumplir la tolerancia,
    # devuelve los resultados indicando que no hubo convergencia.
    return {
        "solucion": x,
        "iteraciones": max_iteraciones,
        "error": error,
        "convergencia": False
    }
