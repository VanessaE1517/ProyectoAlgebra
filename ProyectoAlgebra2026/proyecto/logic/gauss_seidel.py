
def gauss_seidel(A, b, x0, tolerancia, max_iteraciones=1000):

    # Cantidad de incógnitas.
    n = len(A)

    # Comprobar que las dimensiones sean correctas.
    if n == 0 or len(b) != n or len(x0) != n:
        raise ValueError("Las dimensiones no coinciden.")

    # Comprobar que la matriz sea cuadrada.
    for fila in A:
        if len(fila) != n:
            raise ValueError("La matriz debe ser cuadrada.")

    # Trabajar con números decimales.
    A = [[float(valor) for valor in fila] for fila in A]
    b = [float(valor) for valor in b]
    x = [float(valor) for valor in x0]

    # Comprobar los parámetros.
    if tolerancia <= 0 or max_iteraciones <= 0:
        raise ValueError("Los parámetros deben ser positivos.")

    # Comprobar que no haya ceros en la diagonal.
    for i in range(n):
        if A[i][i] == 0:
            raise ValueError("La diagonal principal no puede tener ceros.")

    error = float("inf")

    # Repetir el método hasta alcanzar la tolerancia.
    for iteracion in range(1, max_iteraciones + 1):

        # Guardar los valores anteriores.
        anterior = x.copy()

        # Calcular los nuevos valores de las incógnitas.
        for i in range(n):

            suma = 0

            for j in range(n):
                if i != j:
                    suma += A[i][j] * x[j]

            x[i] = (b[i] - suma) / A[i][i]

        # Calcular el error.
        error = 0

        for i in range(n):
            diferencia = abs(x[i] - anterior[i])

            if diferencia > error:
                error = diferencia

        # Comprobar si se alcanzó la tolerancia.
        if error <= tolerancia:
            return {
                "solucion": x,
                "iteraciones": iteracion,
                "error": error,
                "convergencia": True
            }

    # Si se alcanza el máximo de iteraciones.
    return {
        "solucion": x,
        "iteraciones": max_iteraciones,
        "error": error,
        "convergencia": False
    }
