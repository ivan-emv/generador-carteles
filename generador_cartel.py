import streamlit as st
from docx import Document

def generar_cartel(ciudad, fecha, hora_reunion, nombre_guia, info_paseo, precio_paseo):
    doc_path = "EJEMPLO CARTEL BUDAPEST NUEVO LOGO EMV.docx"
    doc = Document(doc_path)
    
    reemplazos = {
        "Budapest": ciudad,
        "04/Mar/2025": fecha,
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
fecha = st.text_input("Ingrese la fecha (ej. 04/Mar/2025):")
hora_reunion = st.text_input("Ingrese la hora de reunión (ej. 08:45 PM):")
nombre_guia = st.text_input("Ingrese el nombre del guía:")
info_paseo = st.text_area("Ingrese la información del paseo opcional:")
precio_paseo = st.text_input("Ingrese el precio del paseo opcional:")

if st.button("Generar Cartel"):
    archivo_generado = generar_cartel(ciudad, fecha, hora_reunion, nombre_guia, info_paseo, precio_paseo)
    with open(archivo_generado, "rb") as file:
        st.download_button(label="Descargar Cartel", data=file, file_name=archivo_generado, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
