import streamlit as st
from docx import Document
from datetime import datetime

def obtener_dia_semana(fecha):
    # Convertir la fecha a formato datetime
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    try:
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        return dias[fecha_dt.weekday()]
    except ValueError:
        return "Día inválido"

def generar_cartel(ciudad, fecha, hora_reunion, nombre_guia, info_paseo, precio_paseo):
    doc_path = "EJEMPLO CARTEL BUDAPEST NUEVO LOGO EMV.docx"
    doc = Document(doc_path)
    
    dia_semana = obtener_dia_semana(fecha)
    fecha_formateada = f"{dia_semana} - {fecha}"
    
    reemplazos = {
        "Budapest": ciudad,
        "Lunes / Segunda-Feira - 04/Mar/2025": fecha_formateada,
        "08:45 PM": hora_reunion,
        "Eduardo": nombre_guia,
        '"Budapest iluminado y crucero por el Danubio"': info_paseo,
        "45€": precio_paseo,
    }
    
    for p in doc.paragraphs:
        for key, value in reemplazos.items():
            if key in p.text:
                p.text = p.text.replace(key, value)
    
    output_path = f"Cartel_{ciudad}.docx"
    doc.save(output_path)
    return output_path

st.title("Generador de Carteles para Pasajeros")

ciudad = st.text_input("Ingrese la ciudad:")
fecha = st.text_input("Ingrese la fecha (dd/mm/aaaa):")
hora_reunion = st.text_input("Ingrese la hora de reunión (ej. 08:45 PM):")
nombre_guia = st.text_input("Ingrese el nombre del guía:")
info_paseo = st.text_area("Ingrese la información del paseo opcional:")
precio_paseo = st.text_input("Ingrese el precio del paseo opcional:")

if st.button("Generar Cartel"):
    archivo_generado = generar_cartel(ciudad, fecha, hora_reunion, nombre_guia, info_paseo, precio_paseo)
    with open(archivo_generado, "rb") as file:
        st.download_button(label="Descargar Cartel", data=file, file_name=archivo_generado, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
