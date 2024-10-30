import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

def reportes_page():
    st.title("Reportes Mensuales")
    
    mes = st.date_input("Seleccione mes", datetime.now())
    if st.button("Generar Reporte"):
        # Aquí iría la lógica para generar el reporte
        response = requests.get(
            f"http://localhost:8000/reportes/mensual/{mes.year}/{mes.month}",
            headers={"Authorization": f"Bearer {st.session_state.get('token')}"}
        )
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            st.download_button(
                "Descargar Reporte",
                df.to_excel(),
                "reporte_mensual.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )