from fractions import Fraction
import csv #este no se borra

def convertir_a_fraccion(texto):
    texto = texto.strip() #eliminamos los espacios al inicio y al final
    if texto == "":
        return False, "La casilla está vacía"

    texto = texto.replace(",", ".") #eliminamos los espacios en medio
    
    try: 
        numero = Fraction(texto) #convertimos el texto en una fraccion exacta
        return True, numero

    except ZeroDivisionError:
        return False, "No se puede dividir por cero"

    except ValueError:
        return False, "El valor ingresado no es un número válido"   

#vamos a leer el archivo que de el profe
def leer_csv(ruta):
    try:
        with open(ruta, newline="", encoding="utf-8-sig") as archivo: #el enconding evita problemas con archivos de excel
            lector =csv.reader(archivo,delimiter=",") #funcion para leer el contenido, y la coma indica que las columnas están separadas por eso
            filas = list(lector)

        #eliminamos todas las filas vacías
        filas_validas = []
        for fila in filas:
            vacia =True
            for casilla in fila:
                if casilla.strip() != "":
                    vacia = False
            if not vacia:
                filas_validas.append(fila)
        return True, filas_validas
    except FileNotFoundError:
        return False, "No se encontró el archivo CSV"

    except PermissionError:
        return False, "No se puede acceder al archivo. Ciérrelo si está abierto en Excel"

    except UnicodeDecodeError:
        return False, "El archivo tiene una codificación no compatible"

    except csv.Error:
        return False, "Error al leer el contenido del archivo CSV"

    except OSError:
        return False, "Ocurrió un error al abrir o leer el archivo"
    




if __name__ == "__main__":

    pruebas = ["1 2", " 7 ", "-2.5", "3/4", "1,5", "", "abc", "3/0", "--3"]

    for texto in pruebas:
        resultado = convertir_a_fraccion(texto)
        print(texto, "->", resultado)

#probar la lectura del csv

    print("Prueba de leer_csv:")

    resultado = leer_csv("prueba.csv")
    print(resultado)

    print("\nPrueba de archivo inexistente:")

    resultado = leer_csv("no_existe.csv")
    print(resultado)