from logic.lectura import leer_csv
from logic.validaciones import validar_forma, validar_tabla

ok, filas = leer_csv("prueba.csv")

if ok:
    print(validar_forma(filas, 3))

    if validar_forma(filas, 3)[0]:
        print(validar_tabla(filas))


#codgo de prueba, se borra todo el archivo