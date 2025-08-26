import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import modelo
 
class Vista:
    def __init__(self, window):
        self.root = window
        self.root.title("DOPARTI")
        self.evento_sel_id = None 
 
        s = ttk.Style()
        temas = s.theme_names()
        if "vista" in temas:
            s.theme_use("vista")
        elif "default" in temas:
            s.theme_use("default")
 
        # --- Título ---
        ttk.Label(self.root, text="Ingrese los datos del evento deportivo.").grid(
            row=0, column=0, columnspan=4, sticky="we", padx=8, pady=(8,4)
        )
 
        # --- Descripción ---
        ttk.Label(self.root, text="Descripción:").grid(row=1, column=0, sticky="e", padx=8, pady=4)
        self.descripcion = ttk.Entry(self.root, width=40)
        self.descripcion.grid(row=1, column=1, sticky="w", padx=8, pady=4)
 
        # --- Fecha (DateEntry) ---
        ttk.Label(self.root, text="Fecha:").grid(row=2, column=0, sticky="e", padx=8, pady=4)
        self.fecha = DateEntry(self.root, date_pattern="dd/MM/yyyy",
                               firstweekday="monday", showweeknumbers=False, locale="es", state="readonly")
        self.fecha.grid(row=2, column=1, sticky="w", padx=8, pady=4)
 
        # --- Orden ---
        ttk.Label(self.root, text="Orden:").grid(row=3, column=0, sticky="e", padx=8, pady=4)
        self.orden = ttk.Spinbox(self.root, from_=1, to=9999, width=5)
        self.orden.set(1)
        self.orden.grid(row=3, column=1, sticky="w", padx=8, pady=4)
 
        # --- Botones ---
        ttk.Button(self.root, text="Guardar", command=self.guardar).grid(row=4, column=0, pady=12)
        ttk.Button(self.root, text="Editar (cargar)", command=self.editar_cargar).grid(row=4, column=1, pady=12, sticky="w")
        ttk.Button(self.root, text="Actualizar", command=self.actualizar).grid(row=4, column=2, pady=12, sticky="w")
        ttk.Button(self.root, text="Eliminar", command=self.eliminar).grid(row=4, column=3, pady=12, sticky="w")
 
        # --- Treeview ---
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("col1", "col2", "col3")  # Orden, Descripción, Fecha
        self.tree.column("#0", width=0, stretch=False)   # oculto: ID del objeto
        self.tree.heading("#0", text="")
        self.tree.column("col1", width=120, anchor="center")
        self.tree.column("col2", width=300, anchor="w")
        self.tree.column("col3", width=120, anchor="center")
        self.tree.heading("col1", text="Orden")
        self.tree.heading("col2", text="Descripción")
        self.tree.heading("col3", text="Fecha")
        self.tree.grid(row=10, column=0, columnspan=4, sticky="nsew", padx=8, pady=8)
 
        # Layout
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(10, weight=1)
 
        # Cargar datos
        self.actualizar_treeview()
 
    # ---------- Rutinas ----------
    def guardar(self):
        res = modelo.guardar_partido(self.fecha, self.descripcion, self.orden)
        if res == "ok":
            messagebox.showinfo("Guardado", "Evento guardado correctamente.")
            self.actualizar_treeview()
            self._limpiar_form()
        else:
            messagebox.showerror("Error", res)
 
    def editar_cargar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccioná un elemento del listado.")
            return
        indice = sel[0]
        eid = self.tree.item(indice).get("text")  # ID del objeto
        datos = modelo.obtener_partido(int(eid))
        if not datos:
            messagebox.showerror("Error", "No se encontró el registro seleccionado.")
            return
 
        # datos = (id, orden, descripcion, fecha)
        self.evento_sel_id = datos[0]
        orden, desc, fecha = datos[1], datos[2], datos[3]
 
        self.orden.set(orden)
        self.descripcion.delete(0, tk.END)
        self.descripcion.insert(0, desc)
        try:
            self.fecha.set_date(fecha)
        except Exception:
            pass
 
        messagebox.showinfo("Editar", "Registro cargado en el formulario. Modificá y presioná 'Actualizar'.")
 
    def actualizar(self):
        if not self.evento_sel_id:
            messagebox.showwarning("Atención", "Primero cargá un registro con el botón 'Editar (cargar)'.")
            return
        res = modelo.actualizar_partido(self.evento_sel_id, self.fecha, self.descripcion, self.orden)
        if res == "ok":
            messagebox.showinfo("OK", "Evento actualizado.")
            self.actualizar_treeview()
            self._limpiar_form()
            self.evento_sel_id = None
        else:
            messagebox.showerror("Error", res)
 
    def eliminar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccioná un elemento del listado.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el/los elemento(s) seleccionado(s)?"):
            return
 
        errores = []
        for indice in sel:
            eid = self.tree.item(indice).get("text")
            r = modelo.eliminar_partido(int(eid))
            if r == "ok":
                self.tree.delete(indice)
            else:
                errores.append(r)
        if errores:
            messagebox.showerror("Error", "\n".join(errores))
        else:
            messagebox.showinfo("OK", "Elemento(s) eliminado(s).")
 
    def actualizar_treeview(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        for (eid, orden, desc, fecha) in (modelo.ver_partidos() or []):
            fecha_str = getattr(fecha, "strftime", lambda *_: str(fecha))("%d/%m/%Y")
            self.tree.insert("", "end", text=eid, values=(orden, desc, fecha_str))
 
    # ---------- Aux ----------
    def _limpiar_form(self):
        self.descripcion.delete(0, tk.END)
        self.orden.set(1)
 
if __name__ == "__main__":
    root = tk.Tk()
    Vista(root)
    root.mainloop()