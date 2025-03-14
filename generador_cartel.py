import streamlit as st
from docx import Document
from datetime import datetime

def obtener_dia_semana(fecha):
    dias = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
    dias_pt = {"Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira", "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"}
    dias_en = {"Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday", "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday", "Sunday": "Sunday"}
    try:
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        dia_semana = fecha_dt.strftime("%A")
        return dias[dia_semana], dias_pt[dia_semana], dias_en[dia_semana]
    except ValueError:
        return "Día inválido", "Dia inválido", "Invalid day"

def generar_cartel(idiomas, ciudad, fecha, hora_reunion, punto_encuentro, desayuno, nombre_guia, opcional1, precio1, opcional2, precio2):
    doc_path = "EJEMPLO CARTEL EMV.docx"
    doc = Document(doc_path)
    
    dia_es, dia_pt, dia_en = obtener_dia_semana(fecha)
    fecha_es = f"{dia_es} {fecha}"
    fecha_pt = f"{dia_pt} {fecha}"
    fecha_en = f"{dia_en} {fecha}"
    
    textos = {
        "Español": {"bienvenida": "¡Bienvenidos", "guia": "GUÍA"},
        "Portugués": {"bienvenida": "Bem-Vindos", "guia": "GUIA"},
        "Inglés": {"bienvenida": "Welcome", "guia": "GUIDE"},
    }
    
    idioma1, idioma2 = idiomas[0], idiomas[1] if len(idiomas) > 1 else idiomas[0]
    texto1, texto2 = textos[idioma1], textos[idioma2]
    
    reemplazos = {
        "¡Bienvenidos / Welcome / Bem-Vindos": f"{texto1['bienvenida']} / {texto2['bienvenida']}",
        "(CIUDAD)": f"{ciudad} / {ciudad}",
        "📅": f"📅 {fecha_es} / {fecha_pt} / {fecha_en}",
        "⏰": f"⏰ {hora_reunion}",
        "📍": f"📍 {punto_encuentro}",
        "➡️": f"➡️ {desayuno}",
        "🧑‍💼": f"🧑‍💼 {texto1['guia']} / {texto2['guia']}: {nombre_guia}",
        "OP1 =": f"{opcional1}",
        "💰A 45€": f"💰A {precio1}",
        "OP2=": f"{opcional2}" if opcional2 else "",
        "💰B 45€": f"💰B {precio2}" if opcional2 else "",
    }
    
    for p in doc.paragraphs:
        for key, value in reemplazos.items():
            if key in p.text:
                p.text = p.text.replace(key, value)
    
    output_path = f"Cartel_{ciudad}_{idioma1}_{idioma2}.docx"
    doc.save(output_path)
    return output_path

st.title("Generador de Carteles para Pasajeros")
idiomas_disponibles = ["Español", "Portugués", "Inglés"]
idiomas_seleccionados = st.multiselect("Seleccione hasta 2 idiomas:", idiomas_disponibles, default=["Español"], max_selections=2)
ciudad = st.text_input("Ingrese la ciudad:")
fecha = st.text_input("Ingrese la fecha (dd/mm/aaaa):")
hora_reunion = st.text_input("Ingrese la hora de reunión (ej. 08:45 PM):")
punto_encuentro = st.text_input("Ingrese el punto de encuentro:")
desayuno = st.text_input("Ingrese la hora del desayuno:")
nombre_guia = st.text_input("Ingrese el nombre del guía:")
opcional1 = st.text_input("Ingrese la primera excursión opcional:")
precio1 = st.text_input("Ingrese el precio de la primera excursión opcional:")
opcional2 = st.text_input("Ingrese la segunda excursión opcional (opcional):")
precio2 = st.text_input("Ingrese el precio de la segunda excursión opcional (opcional):")

if st.button("Generar Cartel"):
    archivo_generado = generar_cartel(idiomas_seleccionados, ciudad, fecha, hora_reunion, punto_encuentro, desayuno, nombre_guia, opcional1, precio1, opcional2, precio2)
    with open(archivo_generado, "rb") as file:
        st.download_button(label="Descargar Cartel", data=file, file_name=archivo_generado, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
