from peewee import *
from datetime import datetime
 
db = SqliteDatabase('partidos.db')
 
class BaseModel(Model):
    class Meta:
        database = db
 
class Evento(BaseModel):
    fecha = DateField()
    descripcion = CharField()
    orden = IntegerField()
 
db.connect()
db.create_tables([Evento], safe=True) 
 
def guardar_partido(fecha_widget, descripcion_widget, orden_widget):
    descripcion = (descripcion_widget.get() or "").strip()
    
    if(descripcion == ""):
        return "error: la descripcion no debe estar vacia"
    
    if hasattr(fecha_widget, "get_date"):
        fecha = fecha_widget.get_date()            
    else:
        raw = (fecha_widget.get() or "").strip()
        fecha = datetime.strptime(raw, "%d/%m/%Y").date()
    
    orden_str = (orden_widget.get() or "").strip()
    if not orden_str.isdigit():
        return "error: el orden debe ser un número entero positivo"

    orden = int(orden_str)
    
    Evento.create(fecha=fecha, descripcion=descripcion, orden=orden)
    return "ok"
 
def ver_partidos():
    qs = (Evento
          .select(Evento.id, Evento.orden, Evento.descripcion, Evento.fecha)
          .order_by(Evento.id.asc()))
    return list(qs.tuples())
 
def obtener_partido(evento_id: int):
    try:
        e = Evento.get_by_id(evento_id)
        return (e.id, e.orden, e.descripcion, e.fecha)
    except Evento.DoesNotExist:
        return None
 
def actualizar_partido(evento_id: int, fecha_widget, descripcion_widget, orden_widget):
    try:
        e = Evento.get_by_id(evento_id)
 
        desc = (descripcion_widget.get() or "").strip()
        if not desc:
            return "error: la descripción está vacía"
 
        if hasattr(fecha_widget, "get_date"):
            fec = fecha_widget.get_date()
        else:
            raw = (fecha_widget.get() or "").strip()
            try:
                fec = datetime.strptime(raw, "%d/%m/%Y").date()
            except ValueError:
                fec = datetime.strptime(raw, "%Y-%m-%d").date()
 
        ordn = int(orden_widget.get())
 
        e.descripcion = desc
        e.fecha = fec
        e.orden = ordn
        e.save()
        return "ok"
    except Evento.DoesNotExist:
        return "error: id inexistente"
    except Exception as e:
        return f"error: {e}"
 
def eliminar_partido(evento_id: int):
    try:
        borr = Evento.delete_by_id(evento_id)
        return "ok" if borr else "error: id inexistente"
    except Exception as e:
        return f"error: {e}"