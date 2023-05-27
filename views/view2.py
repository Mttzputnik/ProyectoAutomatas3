import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
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
        filepath = fd.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filepath:
            error = self.controller.LoadAutomataFromFile(filepath)
            if error is not None:
                messagebox.showerror("Error", "Error al cargar el archivo: " + error)
            else:
                messagebox.showinfo("Información", "Autómata cargado correctamente")

    def LoadAutomatonFromInput(self):
        data = self.input_entry2.get()
        if data:
            error = self.controller.LoadAutomataFromString(data)
            if error is not None:
                messagebox.showerror("Error", "Error al cargar el autómata: " + error)
            else:
                messagebox.showinfo("Información", "Autómata cargado correctamente")

    def SaveAutomataToFile(self):
        filepath = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filepath:
            error = self.controller.SaveAutomataToFile(filepath)
            if error is not None:
                messagebox.showerror("Error", "Error al guardar el archivo: " + error)
            else:
                messagebox.showinfo("Información", "Autómata guardado correctamente")

    def ConvertToAFD(self):
        afd = self.controller.ConvertToDFA()
        if afd is not None:
            messagebox.showinfo("Información", "Autómata convertido a AFD correctamente")
        else:
            messagebox.showerror("Error", "Error al convertir el autómata a AFD")


    def VisualizeAutomata(self):
        self.controller.VisualizeAutomata()
        return None
    


    def Run(self):
        root = tk.Tk()
        root.title("Verificador de autómatas")
        root.geometry("400x450")

        # Crear los componentes de la interfaz
        label_home = tk.Label(root, text="¿Qué desea hacer?")
        load_file_button = tk.Button(root, text="Cargar autómata desde archivo", command=self.LoadAutomataFromFile, )
        label_automata = tk.Label(root, text="Ingrese una Automata manualmente:")
        load_input_button = tk.Button(root, text="Cargar autómata desde entrada manual", command=self.LoadAutomatonFromInput)
        self.input_entry2 = tk.Entry(root, width = 50)
        label_string= tk.Label(root, text="Ingrese una cadena para verificar:")
        self.input_entry = tk.Entry(root, width = 50)
        verify_button = tk.Button(root, text="Verificar", command=self.VerifyString)
        save_file_button = tk.Button(root, text="Guardar autómata en archivo", command=self.SaveAutomataToFile)
        visualize_button = tk.Button(root, text="Visualizar autómata", command=self.VisualizeAutomata)
        convert_button = tk.Button(root, text="Convertir a AFD", command=self.ConvertToAFD)
        

        # Colocar los componentes en la ventana
        label_home.pack(padx=10, pady=5)

        load_file_button.pack(padx=25, pady=20)

        label_automata.pack(padx=10, pady=5)
        self.input_entry2.pack(padx=25, pady=5)
        load_input_button.pack(padx=25, pady=5)
        

        label_string.pack(padx=25, pady=5)
        self.input_entry.pack(padx=25, pady=5)
        verify_button.pack(padx=25, pady=5)
        
        
        save_file_button.pack(padx=25, pady=10)
        visualize_button.pack(padx=25, pady=10)
        convert_button.pack(padx=25, pady=10)

        root.mainloop()
