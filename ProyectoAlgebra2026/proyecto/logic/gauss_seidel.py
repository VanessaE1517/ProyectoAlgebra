
def gauss_seidel(A, b, x0, tolerancia, max_iteraciones=1000):
    n = len(A)

    if n == 0 or len(b) != n or len(x0) != n:
        raise ValueError("Las dimensiones de A, b y x0 no coinciden.")

    for fila in A:
        if len(fila) != n:
            raise ValueError("La matriz debe ser cuadrada.")

    A = [[float(valor) for valor in fila] for fila in A]
    b = [float(valor) for valor in b]
    x = [float(valor) for valor in x0]

    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    if max_iteraciones <= 0:
        raise ValueError("El máximo de iteraciones debe ser positivo.")

    for i in range(n):
        if A[i][i] == 0:
            raise ValueError(
                "Hay un cero en la diagonal principal. "
                "No se puede aplicar Gauss-Seidel directamente."
            )

    error = float("inf")

    for iteracion in range(1, max_iteraciones + 1):
        x_anterior = x.copy()

        for i in range(n):
            suma = 0
            for j in range(n):
                if j != i:
                    suma += A[i][j] * x[j]
            x[i] = (b[i] - suma) / A[i][i]

        error = max(abs(x[i] - x_anterior[i]) for i in range(n))

        if error <= tolerancia:
            return {
                "solucion": x,
                "iteraciones": iteracion,
                "error": error,
                "convergencia": True
            }

    return {
        "solucion": x,
        "iteraciones": max_iteraciones,
        "error": error,
        "convergencia": False
    }