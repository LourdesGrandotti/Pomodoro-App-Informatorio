# Pruebas funcionales (tester)

import unittest

from menu import Aplicacion

class test_Aplicacion(unittest.TestCase):
        
    def test_app(self):

        if Aplicacion.agregar_tarea:
            print("debe iniciar el cronometro")
        else:
            print("Debe agregar tarea")
        if Aplicacion.iniciar_cronometro:
            print("la aplicacion se ha ejecutado")
        else:
            print("La aplicacion no funciona")


if __name__ == "__main__":
    unittest.main()

        

