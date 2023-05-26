import os

from controllers.controller import Controller

class View:
    def __init__(self, controller = Controller):
        self.Controller = controller

    def GetInput(self):
        input_str = input("Ingrese una cadena para verificar: ")

        isAccepted, err = self.Controller.CheckString(input_str)
        if err is not None:
            print("Error al verificar la cadena:", err)
        elif isAccepted:
            print("La cadena", input_str, "es aceptada por el autómata")
        else:
            print("La cadena", input_str, "no es aceptada por el autómata")

    def Run(self):
        while True:
            print("¿Qué desea hacer?")
            print("1. Cargar autómata desde archivo")
            print("2. Cargar autómata desde entrada manual")
            print("3. Guardar autómata en archivo")
            print("4. Verificar cadena")
            print("5. Visualizar automata")
            print("6. Salir")
            input_str = input()

            if input_str == "1":
                filepath = input("Ingrese la ruta del archivo: ")
                err = self.Controller.LoadAutomataFromFile(filepath)
                if err is not None:
                    print("Error al cargar el archivo:", err)
                else:
                    print("Autómata cargado correctamente")
            elif input_str == "2":
                data = input("Ingrese el autómata en formato JSON: ")
                err = self.Controller.LoadAutomataFromString(data)
                if err is not None:
                    print("Error al cargar el autómata:", err)
                else:
                    print("Autómata cargado correctamente")
            elif input_str == "3":
                filepath = input("Ingrese la ruta del archivo: ")
                err = self.Controller.SaveAutomataToFile(filepath)
                if err is not None:
                    print("Error al guardar el archivo:", err)
                else:
                    print("Autómata guardado correctamente")
            elif input_str == "4":
                self.GetInput()

            elif input_str == "5":
               self.Controller.Automata.PrintAutomata() 

            elif input_str == "6":
                print("Saliendo...")
                os._exit(0)
            else:
                print("Opción inválida")
