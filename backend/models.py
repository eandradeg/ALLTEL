from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from .database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    permisionario = Column(String)
    codigo = Column(String)
    nombres = Column(String)
    apellidos = Column(String)
    cliente = Column(String)
    cedula_ruc = Column(String)
    servicio_contratado = Column(String)
    plan_contratado = Column(String)
    provincia = Column(String)
    ciudad = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    correo = Column(String, unique=True, index=True)
    fecha_de_inscripcion = Column(String)
    estado = Column(String)
    
    #reclamations = relationship("Reclamation", back_populates="client")
    #capacity_reclamations = relationship("CapacityReclamation", back_populates="client")
    #repair_times = relationship("RepairTime", back_populates="client")
    #reports = relationship("Report", back_populates="client")

