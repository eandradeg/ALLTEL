import streamlit as st
import pandas as pd
import requests

def averias_page():
    st.title("Gestión de Averías")
    
    # Formulario para nueva avería
    with st.form("nueva_averia"):
        st.subheader("Reportar Nueva Avería")
        descripcion = st.text_area("Descripción de la avería")
        submit = st.form_submit_button("Reportar")
        
        if submit:
            response = requests.post(
                "http://localhost:8000/averias/",
                json={"descripcion": descripcion, "estado": "pendiente"},
                headers={"Authorization": f"Bearer {st.session_state.get('token')}"}
            )
            if response.status_code == 200:
                st.success("Avería reportada exitosamente")
    
    # Lista de averías
    st.subheader("Averías Reportadas")
    response = requests.get("http://localhost:8000/averias/")
    if response.status_code == 200:
        averias = pd.DataFrame(response.json())
        st.dataframe(averias)