import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fractions import Fraction

# Colores de la interfaz (tonos rosa suaves).
FONDO = '#FFF5F8'
PANEL = '#FFE4EC'
BORDE = '#F3C1D3'
ACENTO = '#E58FAE'
ACENTO_OSCURO = '#D06A91'
TEXTO = '#5A3A46'
TITULO = '#B84A75'
LETRA = 'Segoe UI'

class VentanaPrincipal(tk.Tk):

    def __init__(self, dominio):
        super().__init__()
        self.dominio = dominio
        self.aplicar_estilo()
        self.title('Sistemas de ecuaciones lineales')
        self.geometry('800x600')
        self.resizable(False, False)
        self.crear_area_desplazable()
        self.crear_menu_principal()

    # Define los colores y las fuentes de todos los elementos (ttk).
    def aplicar_estilo(self):
        self.configure(bg=FONDO)
        estilo = ttk.Style(self)
        estilo.theme_use('clam')
        estilo.configure('.', background=FONDO, foreground=TEXTO, font=(LETRA, 11))
        estilo.configure('TFrame', background=FONDO)
        estilo.configure('TLabel', background=FONDO, foreground=TEXTO)
        estilo.configure('Titulo.TLabel', background=FONDO, foreground=TITULO)
        estilo.configure('TButton', background=ACENTO, foreground='white', font=(LETRA, 11, 'bold'),
                         padding=(14, 7), borderwidth=0, focusthickness=0, focuscolor=ACENTO)
        estilo.map('TButton', background=[('pressed', ACENTO_OSCURO), ('active', ACENTO_OSCURO)])
        estilo.configure('TEntry', fieldbackground='white', foreground=TEXTO, bordercolor=BORDE,
                         lightcolor=BORDE, darkcolor=BORDE, padding=4)
        estilo.map('TEntry', bordercolor=[('focus', ACENTO)], lightcolor=[('focus', ACENTO)])
        estilo.configure('TCheckbutton', background=FONDO, foreground=TEXTO)
        estilo.map('TCheckbutton', background=[('active', FONDO)], indicatorcolor=[('selected', ACENTO)])
        estilo.configure('Treeview', background='white', fieldbackground='white', foreground=TEXTO,
                         rowheight=26, bordercolor=BORDE)
        estilo.configure('Treeview.Heading', background=PANEL, foreground=TITULO, font=(LETRA, 11, 'bold'),
                         relief='flat')
        estilo.map('Treeview', background=[('selected', ACENTO)], foreground=[('selected', 'white')])
        estilo.map('Treeview.Heading', background=[('active', BORDE)])
        estilo.configure('Vertical.TScrollbar', background=BORDE, troughcolor=FONDO, bordercolor=FONDO,
                         arrowcolor=TEXTO)
        estilo.configure('Horizontal.TScrollbar', background=BORDE, troughcolor=FONDO, bordercolor=FONDO,
                         arrowcolor=TEXTO)

    # Da el color de fondo a una ventana secundaria.
    def estilizar_ventana(self, ventana):
        ventana.configure(bg=FONDO)

    # Da colores y fuente a un cuadro de texto (tk.Text no usa ttk).
    def estilizar_texto(self, texto):
        texto.configure(bg='white', fg=TEXTO, font=('Consolas', 11), relief='flat', padx=12, pady=10,
                        highlightthickness=1, highlightbackground=BORDE, highlightcolor=ACENTO,
                        selectbackground=BORDE, selectforeground=TEXTO)

    # Crea el área con barras de desplazamiento donde se dibujan todas las pantallas.
    def crear_area_desplazable(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg=FONDO, highlightthickness=0, yscrollincrement=20, xscrollincrement=20)
        barra_vertical = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        barra_horizontal = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=barra_vertical.set, xscrollcommand=barra_horizontal.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        barra_vertical.grid(row=0, column=1, sticky='ns')
        barra_horizontal.grid(row=1, column=0, sticky='ew')
        # Marco interno: aquí van todos los elementos de cada pantalla.
        self.area = ttk.Frame(self.canvas)
        self.ventana_area = self.canvas.create_window((0, 0), window=self.area, anchor='nw')
        self.area.bind('<Configure>', self.actualizar_region)
        self.canvas.bind('<Configure>', self.actualizar_region)
        # Rueda del mouse: vertical sola, horizontal con Shift.
        self.bind_all('<MouseWheel>', self.rueda_vertical)
        self.bind_all('<Shift-MouseWheel>', self.rueda_horizontal)

    # Ajusta el tamaño del marco y la zona que se puede desplazar.
    # El marco nunca es más pequeño que la ventana, así el contenido queda centrado.
    def actualizar_region(self, evento=None):
        ancho = max(self.canvas.winfo_width(), self.area.winfo_reqwidth())
        alto = max(self.canvas.winfo_height(), self.area.winfo_reqheight())
        self.canvas.itemconfigure(self.ventana_area, width=ancho, height=alto)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    # Desplaza hacia arriba o abajo con la rueda (solo en la ventana principal).
    def rueda_vertical(self, evento):
        try:
            if evento.widget.winfo_toplevel() is not self:
                return
        except (AttributeError, tk.TclError):
            return
        self.canvas.yview_scroll(-1 if evento.delta > 0 else 1, 'units')

    # Desplaza a los lados con Shift + rueda.
    def rueda_horizontal(self, evento):
        try:
            if evento.widget.winfo_toplevel() is not self:
                return
        except (AttributeError, tk.TclError):
            return
        self.canvas.xview_scroll(-1 if evento.delta > 0 else 1, 'units')

    def limpiar_ventana(self):
        for elemento in self.area.winfo_children():
            elemento.destroy()

    def crear_titulo(self, texto, tamano=20):
        ttk.Label(self.area, text=texto, style='Titulo.TLabel', font=(LETRA, tamano, 'bold')).pack(pady=25)

    def crear_boton(self, texto, accion, marco=None, **opciones):
        padre = marco if marco else self.area
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
        self.crear_titulo('Resolver y clasificar un sistema')
        marco = ttk.Frame(self.area)
        marco.pack(pady=15)
        ttk.Label(marco, text='Cantidad de incógnitas:').grid(row=0, column=0, padx=10)
        self.entrada_n = ttk.Entry(marco, width=10)
        self.entrada_n.grid(row=0, column=1, padx=5)
        ttk.Button(marco, text='Generar matriz', command=self.generar_matriz).grid(row=0, column=2, padx=5)
        ttk.Button(marco, text='Cargar archivo CSV', command=self.cargar_csv).grid(row=0, column=3, padx=5)
        self.marco_matriz = ttk.Frame(self.area)
        self.marco_matriz.pack(pady=15)
        self.entradas_matriz = []
        self.mostrar_pasos = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.area, text='Mostrar operaciones paso a paso', variable=self.mostrar_pasos).pack(pady=5)
        self.crear_boton('Volver al menú', self.crear_menu_principal)

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
            ttk.Label(self.marco_matriz, text=encabezado, font=(LETRA, 10, 'bold')).grid(row=1, column=j, padx=5)
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
        self.estilizar_ventana(ventana)
        ventana.title('Resultados')
        ventana.geometry('600x500')
        texto = tk.Text(ventana, width=65, height=23)
        self.estilizar_texto(texto)
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
        self.estilizar_ventana(ventana_pasos)
        ventana_pasos.title('Operaciones paso a paso')
        ventana_pasos.geometry('500x400')
        matrices, pasos, indice = resultado['matrices'], resultado['pasos'], [0]
        etiqueta = ttk.Label(ventana_pasos, text='')
        etiqueta.pack(pady=10)
        texto_paso = tk.Text(ventana_pasos, width=45, height=12)
        self.estilizar_texto(texto_paso)
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
        ttk.Label(self.area, text='Seleccione cómo desea realizar la comparación:').pack(pady=15)
        ttk.Label(self.area, text='Comparación con un sistema ingresado manualmente').pack(pady=5)
        ttk.Label(self.area, text='Tamaño del sistema:').pack(pady=5)
        self.entrada_n_comparacion = ttk.Entry(self.area, width=12)
        self.entrada_n_comparacion.pack(pady=5)
        self.crear_boton('Continuar', self.crear_formulario_comparacion)
        ttk.Separator(self.area, orient='horizontal').pack(fill='x', padx=100, pady=15)
        ttk.Label(self.area, text='Experimento con matrices aleatorias').pack(pady=5)
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
        if n > 8:
            self.crear_formulario_grande(n)
            return
        self.limpiar_ventana()
        self.crear_titulo('Ingreso del sistema')
        ttk.Label(self.area, text=f'Ingrese la matriz A ({n}x{n}), el vector b y el vector inicial x0:').pack(pady=10)
        self.entradas_matriz = []
        self.entradas_b = []
        self.entradas_x0 = []
        contenedor = ttk.Frame(self.area)
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
        ttk.Checkbutton(self.area, text='Utilizar el vector cero como aproximación inicial', variable=self.usar_vector_cero, command=self.actualizar_vector_inicial).pack(pady=5)
        ttk.Label(self.area, text='Tolerancia:').pack(pady=3)
        self.entrada_tolerancia = ttk.Entry(self.area, width=15)
        self.entrada_tolerancia.insert(0, '0.000001')
        self.entrada_tolerancia.pack()
        ttk.Label(self.area, text='Máximo de iteraciones:').pack(pady=3)
        self.entrada_max_iteraciones = ttk.Entry(self.area, width=15)
        self.entrada_max_iteraciones.insert(0, '1000')
        self.entrada_max_iteraciones.pack()
        ttk.Label(self.area, text='Cantidad de repeticiones:').pack(pady=3)
        self.entrada_repeticiones = ttk.Entry(self.area, width=15)
        self.entrada_repeticiones.insert(0, '3')
        self.entrada_repeticiones.pack()
        self.crear_boton('Comparar métodos', self.procesar_comparacion)
        self.crear_boton('Volver', self.pantalla_comparar)

    # Pantalla para sistemas grandes (n mayor que 8): no se muestra la tabla,
    # el sistema se carga desde un CSV o se genera al azar.
    def crear_formulario_grande(self, n):
        self.limpiar_ventana()
        self.crear_titulo(f'Sistema de tamaño {n}', 18)
        self.sistema_grande = None
        ttk.Label(self.area, text='Para este tamaño no se muestra la tabla.\nCargue un archivo CSV o genere un sistema al azar.').pack(pady=5)
        self.etiqueta_sistema = ttk.Label(self.area, text='Todavía no hay un sistema cargado.')
        self.etiqueta_sistema.pack(pady=5)
        marco = ttk.Frame(self.area)
        marco.pack(pady=5)
        ttk.Button(marco, text='Cargar archivo CSV', command=lambda: self.cargar_csv_grande(n)).grid(row=0, column=0, padx=5)
        ttk.Button(marco, text='Generar sistema al azar', command=lambda: self.generar_sistema_grande(n)).grid(row=0, column=1, padx=5)
        ttk.Label(self.area, text='Aproximación inicial (n valores separados por coma, o vacío para el vector cero):').pack(pady=3)
        self.entrada_x0_grande = ttk.Entry(self.area, width=40)
        self.entrada_x0_grande.pack()
        ttk.Label(self.area, text='Tolerancia:').pack(pady=2)
        self.entrada_tolerancia = ttk.Entry(self.area, width=15)
        self.entrada_tolerancia.insert(0, '0.000001')
        self.entrada_tolerancia.pack()
        ttk.Label(self.area, text='Máximo de iteraciones:').pack(pady=2)
        self.entrada_max_iteraciones = ttk.Entry(self.area, width=15)
        self.entrada_max_iteraciones.insert(0, '1000')
        self.entrada_max_iteraciones.pack()
        ttk.Label(self.area, text='Cantidad de repeticiones:').pack(pady=2)
        self.entrada_repeticiones = ttk.Entry(self.area, width=15)
        self.entrada_repeticiones.insert(0, '3')
        self.entrada_repeticiones.pack()
        self.crear_boton('Comparar métodos', lambda: self.procesar_comparacion_grande(n), pady=5)
        self.crear_boton('Volver', self.pantalla_comparar, pady=5)

    # Carga el sistema grande desde un archivo CSV (a través del dominio).
    def cargar_csv_grande(self, n):
        ruta = filedialog.askopenfilename(title='Seleccionar archivo CSV', filetypes=[('Archivos CSV', '*.csv')])
        if not ruta:
            return
        ok, resultado = self.dominio.cargar_sistema_csv(ruta, n)
        if not ok:
            self.mostrar_error(resultado)
            return
        self.sistema_grande = resultado
        self.etiqueta_sistema.config(text=f'Sistema de {n} x {n} cargado desde el archivo CSV.')

    # Genera un sistema aleatorio diagonalmente dominante de tamaño n.
    def generar_sistema_grande(self, n):
        self.sistema_grande = self.dominio.generar_sistema_aleatorio(n)
        self.etiqueta_sistema.config(text=f'Sistema aleatorio de {n} x {n} generado.')

    # Convierte el texto de una casilla en un número, con un mensaje claro si falla.
    def leer_numero(self, entrada, nombre, tipo):
        try:
            return tipo(entrada.get().strip())
        except ValueError:
            if tipo is int:
                raise ValueError(f'{nombre} debe ser un número entero.')
            raise ValueError(f'{nombre} debe ser un número válido.')

    # Compara los métodos con el sistema grande ya cargado o generado.
    def procesar_comparacion_grande(self, n):
        try:
            if self.sistema_grande is None:
                raise ValueError('Primero cargue un archivo CSV o genere un sistema al azar.')
            A, b = self.sistema_grande
            texto_x0 = self.entrada_x0_grande.get().strip()
            if texto_x0 == '':
                x0 = [0] * n
            else:
                valores = [valor.strip() for valor in texto_x0.split(',')]
                if len(valores) != n:
                    raise ValueError(f'La aproximación inicial debe tener exactamente {n} valores.')
                try:
                    x0 = [Fraction(valor) for valor in valores]
                except ValueError:
                    raise ValueError('La aproximación inicial solo puede tener números.')
            tolerancia = self.leer_numero(self.entrada_tolerancia, 'La tolerancia', float)
            max_iteraciones = self.leer_numero(self.entrada_max_iteraciones, 'El máximo de iteraciones', int)
            repeticiones = self.leer_numero(self.entrada_repeticiones, 'La cantidad de repeticiones', int)
            if tolerancia <= 0:
                raise ValueError('La tolerancia debe ser positiva.')
            if max_iteraciones <= 0:
                raise ValueError('El máximo de iteraciones debe ser positivo.')
            if repeticiones <= 0:
                raise ValueError('La cantidad de repeticiones debe ser positiva.')
            resultado = self.dominio.comparar_metodos(A, b, x0, tolerancia, max_iteraciones, repeticiones)
            self.mostrar_resultados_comparacion(resultado)
        except ZeroDivisionError:
            self.mostrar_error('La aproximación inicial tiene una división entre cero.')
        except ValueError as error:
            self.mostrar_error(str(error))
        except Exception as error:
            self.mostrar_error(f'No se pudo realizar la comparación: {error}')

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
        self.estilizar_ventana(ventana)
        ventana.title('Resultados de la comparación')
        ventana.geometry('650x600')
        texto = tk.Text(ventana, width=75, height=30, wrap='word')
        self.estilizar_texto(texto)
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
        texto.insert(tk.END, f"Repeticiones: {resultado['repeticiones']}\n")
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
        ttk.Label(self.area, text='Se generarán sistemas aleatorios diagonalmente dominantes.').pack(pady=10)
        ttk.Label(self.area, text='Tamaños: 10, 20, 50, 100 y 300').pack(pady=5)
        ttk.Label(self.area, text='Tolerancia:').pack(pady=3)
        self.entrada_tolerancia_experimento = ttk.Entry(self.area, width=15)
        self.entrada_tolerancia_experimento.insert(0, '0.000001')
        self.entrada_tolerancia_experimento.pack()
        ttk.Label(self.area, text='Máximo de iteraciones:').pack(pady=3)
        self.entrada_iteraciones_experimento = ttk.Entry(self.area, width=15)
        self.entrada_iteraciones_experimento.insert(0, '1000')
        self.entrada_iteraciones_experimento.pack()
        ttk.Label(self.area, text='Cantidad de repeticiones:').pack(pady=3)
        self.entrada_repeticiones_experimento = ttk.Entry(self.area, width=15)
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
            respuesta = messagebox.askyesno('Confirmar experimento', 'Se ejecutarán cinco pruebas (n = 10, 20, 50, 100 y 300).\n\nEl proceso puede tardar unos segundos. ¿Desea continuar?')
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
        self.estilizar_ventana(ventana)
        ventana.title('Resultados del experimento')
        ventana.geometry('850x400')
        ttk.Label(ventana, text='Resultados del experimento', style='Titulo.TLabel', font=(LETRA, 16, 'bold')).pack(pady=15)
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