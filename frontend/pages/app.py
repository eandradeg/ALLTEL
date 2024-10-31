import streamlit as st
import pandas as pd
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend import models
from backend.database import SessionLocal, engine
from datetime import datetime
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Sistema de Gestión de Clientes", layout="wide")

# URLs de la API
API_URL = "http://127.0.0.1:8000"
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def create_client(client_data):
    db = get_db()
    try:
        db_client = models.Client(
            permisionario=client_data.get("permisionario"),
            codigo=client_data.get("codigo"),
            nombres=client_data.get("nombres"),
            apellidos=client_data.get("apellidos"),
            cliente=client_data.get("cliente"),
            cedula_ruc=client_data.get("cedula_ruc"),
            servicio_contratado=client_data.get("servicio_contratado"),
            plan_contratado=client_data.get("plan_contratado"),
            provincia=client_data.get("provincia"),
            ciudad=client_data.get("ciudad"),
            direccion=client_data.get("direccion"),
            telefono=client_data.get("telefono"),
            correo=client_data.get("correo"),
            fecha_de_inscripcion=client_data.get("fecha_de_inscripcion"),
            estado=client_data.get("estado")
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return True
    except Exception as e:
        db.rollback()
        st.error(f"Error al crear cliente: {str(e)}")
        return False
    finally:
        db.close()

def get_clients():
    db = get_db()
    try:
        return db.query(models.Client).all()
    finally:
        db.close()

def delete_client(client_id):
    db = get_db()
    try:
        client = db.query(models.Client).filter(models.Client.id == client_id).first()
        if client:
            db.delete(client)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        st.error(f"Error al eliminar cliente: {str(e)}")
        return False
    finally:
        db.close()
        

# Título principal
st.title("🏢 Sistema de Gestión de Clientes y Reclamos")

# Menú lateral
menu = st.sidebar.selectbox(
    "Menú",
    ["Dashboard", "Gestión de Clientes", "Gestión de Reclamos"]
)


if menu == "Dashboard":
    st.header("📊 Dashboard")
    
    # Obtener todos los clientes
    clients = get_clients()
    
    # Mostrar estadísticas básicas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Clientes", len(clients))
    with col2:
        activos = len([c for c in clients if c.estado == "Activo"])
        st.metric("Clientes Activos", activos)
    with col3:
        inactivos = len([c for c in clients if c.estado == "Inactivo"])
        st.metric("Clientes Inactivos", inactivos)
    
    # Mostrar tabla de clientes
    if clients:
        df = pd.DataFrame([{
            "ID": c.id,
            "Nombres": c.nombres,
            "Apellidos": c.apellidos,
            "Email": c.correo,
            "Teléfono": c.telefono,
            "Estado": c.estado
        } for c in clients])
        st.dataframe(df)

elif menu == "Gestión de Clientes":
    st.header("👥 Gestión de Clientes")
    
    with st.form("nuevo_cliente"):
        col1, col2 = st.columns(2)
        
        with col1:
            permisionario = st.text_input("Permisionario")
            codigo = st.text_input("Código")
            nombres = st.text_input("Nombres")
            apellidos = st.text_input("Apellidos")
            cliente = st.text_input("Cliente")
            cedula_ruc = st.text_input("Cédula/RUC")
            servicio_contratado = st.selectbox("Servicio Contratado", ["INTERNET", "TV", "INTERNET+TV"])
            plan_contratado = st.text_input("Plan Contratado")
            
        with col2:
            provincia = st.text_input("Provincia")
            ciudad = st.text_input("Ciudad")
            direccion = st.text_input("Dirección")
            telefono = st.text_input("Teléfono")
            correo = st.text_input("Correo")
            fecha_inscripcion = st.date_input("Fecha de Inscripción")
            estado = st.selectbox("Estado", ["ACTIVO", "INACTIVO"])
        
        submitted = st.form_submit_button("Guardar Cliente")
        
        if submitted:
            client_data = {
                "permisionario": permisionario,
                "codigo": codigo,
                "nombres": nombres,
                "apellidos": apellidos,
                "cliente": cliente,
                "cedula_ruc": cedula_ruc,
                "servicio_contratado": servicio_contratado,
                "plan_contratado": plan_contratado,
                "provincia": provincia,
                "ciudad": ciudad,
                "direccion": direccion,
                "telefono": telefono,
                "correo": correo,
                "fecha_de_inscripcion": fecha_inscripcion.strftime("%Y-%m-%d"),
                "estado": estado
            }
            
            if create_client(client_data):
                st.success("Cliente creado exitosamente!")
                st.experimental_rerun()

elif menu == "Buscar Clientes":
    st.header("🔍 Buscar Clientes")
    
    search_term = st.text_input("Buscar por nombre o correo")
    
    if search_term:
        db = get_db()
        results = db.query(models.Client).filter(
            (models.Client.nombres.ilike(f"%{search_term}%")) |
            (models.Client.correo.ilike(f"%{search_term}%"))
        ).all()
        
        if results:
            for client in results:
                with st.expander(f"{client.nombres} {client.apellidos}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Email:** {client.correo}")
                        st.write(f"**Teléfono:** {client.telefono}")
                        st.write(f"**Ciudad:** {client.ciudad}")
                    with col2:
                        st.write(f"**Estado:** {client.estado}")
                        st.write(f"**Plan:** {client.plan_contratado}")
                        if st.button("Eliminar", key=f"del_{client.id}"):
                            if delete_client(client.id):
                                st.success("Cliente eliminado exitosamente!")
                                st.experimental_rerun()
        else:
            st.info("No se encontraron resultados")