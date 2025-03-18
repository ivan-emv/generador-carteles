import streamlit as st
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime
import os

def obtener_dia_semana(fecha, idiomas):
    dias = {
        "Español": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        "Portugués": ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo"],
        "Inglés": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }
    try:
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        dias_traducidos = [dias.get(idioma, dias["Español"])[fecha_dt.weekday()] for idioma in idiomas]
        return f"{' / '.join(dias_traducidos)} - {fecha}"
    except ValueError:
        return "Día inválido"

def generar_cartel(ciudad, fecha, actividad, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idiomas):
    doc_path = "EJEMPLO CARTEL EMV.docx"
    if not os.path.exists(doc_path):
        return "Error: No se encuentra el archivo base. Asegúrate de que 'EJEMPLO CARTEL EMV.docx' está en el directorio."
    
    doc = Document(doc_path)
    fecha_formateada = obtener_dia_semana(fecha, idiomas)
    
    reemplazos = {
        "(BIENVENIDA)": " / ".join(["¡Bienvenidos!" if idioma == "Español" else "Bem-Vindos!" if idioma == "Portugués" else "Welcome!" for idioma in idiomas]),
        "(CIUDAD)": ciudad,
        "📅": f"📅 {fecha_formateada}\n➡️ Desayuno: {desayuno}\n{actividad}",
        "⏰": f"⏰ {hora_encuentro}",
        "📍": f"📍 Punto de Encuentro: {punto_encuentro}",
        "🧑‍💼": f"🧑‍💼 GUÍA: {nombre_guia}"
    }
    
    for p in doc.paragraphs:
        for key, value in reemplazos.items():
            if key in p.text:
                p.text = p.text.replace(key, value)
    
    output_path = f"Cartel_{ciudad}_{'_'.join(idiomas)}.docx"
    doc.save(output_path)
    return output_path

st.title("Generador de Carteles para Pasajeros")

idiomas_disponibles = ["Español", "Portugués", "Inglés"]
idiomas_seleccionados = st.multiselect("Seleccione los idiomas:", idiomas_disponibles, default=["Español"])

if len(idiomas_seleccionados) == 0:
    st.warning("Debe seleccionar al menos un idioma para generar el cartel.")
else:
    ciudad = st.text_input("Ingrese la ciudad:")
    fecha = st.text_input("Ingrese la fecha (dd/mm/aaaa):")
    actividad = st.text_input("Ingrese la actividad principal:")
    hora_encuentro = st.text_input("Ingrese la hora de encuentro:")
    punto_encuentro = st.text_input("Ingrese el punto de encuentro:")
    desayuno = st.text_input("Ingrese la hora del desayuno:")
    nombre_guia = st.text_input("Ingrese el nombre del guía:")
    op1 = st.text_input("Excursión Opcional 1 (Opcional):")
    precio_op1 = st.text_input("Precio Excursión Opcional 1 (Opcional):")
    op2 = st.text_input("Excursión Opcional 2 (Opcional):")
    precio_op2 = st.text_input("Precio Excursión Opcional 2 (Opcional):")
    
    if st.button("Generar Cartel"):
        archivo_generado = generar_cartel(ciudad, fecha, actividad, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idiomas_seleccionados)
        if archivo_generado.startswith("Error"):
            st.error(archivo_generado)
        else:
            with open(archivo_generado, "rb") as file:
                st.download_button(label="Descargar Cartel", data=file, file_name=os.path.basename(archivo_generado), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
