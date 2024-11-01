import streamlit as st 
import pandas as pd
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend import models
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Sistema de Gestión de Clientes", layout="wide")

# Construir la URL de conexión manualmente usando los valores de `secrets`
postgresql_info = st.secrets["connections"]["postgresql"]
DATABASE_URL = f"{postgresql_info['dialect']}://{postgresql_info['username']}:{postgresql_info['password']}@{postgresql_info['host']}:{postgresql_info['port']}/{postgresql_info['database']}"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para crear un hash de la contraseña
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Función para verificar el usuario
def check_user(username, password):
    users = {
        "admin": {"password": make_hash("admin123"), "permisionario": "per 1"},
        "user": {"password": make_hash("user123"), "permisionario": "per 2"}
    }
    if username in users and users[username]["password"] == make_hash(password):
        st.session_state['permisionario'] = users[username]["permisionario"]
        return True
    return False

# Función para crear el formulario de login
def login_form():
    with st.form("login_form"):
        st.markdown("### Inicio de Sesión")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar")
        if submit:
            if check_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

# Función de logout
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Función para conectarse a la base de datos
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def create_client(client_data):
    db = get_db()
    try:
        db_client = models.Client(**client_data)
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

def get_clients(permisionario):
    db = get_db()
    try:
        return db.query(models.Client).filter(models.Client.permisionario == permisionario).all()
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

# Función del dashboard
def dashboard(permisionario):
    st.header("Dashboard")
    clients = get_clients(permisionario)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Clientes", len(clients))
    with col2:
        activos = len([c for c in clients if c.estado == "ACTIVO"])
        st.metric("Clientes Activos", activos)
    with col3:
        inactivos = len([c for c in clients if c.estado == "INACTIVO"])
        st.metric("Clientes Inactivos", inactivos)
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

# Función para la gestión de clientes
def client_management():
    st.header("Gestión de Clientes")
    with st.form("nuevo_cliente"):
        permisionario = st.session_state.get('permisionario')
        st.text_input("Permisionario", value=permisionario, disabled=True)
        client_data = {
            "codigo": st.text_input("Código"),
            "nombres": st.text_input("Nombres"),
            "apellidos": st.text_input("Apellidos"),
            "cliente": st.text_input("Cliente"),
            "cedula_ruc": st.text_input("Cédula/RUC"),
            "servicio_contratado": st.selectbox("Servicio Contratado", ["INTERNET", "TV", "INTERNET+TV"]),
            "plan_contratado": st.text_input("Plan Contratado"),
            "provincia": st.text_input("Provincia"),
            "ciudad": st.text_input("Ciudad"),
            "direccion": st.text_input("Dirección"),
            "telefono": st.text_input("Teléfono"),
            "correo": st.text_input("Correo"),
            "fecha_de_inscripcion": st.date_input("Fecha de Inscripción").strftime("%Y-%m-%d"),
            "estado": st.selectbox("Estado", ["ACTIVO", "INACTIVO"])
        }
        if st.form_submit_button("Guardar Cliente") and create_client(client_data):
            st.success("Cliente creado exitosamente!")
            st.experimental_rerun()

def search_clients(permisionario):
    st.header("Buscar Clientes")
    search_term = st.text_input("Buscar por nombre o correo")
    if search_term:
        db = get_db()
        results = db.query(models.Client).filter(
            (models.Client.permisionario == permisionario) &
            ((models.Client.nombres.ilike(f"%{search_term}%")) |
             (models.Client.correo.ilike(f"%{search_term}%")))
        ).all()
        if results:
            for client in results:
                with st.expander(f"{client.nombres} {client.apellidos}"):
                    st.write(f"**Email:** {client.correo}")
                    st.write(f"**Teléfono:** {client.telefono}")
                    st.write(f"**Estado:** {client.estado}")
                    if st.button("Eliminar", key=f"del_{client.id}") and delete_client(client.id):
                        st.success("Cliente eliminado exitosamente!")
                        st.experimental_rerun()
        else:
            st.info("No se encontraron resultados")

# Función principal
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_form()
    else:
        permisionario = st.session_state.get('permisionario')
        st.sidebar.title("Menú")
        menu = st.sidebar.selectbox("Menú", ["Dashboard", "Gestión de Clientes", "Buscar Clientes"])
        
        if st.sidebar.button("Cerrar Sesión"):
            logout()
                    
        if menu == "Dashboard":
            dashboard(permisionario)
        elif menu == "Gestión de Clientes":
            client_management()
        elif menu == "Buscar Clientes":
            search_clients(permisionario)

if __name__ == "__main__":
    main()
