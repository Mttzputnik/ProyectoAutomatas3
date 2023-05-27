import json

from models.model import Automata


class Controller:
    def __init__(self, automata=Automata):
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
        # Crear un diccionario con los atributos del objeto Automata
        automata_data = {
            'states': list(self.Automata.States),
            'alphabet': list(self.Automata.Alphabet),
            'transitions': self.Automata.Transitions,
            'initial_state': self.Automata.InitialState,
            'final_states': list(self.Automata.FinalStates),
            'is_complete': self.Automata.isComplete
        }

        # Codificar el diccionario en formato JSON.
        data = json.dumps(automata_data)

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


    def ConvertToDFA(self):
        dfa_states = set()
        dfa_alphabet = self.Automata.Alphabet
        dfa_transitions = {}
        dfa_initial_state = ""
        dfa_final_states = set()

        # Obtener el cierre-épsilon del estado inicial
        initial_closure = self.EpsilonClosure([self.Automata.InitialState])

        # Crear el estado inicial del AFD
        dfa_initial_state = ",".join(sorted(initial_closure))
        dfa_states.add(dfa_initial_state)

        # Crear una cola para procesar los nuevos estados del AFD
        queue = [dfa_initial_state]

        while queue:
            current_state = queue.pop(0).split(",")

            for symbol in self.Automata.Alphabet:
                new_state = self.EpsilonClosure(
                    self.GetNextStates(current_state, symbol))

                if new_state:
                    new_state_str = ",".join(sorted(new_state))

                    if new_state_str not in dfa_states:
                        dfa_states.add(new_state_str)
                        queue.append(new_state_str)

                    dfa_transitions[tuple(current_state)] = dfa_transitions.get(
                        tuple(current_state), {})
                    dfa_transitions[tuple(current_state)][symbol] = new_state_str

        # Determinar los estados finales del AFD
        for state in dfa_states:
            for final_state in self.Automata.FinalStates:
                if final_state in state.split(","):
                    dfa_final_states.add(state)

        # Verificar si el estado inicial es final
        if self.Automata.InitialState in self.Automata.FinalStates:
            dfa_final_states.add(dfa_initial_state)

        # Crear el nuevo AFD
        dfa = Automata(
            states=list(dfa_states),
            alphabet=dfa_alphabet,
            transitions=dfa_transitions,
            initial_state=dfa_initial_state,
            final_states=list(dfa_final_states),
            is_complete=True
        )

        dfa.PrintAutomata()

        return dfa



    def EpsilonClosure(self, states):
        closure = set(states)
        queue = list(states)

        while queue:
            current_state = queue.pop(0)

            if current_state in self.Automata.Transitions:
                if "" in self.Automata.Transitions[current_state]:
                    epsilon_transitions = self.Automata.Transitions[current_state][""]
                    for state in epsilon_transitions:
                        if state not in closure:
                            closure.add(state)
                            queue.append(state)

        return closure

    def GetNextStates(self, states, symbol):
        next_states = set()

        for state in states:
            if state in self.Automata.Transitions and symbol in self.Automata.Transitions[state]:
                next_states.update(self.Automata.Transitions[state][symbol])

        return next_states
