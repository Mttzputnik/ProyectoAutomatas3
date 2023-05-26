import tkinter as tk
from tkinter import messagebox
from controllers.controller import Controller

class View:
    def __init__(self, controller = Controller):
        self.controller = controller

    def VerifyString(self):
        input_str = self.input_entry.get()

        is_accepted, error = self.controller.CheckString(input_str)
        if error is not None:
            messagebox.showerror("Error", "Error al verificar la cadena: " + error)
        elif is_accepted:
            messagebox.showinfo("Resultado", "La cadena '" + input_str + "' es aceptada por el autómata")
        else:
            messagebox.showinfo("Resultado", "La cadena '" + input_str + "' no es aceptada por el autómata")

    def LoadAutomataFromFile(self):
        filepath = tk.filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filepath:
            error = self.controller.LoadAutomataFromFile(filepath)
            if error is not None:
                messagebox.showerror("Error", "Error al cargar el archivo: " + error)
            else:
                messagebox.showinfo("Información", "Autómata cargado correctamente")

    def LoadAutomatonFromInput(self):
        data = self.input_text.get("1.0", "end-1c")
        if data:
            error = self.controller.LoadAutomataFromString(data)
            if error is not None:
                messagebox.showerror("Error", "Error al cargar el autómata: " + error)
            else:
                messagebox.showinfo("Información", "Autómata cargado correctamente")

    def SaveAutomataToFile(self):
        filepath = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filepath:
            error = self.controller.SaveAutomataToFile(filepath)
            if error is not None:
                messagebox.showerror("Error", "Error al guardar el archivo: " + error)
            else:
                messagebox.showinfo("Información", "Autómata guardado correctamente")

    def VisualizeAutomata(self):
        # Lógica para visualizar el autómata en un lienzo gráfico
        return None

    def Run(self):
        root = tk.Tk()
        root.title("Verificador de autómatas")

        # Crear los componentes de la interfaz
        label = tk.Label(root, text="Ingrese una cadena para verificar:")
        self.input_entry = tk.Entry(root)
        verify_button = tk.Button(root, text="Verificar", command=self.VerifyString)
        load_file_button = tk.Button(root, text="Cargar autómata desde archivo", command=self.LoadAutomataFromFile)
        load_input_button = tk.Button(root, text="Cargar autómata desde entrada manual", command=self.LoadAutomatonFromInput)
        save_file_button = tk.Button(root, text="Guardar autómata en archivo", command=self.SaveAutomataToFile)
        visualize_button = tk.Button(root, text="Visualizar autómata", command=self.VisualizeAutomata)

        # Colocar los componentes en la ventana
        label.pack()
        self.input_entry.pack()
        verify_button.pack()
        load_file_button.pack()
        load_input_button.pack()
        save_file_button.pack()
        visualize_button.pack()

        root.mainloop()
