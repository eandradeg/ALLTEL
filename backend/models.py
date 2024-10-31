from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "alltel_clients"
    id = Column(Integer, primary_key=True, index=True)
    permisionario = Column(Text)
    codigo = Column(Text)
    nombres = Column(Text)
    apellidos = Column(Text)
    cliente = Column(Text)
    cedula_ruc = Column(Text)
    servicio_contratado = Column(Text)
    plan_contratado = Column(Text)
    provincia = Column(Text)
    ciudad = Column(Text)
    direccion = Column(Text)
    telefono = Column(Text)
    correo = Column(Text)
    fecha_de_inscripcion = Column(Text)
    estado = Column(Text)
    
    reclamations = relationship("Reclamation", back_populates="client")
    capacity_reclamations = relationship("CapacityReclamation", back_populates="client")
    repair_times = relationship("RepairTime", back_populates="client")
    reports = relationship("Report", back_populates="client")

class Reclamation(Base):
    __tablename__ = "alltel_reclamations"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(Text)
    provincia = Column(Text)
    mes = Column(Text)
    fecha_hora_registro = Column(Text)
    nombre_reclamante = Column(Text)
    telefono_contacto = Column(Text)
    tipo_conexion = Column(Text)
    canal_reclamo = Column(Text)
    tipo_reclamo = Column(Text)
    fecha_hora_solucion = Column(Text)
    tiempo_resolucion = Column(Text)
    descripcion_solucion = Column(Text)
    permisionario = Column(Text, ForeignKey("alltel_clients.permisionario"))
    softr_record_id = Column(Text)
    
    client = relationship("Client", back_populates="reclamations")

class CapacityReclamation(Base):
    __tablename__ = "alltel_capacity_reclamations"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(Text)
    provincia = Column(Text)
    fecha_hora_registro = Column(Text)
    nombre_reclamante = Column(Text)
    telefono_contacto = Column(Text)
    canal_reclamo = Column(Text)
    capacidad_efectiva_contratada = Column(Text)
    comparticion = Column(Text)
    capacidad_suministrada = Column(Text)
    descripcion_solucion = Column(Text)
    permisionario = Column(Text, ForeignKey("alltel_clients.permisionario"))
    
    client = relationship("Client", back_populates="capacity_reclamations")

class RepairTime(Base):
    __tablename__ = "alltel_repair_times"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(Text)
    provincia = Column(Text)
    nombre_requerimiento = Column(Text)
    telefono_contacto = Column(Text)
    tipo_conexion = Column(Text)
    canal_requerimiento = Column(Text)
    tipo_averia = Column(Text)
    fecha_hora_reporte = Column(Text)
    fecha_hora_reparacion = Column(Text)
    tiempo_reparacion = Column(Text)
    descripcion_solucion = Column(Text)
    permisionario = Column(Text, ForeignKey("alltel_clients.permisionario"))
    softr_record_id = Column(Text)
    
    client = relationship("Client", back_populates="repair_times")

class Report(Base):
    __tablename__ = "alltel_reports"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(Text)
    tipo_reporte = Column(Text)
    mes = Column(Text)
    ano = Column(Text)
    ubicacion_archivo = Column(Text)
    permisionario = Column(Text, ForeignKey("alltel_clients.permisionario"))
    descarga = Column(Text)
    
    client = relationship("Client", back_populates="reports")

class Administrator(Base):
    __tablename__ = "alltel_administrators"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(Text)
    contrasena = Column(Text)
    permisionario = Column(Text, ForeignKey("alltel_clients.permisionario"))