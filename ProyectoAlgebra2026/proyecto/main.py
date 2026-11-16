from domain.dominio import Dominio
from gui.ventana_principal import VentanaPrincipal 

def main():
    dominio = Dominio()
    ventana = VentanaPrincipal(dominio)
    ventana.mainloop()

if __name__ == "__main__":
    main()
    