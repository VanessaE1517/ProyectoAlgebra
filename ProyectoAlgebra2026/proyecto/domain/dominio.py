import time
import copy
import random

# Importa la función que obtiene la solución general de un sistema
# cuando este tiene infinitas soluciones.
from logic.solucion_general import solucion_general

# Importa el método iterativo de Gauss-Seidel.
from logic.gauss_seidel import gauss_seidel

# Importa las funciones necesarias para aplicar el método de eliminación gaussiana.
from logic.gauss import (
    crear_matriz_aumentada,  # Construye la matriz aumentada del sistema.
    eliminacion_gaussiana,   # Realiza la eliminación gaussiana.
    sustitucion_hacia_atras, # Obtiene la solución mediante sustitución hacia atrás.
    comprobar_solucion       # Comprueba si la solución satisface el sistema.
)

# Importa la función que clasifica el sistema según sus soluciones.
from logic.clasificacion import clasificar

# Importa la lectura y la validación de archivos CSV.
from logic.lectura import leer_csv
from logic.validaciones import validar_forma, validar_tabla


class Dominio:

    # Constructor de la clase Dominio.
    def __init__(self):
        pass

    # Resuelve un sistema de ecuaciones utilizando eliminación gaussiana.
    def resolver_sistema(self, A, b):

        # Construye la matriz aumentada a partir de la matriz A y el vector b.
        matriz = crear_matriz_aumentada(A, b)

        # Aplica eliminación gaussiana.
        # Retorna la matriz resultante, los pasos realizados,
        # las matrices de cada paso y las posiciones de los pivotes.
        resultado, pasos, matrices, pivotes = eliminacion_gaussiana(matriz)

        # Determina si el sistema tiene solución única, infinitas soluciones o ninguna.
        tipo = clasificar(resultado, pivotes)

        # Calcula el rango de la matriz de coeficientes.
        rango_A = len(pivotes)

        # Calcula el rango de la matriz aumentada.
        # Si el sistema no tiene solución, el rango aumentado es mayor.
        rango_aumentada = rango_A + 1 if tipo == "ninguna" else rango_A

        # Inicializa las variables que almacenarán los resultados.
        solucion = verificacion = Ax = general = libres = None

        # Si el sistema tiene solución única:
        if tipo == "unica":

            # Obtiene los valores de las incógnitas mediante sustitución hacia atrás.
            solucion = sustitucion_hacia_atras(resultado)

            # Comprueba la solución sustituyendo los valores en el sistema original.
            verificacion, Ax = comprobar_solucion(A, b, solucion)

        # Si el sistema tiene infinitas soluciones:
        elif tipo == "infinitas":

            # Obtiene la expresión general de las soluciones
            # y las variables libres del sistema.
            general, libres = solucion_general(resultado, pivotes)

        # Retorna toda la información obtenida al resolver el sistema.
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

    # Valida si una matriz cumple las condiciones necesarias
    # para aplicar Gauss-Seidel.
    def validar_matriz_seidel(self, A):

        # Obtiene la cantidad de filas de la matriz.
        n = len(A)

        # Comprueba que la matriz sea cuadrada y tenga al menos 2 filas.
        if n < 2 or any(len(fila) != n for fila in A):
            raise ValueError("La matriz debe ser cuadrada y tener al menos 2 filas.")

        # Comprueba que ningún elemento de la diagonal principal sea cero.
        for i in range(n):
            if A[i][i] == 0:
                raise ValueError(f"El elemento A[{i+1},{i+1}] de la diagonal principal no puede ser cero.")

        # Inicialmente se considera que la matriz es diagonalmente dominante.
        dominante = True

        # Recorre cada fila de la matriz.
        for i in range(n):

            # Suma los valores absolutos de los elementos que están
            # fuera de la diagonal principal en la fila actual.
            suma = sum(abs(A[i][j]) for j in range(n) if j != i)

            # Comprueba si el elemento diagonal es menor que esa suma.
            if abs(A[i][i]) < suma:

                # Si no cumple la condición, la matriz no es diagonalmente dominante.
                dominante = False
                break

        # Retorna True si es diagonalmente dominante o False en caso contrario.
        return dominante

    # Comprueba si la matriz es estrictamente diagonalmente dominante:
    # en cada fila, |a_ii| es mayor que la suma de los demás |a_ij|.
    # Una matriz así siempre tiene solución única.
    def es_estrictamente_dominante(self, A):
        n = len(A)

        for i in range(n):
            suma = sum(abs(A[i][j]) for j in range(n) if j != i)

            if abs(A[i][i]) <= suma:
                return False

        return True

    # Resuelve un sistema utilizando el método iterativo de Gauss-Seidel.
    def resolver_seidel(self, A, b, x0=None, tolerancia=0.000001, max_iteraciones=1000):

        # Obtiene el número de incógnitas del sistema.
        n = len(A)

        # Si no se proporciona una aproximación inicial,
        # se utiliza un vector de ceros.
        if x0 is None: x0 = [0] * n

        # Ejecuta el método de Gauss-Seidel con los parámetros recibidos.
        resultado = gauss_seidel(A, b, x0, tolerancia, max_iteraciones)

        # Retorna los resultados obtenidos por el método.
        return resultado

    # Compara el rendimiento de la eliminación gaussiana y Gauss-Seidel.
    def comparar_metodos(self, A, b, x0=None, tolerancia=0.000001, max_iteraciones=1000, repeticiones=1):

        # Obtiene el número de incógnitas del sistema.
        n = len(A)

        # Comprueba que las dimensiones de A y b sean compatibles.
        if n < 2 or len(b) != n:
            raise ValueError("Las dimensiones de A y b no son correctas.")

        # Comprueba que la tolerancia sea un número positivo.
        if tolerancia <= 0:
            raise ValueError("La tolerancia debe ser positiva.")

        # Comprueba que el máximo de iteraciones sea un entero positivo.
        if not isinstance(max_iteraciones, int) or max_iteraciones <= 0:
            raise ValueError("El máximo de iteraciones debe ser un entero positivo.")

        # Comprueba que la cantidad de repeticiones sea un entero positivo.
        if not isinstance(repeticiones, int) or repeticiones <= 0:
            raise ValueError("Las repeticiones deben ser un entero positivo.")

        # Si no se proporciona un vector inicial, utiliza un vector de ceros.
        if x0 is None: x0 = [0] * n

        # Comprueba que el vector inicial tenga la misma dimensión que el sistema.
        if len(x0) != n:
            raise ValueError("El vector inicial debe tener exactamente n valores.")

        # Comprueba que el sistema tenga solución única (esto no cuenta en el tiempo medido).
        if n <= 20:

            # Sistema pequeño: se clasifica con fracciones, el resultado es exacto.
            resultado_gauss = self.resolver_sistema(A, b)

            # No permite comparar los métodos si el sistema tiene infinitas soluciones.
            if resultado_gauss["tipo"] == "infinitas":
                raise ValueError("El sistema tiene infinitas soluciones. No se puede realizar la comparación.")

            # No permite comparar los métodos si el sistema no tiene solución.
            if resultado_gauss["tipo"] == "ninguna":
                raise ValueError("El sistema no tiene solución. No se puede realizar la comparación.")

        # Sistema grande: si es estrictamente diagonalmente dominante ya se sabe
        # que tiene solución única. Si no lo es, se hace una eliminación rápida
        # (sin guardar pasos) y se revisa que haya un pivote en cada columna.
        elif not self.es_estrictamente_dominante(A):
            matriz = crear_matriz_aumentada(A, b, False)
            resultado, pasos, matrices, pivotes = eliminacion_gaussiana(matriz, False)

            if len(pivotes) != n:
                raise ValueError("El sistema no tiene solución única. No se puede realizar la comparación.")

        # Comprueba que no haya ceros en la diagonal y si la matriz es diagonalmente dominante.
        dominante = self.validar_matriz_seidel(A)

        # Lista donde se almacenarán los tiempos de cada ejecución de Gauss.
        tiempos_gauss = []
        solucion = None

        # Ejecuta la eliminación gaussiana la cantidad de veces indicada.
        for _ in range(repeticiones):

            # Registra el tiempo inicial.
            inicio = time.perf_counter()

            # Crea la matriz aumentada con float (es una copia, no modifica A ni b).
            matriz = crear_matriz_aumentada(A, b, False)

            # Ejecuta la eliminación gaussiana sin guardar los pasos.
            resultado, pasos, matrices, pivotes = eliminacion_gaussiana(matriz, False)

            # Obtiene la solución mediante sustitución hacia atrás.
            solucion = sustitucion_hacia_atras(resultado)

            # Registra el tiempo final.
            fin = time.perf_counter()

            # Guarda el tiempo que tardó esta ejecución.
            tiempos_gauss.append(fin - inicio)

        # Lista donde se almacenarán los tiempos de Gauss-Seidel.
        tiempos_seidel = []
        resultado_seidel = None

        # Ejecuta Gauss-Seidel la cantidad de veces indicada.
        for _ in range(repeticiones):

            # Crea copias para conservar los datos originales.
            # Se hacen antes de medir, para que no cuenten en el tiempo.
            A_copia = copy.deepcopy(A)
            b_copia = copy.deepcopy(b)
            x0_copia = copy.deepcopy(x0)

            # Registra el tiempo inicial.
            inicio = time.perf_counter()

            # Resuelve el sistema mediante Gauss-Seidel.
            resultado_seidel = self.resolver_seidel(
                A_copia,
                b_copia,
                x0_copia,
                tolerancia,
                max_iteraciones
            )

            # Registra el tiempo final.
            fin = time.perf_counter()

            # Guarda el tiempo que tardó esta ejecución.
            tiempos_seidel.append(fin - inicio)

        # Calcula las diferencias absolutas entre las soluciones
        # obtenidas por ambos métodos.
        diferencias = [
            abs(float(g) - float(s))
            for g, s in zip(solucion, resultado_seidel["solucion"])
        ]

        # Calcula el tiempo total utilizado por cada método.
        tiempo_gauss_total = sum(tiempos_gauss)
        tiempo_seidel_total = sum(tiempos_seidel)

        # Calcula el tiempo promedio de ejecución de cada método.
        promedio_gauss = tiempo_gauss_total / repeticiones
        promedio_seidel = tiempo_seidel_total / repeticiones

        # Compara los tiempos promedio para determinar cuál método fue más rápido.
        if promedio_gauss < promedio_seidel:

            # La eliminación gaussiana fue más rápida.
            metodo_mas_rapido = "Eliminación gaussiana"

            # Calcula cuántas veces fue más rápido este método.
            factor_rapidez = promedio_seidel / promedio_gauss if promedio_gauss > 0 else None

        elif promedio_seidel < promedio_gauss:

            # Gauss-Seidel fue más rápido.
            metodo_mas_rapido = "Gauss-Seidel"

            # Calcula cuántas veces fue más rápido este método.
            factor_rapidez = promedio_gauss / promedio_seidel if promedio_seidel > 0 else None

        else:

            # Ambos métodos tuvieron el mismo tiempo promedio.
            metodo_mas_rapido = "Ambos métodos tardaron lo mismo"
            factor_rapidez = 1

        # Retorna los resultados de la comparación.
        return {
            "repeticiones": repeticiones,
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

    # Lee un sistema desde un archivo CSV y lo valida.
    # Retorna (True, (A, b)) si todo está bien, o (False, "mensaje") si hay un error.
    def cargar_sistema_csv(self, ruta, n):

        # Lee el archivo y separa sus filas.
        ok, filas = leer_csv(ruta)
        if not ok:
            return False, filas

        # Comprueba que tenga n filas y n+1 columnas en cada fila.
        ok, mensaje = validar_forma(filas, n)
        if not ok:
            return False, mensaje

        # Convierte los textos a números y separa A y b.
        return validar_tabla(filas)

    # Genera automáticamente un sistema de ecuaciones aleatorio.
    def generar_sistema_aleatorio(self, n):

        # Comprueba que el tamaño del sistema sea al menos 2.
        if n < 2:
            raise ValueError("El tamaño debe ser al menos 2.")

        # Lista que almacenará la matriz de coeficientes A.
        A = []

        # Recorre las filas que tendrá la matriz.
        for i in range(n):
            fila = []

            # Recorre las columnas de cada fila.
            for j in range(n):

                # Inicialmente coloca cero en la diagonal principal.
                if i == j:
                    fila.append(0)

                # Para las demás posiciones genera números aleatorios entre -5 y 5.
                else:
                    fila.append(random.randint(-5, 5))

            # Suma los valores absolutos de los elementos de la fila.
            suma = sum(abs(valor) for valor in fila)

            # Asigna a la diagonal principal un valor mayor que la suma anterior.
            # Esto permite construir una matriz diagonalmente dominante.
            fila[i] = suma + random.randint(5, 10)

            # Agrega la fila completa a la matriz A.
            A.append(fila)

        # Genera una solución real aleatoria para las incógnitas.
        solucion_real = [random.randint(-5, 5) for _ in range(n)]

        # Lista que almacenará los resultados del vector independiente b.
        b = []

        # Calcula cada componente de b mediante el producto de A por la solución real.
        for i in range(n):
            valor = sum(A[i][j] * solucion_real[j] for j in range(n))
            b.append(valor)

        # Retorna la matriz de coeficientes y el vector independiente.
        return A, b

    # Ejecuta un experimento para comparar ambos métodos
    # utilizando sistemas de diferentes tamaños.
    def ejecutar_experimento(self, tamanos=None, tolerancia=0.000001, max_iteraciones=1000, repeticiones=3):

        # Si no se indican tamaños, utiliza los siguientes valores predeterminados.
        if tamanos is None: tamanos = [10, 20, 50, 100, 300]

        # Lista donde se almacenarán los resultados de cada experimento.
        resultados = []

        # Recorre cada tamaño de sistema que se desea evaluar.
        for n in tamanos:

            # Genera un sistema aleatorio de tamaño n.
            A, b = self.generar_sistema_aleatorio(n)

            # Establece un vector inicial compuesto por ceros.
            x0 = [0] * n

            # Ejecuta la comparación entre los dos métodos.
            resultado = self.comparar_metodos(A, b, x0, tolerancia, max_iteraciones, repeticiones)

            # Guarda los resultados importantes del experimento actual.
            resultados.append({
                "n": n,
                "tiempo_gauss": resultado["tiempo_gauss_promedio"],
                "tiempo_seidel": resultado["tiempo_seidel_promedio"],
                "iteraciones_seidel": resultado["iteraciones"],
                "convergencia": resultado["convergencia"]
            })

        # Retorna la lista con los resultados de todos los tamaños evaluados.
        return resultados