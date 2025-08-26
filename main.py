# from tkinter import *
# from tkinter import messagebox
# from tkinter import ttk
# from modelo import *
# import modelo


# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import modelo  # tu archivo peewee con guardar_partido()

class Vista:
    def __init__(self, window):

        self.root = window
        self.root.title("DOPARTI")

        s = ttk.Style()
        temas = s.theme_names()
        if "vista" in temas:          # Windows
            s.theme_use("vista")
        elif "xpnative" in temas:     # Windows más viejo
            s.theme_use("xpnative")
        elif "default" in temas:
            s.theme_use("default")
        else:
            s.theme_use(temas[0])

        self.mostrar_treeview()
        self.actualizar_treeview()
        # --- Título ---
        ttk.Label(self.root, text="Ingrese una descripción").grid(row=0, column=0, columnspan=2, sticky="we", padx=8, pady=(8,4))

        # --- Descripción ---
        ttk.Label(self.root, text="Descripción:").grid(row=1, column=0, sticky="e", padx=8, pady=4)
        self.descripcion = ttk.Entry(self.root, width=40)
        self.descripcion.grid(row=1, column=1, sticky="w", padx=8, pady=4)

        # --- Fecha (DateEntry) ---
        ttk.Label(self.root, text="Fecha:").grid(row=2, column=0, sticky="e", padx=8, pady=4)
        self.fecha = DateEntry(
            self.root,
            date_pattern="dd/MM/yyyy",   # muestra dd/mm/aaaa
            firstweekday="monday",        # semana comienza lunes
            showweeknumbers=False,
            locale="es"                   # nombres en español (siempre que tu sistema lo tenga)
        )
        self.fecha.grid(row=2, column=1, sticky="w", padx=8, pady=4)

        # --- Orden ---
        ttk.Label(self.root, text="Orden:").grid(row=3, column=0, sticky="e", padx=8, pady=4)
        self.orden = ttk.Spinbox(self.root, from_=1, to=9999, width=5)
        self.orden.set(1)
        self.orden.grid(row=3, column=1, sticky="w", padx=8, pady=4)

        # --- Botón Guardar ---
        self.btn_guardar = ttk.Button(self.root, text="Guardar", command=self.guardar)
        self.btn_guardar.grid(row=4, column=0, columnspan=2, pady=12)

        # algo de padding general
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)

    def guardar(self):
        descripcion = self.descripcion.get().strip()
        if not descripcion:
            messagebox.showwarning("Falta descripción", "Ingresá una descripción.")
            return

        try:
            fecha_sel = self.fecha.get_date()# devuelve datetime.date
            orden = int(self.orden.get())
            #fecha = datetime.strptime(fecha_sel, '%d/%m/%Y').date()

            # Si tu modelo usa DateField -> mandamos date (OK)
            # Si tu modelo usa DateTimeField, convertir: datetime.combine(fecha_sel, datetime.min.time())
            modelo.guardar_partido(fecha_sel, descripcion, orden)


            messagebox.showinfo("Guardado", f"Se guardó el evento '{descripcion}' para el {fecha_sel.strftime('%d/%m/%Y')}.")
            self.actualizar_treeview()
            self.descripcion.delete(0, tk.END)
            self.orden.set(1)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar.\n{e}")

    
    def mostrar_treeview(self):
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"]=("col1", "col2", "col3")
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.heading("col1", text="Orden")
        self.tree.heading("col2", text="Descripcion")
        self.tree.heading("col3", text="fecha")
        self.tree.grid(row=10, column=0, columnspan=3)


    def actualizar_treeview(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        resultado = modelo.ver_partidos()
        for fila in resultado:
            print(fila)
            self.tree.insert("", 0, values=(fila[0], fila[1], fila[2]))


if __name__ == "__main__":
    root = tk.Tk()
    # Opcional: tema ttk
    try:
        from tkinter import ttk
        root.style = ttk.Style()
        root.style.theme_use("clam")
    except:
        pass

    app = Vista(root)
    app.actualizar_treeview()
    root.mainloop()
