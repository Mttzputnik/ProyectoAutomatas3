import json

from models.model import Automata


class Controller:
    def __init__(self, automata = Automata):
        self.Automata = automata

    def LoadAutomataFromFile(self, filepath):
        # Intenta cargar el archivo especificado.
        try:
            with open(filepath, 'r') as file:
                data = file.read()
        except IOError as e:
            return e

        # Decodifica el archivo JSON en un autómata.
        try:
            automata_data = json.loads(data)
            automata = Automata(
                states=automata_data['states'],
                alphabet=automata_data['alphabet'],
                transitions=automata_data['transitions'],
                initial_state=automata_data['initial_state'],
                final_states=automata_data['final_states'],
                is_complete=automata_data['is_complete']
            )
        except (json.JSONDecodeError, KeyError) as e:
            return e

        # Asigna el autómata cargado al controlador.
        self.Automata = automata

        return None

    def LoadAutomataFromString(self, data):
        # Decodifica la cadena de entrada JSON en un autómata.
        try:
            automata_data = json.loads(data)
            automata = Automata(
                states=automata_data['states'],
                alphabet=automata_data['alphabet'],
                transitions=automata_data['transitions'],
                initial_state=automata_data['initial_state'],
                final_states=automata_data['final_states'],
                is_complete=automata_data['is_complete']
            )
        except (json.JSONDecodeError, KeyError) as e:
            return e

        # Asigna el autómata cargado al controlador.
        self.Automata = automata

        return None
	

    
    def SaveAutomataToFile(self, filepath):
        # Codifica el autómata en formato JSON.
        data = json.dumps(self.Automata)

        # Escribe el archivo.
        try:
            with open(filepath, 'w') as file:
                file.write(data)
        except IOError as e:
            return e

        return None

    def CheckString(self, string):
        if self.Automata is None:
            return False, Exception("Automata no definido")

        # Comprueba que el autómata sea completo y lo completa si es necesario.
        try:
            self.Automata.CheckCompleteness()
        except Exception as e:
            return False, e

        # Comprueba si la cadena es aceptada por el autómata.
        return self.Automata.Accept(string), None
