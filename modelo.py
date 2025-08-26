import sqlite3
from peewee import *
from datetime import datetime


# ---- Peewee ----
db = SqliteDatabase('partidos.db')
 
class BaseModel(Model):
    class Meta:
        database = db
 
class Evento(BaseModel):
    fecha = DateField()
    descripcion = CharField()
    orden = IntegerField()
 
db.connect()
db.create_tables([Evento])
 
# ---- Tkinter ----
def guardar_partido(fecha, descripcion, orden):
    fecha = fecha
        # Limpiar texto
    descripcion = descripcion
    orden = int(orden)
 
    # Guardar en la base de datos
    Evento.create(fecha = fecha, descripcion = descripcion, orden = orden)
    print("Guardado", f"Fecha {fecha} guardada en la base de datos.")


def ver_partidos():
    qs = Evento.select(Evento.orden, Evento.descripcion, Evento.fecha)
    return list(qs.tuples())

def eliminar_partido(id):
    Evento.delete_by_id(id)
    print("Se elimino el evento: ", id)