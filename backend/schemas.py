from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ClientBase(BaseModel):
    permisionario: str
    codigo: str
    nombres: str
    apellidos: str
    cliente: str
    cedula_ruc: str
    servicio_contratado: str
    plan_contratado: str
    provincia: str
    ciudad: str
    direccion: str
    telefono: str
    correo: str
    fecha_de_inscripcion: str
    estado: str
    


class ClientCreate(BaseModel):
    nombres:str
    correo:str
    telefono:str
    
class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True

class ReclamationBase(BaseModel):
    item: str
    provincia: str
    mes: str
    fecha_hora_registro: str
    nombre_reclamante: str
    telefono_contacto: str
    tipo_conexion: str
    canal_reclamo: str
    tipo_reclamo: str
    fecha_hora_solucion: str
    tiempo_resolucion: str
    descripcion_solucion: str
    permisionario: str
    softr_record_id: str

class ReclamationCreate(ReclamationBase):
    pass

class Reclamation(ReclamationBase):
    id: int

    class Config:
        from_attributes = True

class RepairTimeBase(BaseModel):
    item: str
    provincia: str
    nombre_requerimiento: str
    telefono_contacto: str
    tipo_conexion: str
    canal_requerimiento: str
    tipo_averia: str
    fecha_hora_reporte: str
    fecha_hora_reparacion: str
    tiempo_reparacion: str
    descripcion_solucion: str
    permisionario: str
    softr_record_id: str

class RepairTimeCreate(RepairTimeBase):
    pass

class RepairTime(RepairTimeBase):
    id: int

    class Config:
        from_attributes = True

class AdministratorBase(BaseModel):
    usuario: str
    permisionario: str

class AdministratorCreate(AdministratorBase):
    contrasena: str

class Administrator(AdministratorBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    permisionario: Optional[str] = None