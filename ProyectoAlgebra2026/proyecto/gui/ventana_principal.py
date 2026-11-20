import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fractions import Fraction

class VentanaPrincipal(tk.Tk):

    def __init__(self, dominio):
        super().__init__()
        self.dominio = dominio
        self.title('Sistemas de ecuaciones lineales')
        self.geometry('800x600')
        self.resizable(False, False)
        self.crear_menu_principal()

    def limpiar_ventana(self):
        for elemento in self.winfo_children():
            elemento.destroy()

    def crear_titulo(self, texto, tamano=20):
        ttk.Label(self, text=texto, font=('Arial', tamano, 'bold')).pack(pady=25)

    def crear_boton(self, texto, accion, marco=None, **opciones):
        padre = marco if marco else self
        ttk.Button(padre, text=texto, command=accion).pack(pady=opciones.get('pady', 10))

    def mostrar_error(self, mensaje):
        messagebox.showerror('Dato incorrecto', mensaje)

    def crear_menu_principal(self):
        self.limpiar_ventana()
        self.crear_titulo('Sistemas de ecuaciones lineales', 22)
        self.crear_boton('1. Resolver y clasificar un sistema', self.pantalla_resolver)
        self.crear_boton('2. Comparar métodos', self.pantalla_comparar)
        self.crear_boton('Salir', self.destroy)

    def pantalla_resolver(self):
        self.limpiar_ventana()

        # Marco fijo para mantener visible el botón Volver
        marco_inferior = ttk.Frame(self)
        marco_inferior.pack(side='bottom', fill='x', pady=10)

        ttk.Button(
            marco_inferior,
            text='Volver al menú',
            command=self.crear_menu_principal
        ).pack()

        self.crear_titulo('Resolver y clasificar un sistema')

        marco = ttk.Frame(self)
        marco.pack(pady=15)

        ttk.Label(marco, text='Cantidad de incógnitas:').grid(row=0, column=0, padx=10)

        self.entrada_n = ttk.Entry(marco, width=10)
        self.entrada_n.grid(row=0, column=1, padx=5)

        ttk.Button(
            marco,
            text='Generar matriz',
            command=self.generar_matriz
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            marco,
            text='Cargar archivo CSV',
            command=self.cargar_csv
        ).grid(row=0, column=3, padx=5)

        self.marco_matriz = ttk.Frame(self)
        self.marco_matriz.pack(pady=15)

        self.entradas_matriz = []
        self.mostrar_pasos = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            self,
            text='Mostrar operaciones paso a paso',
            variable=self.mostrar_pasos
        ).pack(pady=5)


    def generar_matriz(self):
        try:
            n = int(self.entrada_n.get())
            if not 2 <= n <= 8:
                raise ValueError
        except ValueError:
            return self.mostrar_error('Ingrese un número entero entre 2 y 8.')
        for elemento in self.marco_matriz.winfo_children():
            elemento.destroy()
        self.entradas_matriz = []
        ttk.Label(self.marco_matriz, text='Ingrese los coeficientes y términos independientes:').grid(row=0, column=0, columnspan=n + 2, pady=10)
        for j in range(n + 1):
            encabezado = f'x{j + 1}' if j < n else 'b'
            ttk.Label(self.marco_matriz, text=encabezado, font=('Arial', 10, 'bold')).grid(row=1, column=j, padx=5)
        for i in range(n):
            fila = []
            for j in range(n + 1):
                entrada = ttk.Entry(self.marco_matriz, width=8)
                entrada.grid(row=i + 2, column=j, padx=5, pady=5)
                fila.append(entrada)
            self.entradas_matriz.append(fila)
        ttk.Button(self.marco_matriz, text='Resolver sistema', command=self.resolver_sistema).grid(row=n + 2, column=0, columnspan=n + 1, pady=15)

    def cargar_csv(self):
        ruta = filedialog.askopenfilename(title='Seleccionar archivo CSV', filetypes=[('Archivos CSV', '*.csv')])
        if not ruta:
            return
        try:
            with open(ruta, 'r', encoding='utf-8-sig') as archivo:
                filas = [linea.strip().split(',') for linea in archivo if linea.strip()]
            n = len(filas)
            if not 2 <= n <= 8:
                raise ValueError('El archivo debe tener entre 2 y 8 filas.')
            if any((len(fila) != n + 1 for fila in filas)):
                raise ValueError('Cada fila debe contener n+1 valores: los coeficientes y el término independiente.')
            datos = [[Fraction(valor.strip()) for valor in fila] for fila in filas]
            self.entrada_n.delete(0, tk.END)
            self.entrada_n.insert(0, str(n))
            self.generar_matriz()
            for i in range(n):
                for j in range(n + 1):
                    self.entradas_matriz[i][j].insert(0, str(datos[i][j]))
        except (ValueError, ZeroDivisionError):
            self.mostrar_error('El archivo CSV tiene datos inválidos o un formato incorrecto.')
        except OSError as error:
            self.mostrar_error(f'No se pudo abrir el archivo: {error}')

    def resolver_sistema(self):
        try:
            datos = [[Fraction(entrada.get().strip()) for entrada in fila] for fila in self.entradas_matriz]
            A = [fila[:-1] for fila in datos]
            b = [fila[-1] for fila in datos]
            matriz_inicial = [fila[:] + [b[i]] for i, fila in enumerate(A)]
            resultado = self.dominio.resolver_sistema(A, b)
            resultado['matrices'].insert(0, matriz_inicial)
            resultado['pasos'].insert(0, 'Matriz inicial')
            self.mostrar_resultados(resultado, A, b)
        except (ValueError, ZeroDivisionError):
            self.mostrar_error('Complete todas las casillas con números válidos.')
        except Exception as error:
            self.mostrar_error(f'No se pudo resolver: {error}')

    def formatear_ecuacion(self, fila, termino):
        partes = []
        for j, coeficiente in enumerate(fila):
            if coeficiente == 0:
                continue
            signo = '-' if coeficiente < 0 else '+'
            valor = abs(coeficiente)
            parte = f'x{j + 1}' if valor == 1 else f'{valor}x{j + 1}'
            if not partes:
                partes.append(('-' if coeficiente < 0 else '') + parte)
            else:
                partes.append(f' {signo} {parte}')
        if not partes:
            partes.append('0')
        return ''.join(partes) + f' = {termino}'

    def mostrar_resultados(self, resultado, A, b):
        ventana = tk.Toplevel(self)
        ventana.title('Resultados')
        ventana.geometry('600x500')
        texto = tk.Text(ventana, width=65, height=23)
        texto.pack(padx=15, pady=15)
        texto.insert(tk.END, f"Clasificación: {resultado['tipo']}\nRango de A: {resultado['rango_A']}\nRango de [A|b]: {resultado['rango_aumentada']}\n\nSistema ingresado:\n")
        for i in range(len(A)):
            texto.insert(tk.END, self.formatear_ecuacion(A[i], b[i]) + '\n')
        texto.insert(tk.END, '\nMatriz escalonada:\n')
        for fila in resultado['matriz']:
            texto.insert(tk.END, '   '.join(map(str, fila)) + '\n')
        if resultado['tipo'] == 'unica':
            texto.insert(tk.END, '\nSolución:\n')
            for i, valor in enumerate(resultado['solucion']):
                texto.insert(tk.END, f'x{i + 1} = {valor}\n')
            texto.insert(tk.END, f"\nComprobación Ax=b: {resultado['verificacion']}\n")
        elif resultado['tipo'] == 'infinitas':
            self.mostrar_solucion_general(ventana, texto, resultado, A, b)
        else:
            texto.insert(tk.END, '\nEl sistema no tiene solución.\n')
        texto.config(state='disabled')
        if self.mostrar_pasos.get():
            self.abrir_pasos(resultado)

    def abrir_pasos(self, resultado):
        ventana_pasos = tk.Toplevel(self)
        ventana_pasos.title('Operaciones paso a paso')
        ventana_pasos.geometry('500x400')
        matrices, pasos, indice = resultado['matrices'], resultado['pasos'], [0]
        etiqueta = ttk.Label(ventana_pasos, text='')
        etiqueta.pack(pady=10)
        texto_paso = tk.Text(ventana_pasos, width=45, height=12)
        texto_paso.pack(padx=15, pady=10)

        def actualizar_paso():
            posicion = indice[0]
            etiqueta.config(text=f'Paso {posicion + 1} de {len(matrices)}')
            texto_paso.config(state='normal')
            texto_paso.delete('1.0', tk.END)
            texto_paso.insert(tk.END, pasos[posicion] + '\n\n')
            for fila in matrices[posicion]:
                texto_paso.insert(tk.END, '   '.join(map(str, fila)) + '\n')
            texto_paso.config(state='disabled')
            boton_anterior.config(state='normal' if posicion > 0 else 'disabled')
            boton_siguiente.config(state='normal' if posicion < len(matrices) - 1 else 'disabled')

        def anterior():
            if indice[0] > 0:
                indice[0] -= 1
                actualizar_paso()

        def siguiente():
            if indice[0] < len(matrices) - 1:
                indice[0] += 1
                actualizar_paso()

        marco_botones = ttk.Frame(ventana_pasos)
        marco_botones.pack(pady=10)
        boton_anterior = ttk.Button(marco_botones, text='Anterior', command=anterior)
        boton_anterior.pack(side='left', padx=10)
        boton_siguiente = ttk.Button(marco_botones, text='Siguiente', command=siguiente)
        boton_siguiente.pack(side='left', padx=10)
        actualizar_paso()
    def mostrar_solucion_general(self, ventana, texto, resultado, A, b):
        general = resultado['general']
        libres = resultado['libres']
        texto.insert(tk.END, '\nVariables libres: ')
        texto.insert(tk.END, ', '.join((f'x{i + 1}' for i in libres)) + '\n\n')
        texto.insert(tk.END, 'Solución general:\n')
        for i, valores in enumerate(general):
            expresion = str(valores[0])
            for j in range(len(libres)):
                coeficiente = valores[j + 1]
                if coeficiente != 0:
                    signo = '+' if coeficiente > 0 else '-'
                    expresion += f' {signo} ({abs(coeficiente)})t{j + 1}'
            texto.insert(tk.END, f'x{i + 1} = {expresion}\n')
        marco = ttk.Frame(ventana)
        marco.pack(pady=5)
        entradas = []
        for j, variable in enumerate(libres):
            ttk.Label(marco, text=f'Valor de t{j + 1}:').grid(row=j, column=0, padx=5, pady=3)
            entrada = ttk.Entry(marco, width=10)
            entrada.grid(row=j, column=1, padx=5, pady=3)
            entradas.append(entrada)
        ttk.Button(marco, text='Calcular solución particular', command=lambda: self.calcular_particular(entradas, general, A, b, texto)).grid(row=len(libres), column=0, columnspan=2, pady=10)

    def calcular_particular(self, entradas, general, A, b, texto):
        try:
            valores = [Fraction(entrada.get().strip()) for entrada in entradas]
            solucion = []
            for variable in general:
                resultado = variable[0]
                for j in range(len(valores)):
                    resultado += variable[j + 1] * valores[j]
                solucion.append(resultado)
            Ax = [sum((A[i][j] * solucion[j] for j in range(len(A)))) for i in range(len(A))]
            correcto = all((abs(float(Ax[i] - b[i])) <= 1e-06 for i in range(len(b))))
            texto.config(state='normal')
            texto.insert(tk.END, '\nSolución particular:\n')
            for i, valor in enumerate(solucion):
                texto.insert(tk.END, f'x{i + 1} = {valor}\n')
            texto.insert(tk.END, f'\nComprobación Ax=b: {correcto}\n')
            texto.config(state='disabled')
        except (ValueError, ZeroDivisionError):
            self.mostrar_error('Ingrese valores válidos para todos los parámetros.')

    def pantalla_comparar(self):
        self.limpiar_ventana()
        self.crear_titulo('Comparación de métodos')
        ttk.Label(self, text='Seleccione cómo desea realizar la comparación:').pack(pady=15)
        ttk.Label(self, text='Comparación con un sistema ingresado manualmente').pack(pady=5)
        ttk.Label(self, text='Tamaño del sistema:').pack(pady=5)
        self.entrada_n_comparacion = ttk.Entry(self, width=12)
        self.entrada_n_comparacion.pack(pady=5)
        self.crear_boton('Continuar', self.crear_formulario_comparacion)
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=100, pady=15)
        ttk.Label(self, text='Experimento con matrices aleatorias').pack(pady=5)
        self.crear_boton('Ejecutar experimento', self.pantalla_experimento)
        self.crear_boton('Volver al menú', self.crear_menu_principal)

    def crear_formulario_comparacion(self):
        try:
            n = int(self.entrada_n_comparacion.get())
            if n < 2:
                raise ValueError
        except ValueError:
            self.mostrar_error('Ingrese un número entero mayor o igual que 2.')
            return
        self.limpiar_ventana()
        self.crear_titulo('Ingreso del sistema')
        ttk.Label(self, text=f'Ingrese la matriz A ({n}x{n}), el vector b y el vector inicial x0:').pack(pady=10)
        self.entradas_matriz = []
        self.entradas_b = []
        self.entradas_x0 = []
        contenedor = ttk.Frame(self)
        contenedor.pack(pady=10)
        ttk.Label(contenedor, text='Matriz A').grid(row=0, column=0, columnspan=n, pady=5)
        ttk.Label(contenedor, text='Vector b').grid(row=0, column=n, padx=10)
        ttk.Label(contenedor, text='Vector x0').grid(row=0, column=n + 1, padx=10)
        for i in range(n):
            fila = []
            for j in range(n):
                entrada = ttk.Entry(contenedor, width=8)
                entrada.grid(row=i + 1, column=j, padx=3, pady=3)
                fila.append(entrada)
            self.entradas_matriz.append(fila)
            entrada_b = ttk.Entry(contenedor, width=8)
            entrada_b.grid(row=i + 1, column=n, padx=5)
            self.entradas_b.append(entrada_b)
            entrada_x0 = ttk.Entry(contenedor, width=8)
            entrada_x0.grid(row=i + 1, column=n + 1, padx=5)
            self.entradas_x0.append(entrada_x0)
        self.usar_vector_cero = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text='Utilizar el vector cero como aproximación inicial', variable=self.usar_vector_cero, command=self.actualizar_vector_inicial).pack(pady=5)
        ttk.Label(self, text='Tolerancia:').pack(pady=3)
        self.entrada_tolerancia = ttk.Entry(self, width=15)
        self.entrada_tolerancia.insert(0, '0.000001')
        self.entrada_tolerancia.pack()
        ttk.Label(self, text='Máximo de iteraciones:').pack(pady=3)
        self.entrada_max_iteraciones = ttk.Entry(self, width=15)
        self.entrada_max_iteraciones.insert(0, '1000')
        self.entrada_max_iteraciones.pack()
        ttk.Label(self, text='Cantidad de repeticiones:').pack(pady=3)
        self.entrada_repeticiones = ttk.Entry(self, width=15)
        self.entrada_repeticiones.insert(0, '3')
        self.entrada_repeticiones.pack()
        self.crear_boton('Comparar métodos', self.procesar_comparacion)
        self.crear_boton('Volver', self.pantalla_comparar)

    def actualizar_vector_inicial(self):
        if self.usar_vector_cero.get():
            for entrada in self.entradas_x0:
                entrada.config(state='normal')
                entrada.delete(0, tk.END)
                entrada.insert(0, '0')
                entrada.config(state='disabled')
        else:
            for entrada in self.entradas_x0:
                entrada.config(state='normal')

    def procesar_comparacion(self):
        try:
            A = []
            for fila in self.entradas_matriz:
                valores = []
                for entrada in fila:
                    texto = entrada.get().strip()
                    if not texto:
                        raise ValueError('Debe completar todos los espacios de la matriz.')
                    valores.append(Fraction(texto))
                A.append(valores)
            b = []
            for entrada in self.entradas_b:
                texto = entrada.get().strip()
                if not texto:
                    raise ValueError('Debe completar todos los espacios del vector b.')
                b.append(Fraction(texto))
            if self.usar_vector_cero.get():
                x0 = [0] * len(A)
            else:
                x0 = []
                for entrada in self.entradas_x0:
                    texto = entrada.get().strip()
                    if not texto:
                        raise ValueError('Complete todos los valores del vector x0 o seleccione utilizar el vector cero.')
                    x0.append(Fraction(texto))
            tolerancia = float(self.entrada_tolerancia.get())
            max_iteraciones = int(self.entrada_max_iteraciones.get())
            repeticiones = int(self.entrada_repeticiones.get())
            if tolerancia <= 0:
                raise ValueError('La tolerancia debe ser positiva.')
            if max_iteraciones <= 0:
                raise ValueError('El máximo de iteraciones debe ser positivo.')
            if repeticiones <= 0:
                raise ValueError('La cantidad de repeticiones debe ser positiva.')
            resultado = self.dominio.comparar_metodos(A, b, x0, tolerancia, max_iteraciones, repeticiones)
            self.mostrar_resultados_comparacion(resultado)
        except (ValueError, ZeroDivisionError) as error:
            self.mostrar_error(str(error))
        except Exception as error:
            self.mostrar_error(f'No se pudo realizar la comparación: {error}')
    def mostrar_resultados_comparacion(self, resultado):
        ventana = tk.Toplevel(self)
        ventana.title('Resultados de la comparación')
        ventana.geometry('650x600')
        texto = tk.Text(ventana, width=75, height=30, wrap='word')
        texto.pack(padx=15, pady=15, fill='both', expand=True)
        texto.insert(tk.END, 'RESULTADOS DE LA COMPARACIÓN\n====================================\n\n')
        texto.insert(tk.END, 'Solución por eliminación gaussiana:\n')
        for i, valor in enumerate(resultado['solucion_gauss']):
            texto.insert(tk.END, f'x{i + 1} = {valor}\n')
        texto.insert(tk.END, '\nSolución por Gauss-Seidel:\n')
        for i, valor in enumerate(resultado['solucion_seidel']):
            texto.insert(tk.END, f'x{i + 1} = {valor:.10f}\n')
        texto.insert(tk.END, '\nDiferencia entre soluciones:\n')
        for i, valor in enumerate(resultado['diferencias']):
            texto.insert(tk.END, f'Diferencia en x{i + 1}: {valor:.10e}\n')
        texto.insert(tk.END, '\nRESULTADOS DE TIEMPO\n====================================\n')
        texto.insert(tk.END, f"Repeticiones: {len(resultado.get('tiempos_gauss', [])) or 'Consultar promedio'}\n")
        texto.insert(tk.END, f"Tiempo total de Gauss: {resultado['tiempo_gauss_total']:.8f} segundos\n")
        texto.insert(tk.END, f"Tiempo promedio de Gauss: {resultado['tiempo_gauss_promedio']:.8f} segundos\n\n")
        texto.insert(tk.END, f"Tiempo total de Gauss-Seidel: {resultado['tiempo_seidel_total']:.8f} segundos\n")
        texto.insert(tk.END, f"Tiempo promedio de Gauss-Seidel: {resultado['tiempo_seidel_promedio']:.8f} segundos\n\n")
        texto.insert(tk.END, f"Método más rápido: {resultado['metodo_mas_rapido']}\n")
        factor = resultado['factor_rapidez']
        if factor is not None:
            texto.insert(tk.END, f'Factor de rapidez: {factor:.2f} veces\n')
        texto.insert(tk.END, '\nRESULTADOS DE GAUSS-SEIDEL\n====================================\n')
        texto.insert(tk.END, f"Iteraciones realizadas: {resultado['iteraciones']}\n")
        texto.insert(tk.END, f"Error final: {resultado['error']:.10e}\n")
        texto.insert(tk.END, f"¿Convergió?: {resultado['convergencia']}\n")
        if not resultado['diagonalmente_dominante']:
            texto.insert(tk.END, '\nADVERTENCIA:\nLa matriz no es diagonalmente dominante. Gauss-Seidel podría no converger.\n')
        if not resultado['convergencia']:
            texto.insert(tk.END, '\nNO SE ALCANZÓ LA TOLERANCIA:\nGauss-Seidel llegó al máximo de iteraciones sin alcanzar la tolerancia solicitada.\nSe recomienda aumentar el máximo de iteraciones. La solución de Gauss sí está disponible.\n')
        texto.config(state='disabled')
        ttk.Button(ventana, text='Cerrar', command=ventana.destroy).pack(pady=10)

    def pantalla_experimento(self):
        self.limpiar_ventana()
        self.crear_titulo('Modo experimento')
        ttk.Label(self, text='Se generarán sistemas aleatorios diagonalmente dominantes.').pack(pady=10)
        ttk.Label(self, text='Tamaños: 10, 20, 50, 100, 300 y 500').pack(pady=5)
        ttk.Label(self, text='Tolerancia:').pack(pady=3)
        self.entrada_tolerancia_experimento = ttk.Entry(self, width=15)
        self.entrada_tolerancia_experimento.insert(0, '0.000001')
        self.entrada_tolerancia_experimento.pack()
        ttk.Label(self, text='Máximo de iteraciones:').pack(pady=3)
        self.entrada_iteraciones_experimento = ttk.Entry(self, width=15)
        self.entrada_iteraciones_experimento.insert(0, '1000')
        self.entrada_iteraciones_experimento.pack()
        ttk.Label(self, text='Cantidad de repeticiones:').pack(pady=3)
        self.entrada_repeticiones_experimento = ttk.Entry(self, width=15)
        self.entrada_repeticiones_experimento.insert(0, '3')
        self.entrada_repeticiones_experimento.pack()
        self.crear_boton('Iniciar experimento', self.ejecutar_experimento_interfaz)
        self.crear_boton('Volver', self.pantalla_comparar)

    def ejecutar_experimento_interfaz(self):
        try:
            tolerancia = float(self.entrada_tolerancia_experimento.get())
            max_iteraciones = int(self.entrada_iteraciones_experimento.get())
            repeticiones = int(self.entrada_repeticiones_experimento.get())
            if tolerancia <= 0:
                raise ValueError('La tolerancia debe ser positiva.')
            if max_iteraciones <= 0:
                raise ValueError('El máximo de iteraciones debe ser positivo.')
            if repeticiones <= 0:
                raise ValueError('Las repeticiones deben ser positivas.')
            respuesta = messagebox.askyesno('Confirmar experimento', 'Se ejecutarán seis pruebas, incluyendo sistemas de tamaño 500.\n\nEl proceso puede tardar varios minutos. ¿Desea continuar?')
            if not respuesta:
                return
            resultados = self.dominio.ejecutar_experimento(tolerancia=tolerancia, max_iteraciones=max_iteraciones, repeticiones=repeticiones)
            self.mostrar_tabla_experimento(resultados)
        except (ValueError, ZeroDivisionError) as error:
            self.mostrar_error(str(error))
        except Exception as error:
            self.mostrar_error(f'No se pudo ejecutar el experimento: {error}')

    def mostrar_tabla_experimento(self, resultados):
        ventana = tk.Toplevel(self)
        ventana.title('Resultados del experimento')
        ventana.geometry('850x400')
        ttk.Label(ventana, text='Resultados del experimento', font=('Arial', 16, 'bold')).pack(pady=15)
        columnas = ('n', 'gauss', 'seidel', 'iteraciones', 'convergencia')
        tabla = ttk.Treeview(ventana, columns=columnas, show='headings')
        tabla.heading('n', text='Tamaño n')
        tabla.heading('gauss', text='Gauss (segundos)')
        tabla.heading('seidel', text='Gauss-Seidel (segundos)')
        tabla.heading('iteraciones', text='Iteraciones')
        tabla.heading('convergencia', text='Convergencia')
        tabla.column('n', width=80, anchor='center')
        tabla.column('gauss', width=160, anchor='center')
        tabla.column('seidel', width=190, anchor='center')
        tabla.column('iteraciones', width=120, anchor='center')
        tabla.column('convergencia', width=120, anchor='center')
        for resultado in resultados:
            tabla.insert('', tk.END, values=(resultado['n'], f"{resultado['tiempo_gauss']:.8f}", f"{resultado['tiempo_seidel']:.8f}", resultado['iteraciones_seidel'], 'Sí' if resultado['convergencia'] else 'No'))
        tabla.pack(fill='both', expand=True, padx=15, pady=10)
        ttk.Button(ventana, text='Cerrar', command=ventana.destroy).pack(pady=10)