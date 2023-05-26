from models.model import Automata
from controllers.controller import Controller
from views.view2 import View

def main():
    # Inicializar el modelo
    automata = Automata(
       states=["q0", "q1", "q2"],
    alphabet=["a", "b"],
    transitions={
        "q0": {
            "a": "q1",
            "b": "q2",
        },
        "q1": {
            "a": "q0",
            "b": "q2",
        },
        "q2": {
            "a": "q2",
            "b": "q1",
        },
    },
    initial_state="q0",
    final_states=["q2"],
    is_complete=False
    )

    # Inicializar el controlador
    controller = Controller(automata)

    # Inicializar la vista
    view = View(controller)

    # Ejecutar la vista
    view.Run()

if __name__ == "__main__":
    main()
