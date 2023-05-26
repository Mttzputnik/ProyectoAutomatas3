class Automata:
    def __init__(self, states, alphabet, transitions, initial_state, final_states, is_complete):
        self.States = states
        self.Alphabet = alphabet
        self.Transitions = transitions
        self.InitialState = initial_state
        self.FinalStates = final_states
        self.isComplete = is_complete

    def Complete(self):
        # Agregar estado sumidero
        self.States.append("sumidero")
        for symbol in self.Alphabet:
            self.Transitions["sumidero"] = {symbol: "sumidero"}
        for state in self.States:
            for symbol in self.Alphabet:
                if symbol not in self.Transitions[state]:
                    self.Transitions[state][symbol] = "sumidero"
        self.isComplete = True

    def CheckCompleteness(self):
        if not self.isComplete:
            return ValueError("Automata is incomplete")
        for state in self.States:
            if "" not in self.Transitions[state]:
                return ValueError("Automata is incomplete")
            for sym in self.Alphabet:
                if sym not in self.Transitions[state]:
                    return ValueError("Automata is incomplete")
        return None

    def Accept(self, cadena):
        estadoActual = self.InitialState
        for simbolo in cadena:
            if estadoActual not in self.Transitions or simbolo not in self.Transitions[estadoActual]:
                return False
            estadoActual = self.Transitions[estadoActual][simbolo]
        return estadoActual in self.FinalStates

    
    def PrintAutomata(self):
        print("Estados:", self.States)
        print("Alfabeto:", self.Alphabet)
        print("Transiciones:")
        for state, transitions in self.Transitions.items():
            print(f"   {state}: {transitions}")
        print("Estado inicial:", self.InitialState)
        print("Estados finales:", self.FinalStates)
        print("Completo:", self.isComplete)