import json
import tkinter as tk

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
        dfa_states = []
        dfa_transitions = {}
        dfa_initial_state = set()
        dfa_final_states = []
        dfa_alphabet = self.Automata.Alphabet

        # Obtener el cierre-épsilon del estado inicial
        initial_closure = self.EpsilonClosure([self.Automata.InitialState])

        # Crear el estado inicial del AFD
        dfa_initial_state.update(initial_closure)
        dfa_states.append(dfa_initial_state)

        # Crear una cola para procesar los nuevos estados del AFD
        queue = [dfa_initial_state]

        while queue:
            current_state = queue.pop(0)

            for symbol in self.Automata.Alphabet:
                new_state = self.EpsilonClosure(self.GetNextStates(current_state, symbol))

                if new_state not in dfa_states:
                    dfa_states.append(new_state)
                    queue.append(new_state)

                dfa_transitions[tuple(sorted(current_state))] = dfa_transitions.get(tuple(sorted(current_state)), {})
                dfa_transitions[tuple(sorted(current_state))][symbol] = tuple(sorted(new_state))

        # Determinar los estados finales del AFD
        for state in dfa_states:
            for final_state in self.Automata.FinalStates:
                if final_state in state:
                    dfa_final_states.append(state)
                    break

        # Crear el nuevo AFD
        dfa = Automata(
            states=dfa_states,
            alphabet=dfa_alphabet,
            transitions=dfa_transitions,
            initial_state=dfa_initial_state,
            final_states=dfa_final_states,
            is_complete=True
        )

        dfa.PrintAutomata()

        return dfa


    def EpsilonClosure(self, states):
        closure = set(states)

        queue = list(states)
        while queue:
            current_state = queue.pop(0)
            if "" in self.Automata.Transitions[current_state]:
                epsilon_states = self.Automata.Transitions[current_state][""]
                for state in epsilon_states:
                    if state not in closure:
                        closure.add(state)
                        queue.append(state)

        return closure

    def GetNextStates(self, states, symbol):
        next_states = set()

        for state in states:
            if symbol in self.Automata.Transitions[state]:
                next_states.update(self.Automata.Transitions[state][symbol])

        return next_states

    def VisualizeAutomata(self):
        automata = self.Automata

        # Crear una nueva ventana para mostrar el autómata
        window = tk.Toplevel()
        window.title("Visualizar autómata")

        # Crear un lienzo gráfico más grande para dibujar el autómata
        canvas_width = 400
        canvas_height = 400
        canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
        canvas.pack()

        # Variables para ajustar las posiciones y tamaños de los elementos en el lienzo
        state_radius = 30
        state_margin_x = 100
        state_margin_y = 100
        state_coordinates = {}  # Diccionario para almacenar las coordenadas de los estados

        # Dibujar los estados
        x = state_margin_x
        y = state_margin_y
        for state in automata.States:
            if state == automata.InitialState:
                canvas.create_oval(x - state_radius, y - state_radius, x + state_radius, y + state_radius, fill="green")  # Estado inicial (verde)
            elif state in automata.FinalStates:
                canvas.create_oval(x - state_radius, y - state_radius, x + state_radius, y + state_radius, fill="red")  # Estados finales (rojo)
            else:
                canvas.create_oval(x - state_radius, y - state_radius, x + state_radius, y + state_radius)  # Estados normales

            canvas.create_text(x, y, text=state)  # Etiqueta del estado

            state_coordinates[state] = (x, y)  # Almacenar las coordenadas del estado

            # Ajustar la posición horizontal para el próximo estado
            x += state_margin_x
            if x + state_margin_x > canvas_width - state_margin_x:
                x = state_margin_x
                y += state_margin_y

        # Dibujar las transiciones
        for state, transitions in automata.Transitions.items():
            x1, y1 = state_coordinates[state]  # Coordenadas del estado actual

            for symbol, target_state in transitions.items():
                x2, y2 = state_coordinates[target_state]  # Coordenadas del estado destino

                # Dibujar la flecha de la transición
                canvas.create_line(x1, y1 + state_radius, x2, y2 - state_radius, arrow=tk.LAST)

                # Calcular la posición del símbolo en la flecha
                symbol_x = (x1 + x2) / 2
                symbol_y = (y1 + y2) / 2

                # Mostrar el símbolo de transición
                canvas.create_text(symbol_x, symbol_y, text=symbol)

        window.mainloop()

