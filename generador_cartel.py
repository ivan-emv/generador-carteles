import streamlit as st
from docx import Document
from datetime import datetime

def obtener_dia_semana(fecha, idioma1, idioma2):
    dias = {
        "Español": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        "Portugués": ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo"],
        "Inglés": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }
    try:
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        return f"{dias[idioma1][fecha_dt.weekday()]} / {dias[idioma2][fecha_dt.weekday()]} - {fecha}"
    except ValueError:
        return "Día inválido"

def generar_cartel(ciudad, fecha, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idioma1, idioma2):
    doc_path = "EJEMPLO CARTEL EMV.docx"
    doc = Document(doc_path)
    
    fecha_formateada = obtener_dia_semana(fecha, idioma1, idioma2)
    
    traducciones = {
        "Español": {"Bienvenidos": "¡Bienvenidos", "Guía": "GUÍA", "Opcional": "Paseo opcional"},
        "Portugués": {"Bienvenidos": "Bem-Vindos", "Guía": "GUIA", "Opcional": "Passeio opcional"},
        "Inglés": {"Bienvenidos": "Welcome", "Guía": "GUIDE", "Opcional": "Optional excursion"}
    }
    
    texto1 = traducciones[idioma1]
    texto2 = traducciones[idioma2]
    
    reemplazos = {
        "¡Bienvenidos / Welcome / Bem-Vindos": f"{texto1['Bienvenidos']} / {texto2['Bienvenidos']}",
        "(CIUDAD)": f"{ciudad}",
        "📅": f"📅 {fecha_formateada}",
        "⏰": f"⏰ {hora_encuentro}",
        "📍": f"📍 {punto_encuentro}",
        "➡️": f"➡️ {desayuno}",
        "🧑‍💼": f"🧑‍💼 {texto1['Guía']} / {texto2['Guía']}: {nombre_guia}",
        "OP1 =": f"{op1}",
        "💰A 45€": f"💰A {precio_op1}",
        "OP2=": f"{op2}" if op2 else "", 
        "💰B 45€": f"💰B {precio_op2}" if precio_op2 else ""
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
idiomas_seleccionados = st.multiselect("Seleccione hasta 2 idiomas:", idiomas_disponibles, default=["Español", "Inglés"], max_selections=2)

if len(idiomas_seleccionados) < 2:
    st.warning("Debe seleccionar dos idiomas para generar el cartel.")
else:
    ciudad = st.text_input("Ingrese la ciudad:")
    fecha = st.text_input("Ingrese la fecha (dd/mm/aaaa):")
    hora_encuentro = st.text_input("Ingrese la hora de encuentro:")
    punto_encuentro = st.text_input("Ingrese el punto de encuentro:")
    desayuno = st.text_input("Ingrese la hora del desayuno:")
    nombre_guia = st.text_input("Ingrese el nombre del guía:")
    op1 = st.text_input("Ingrese la Excursión Opcional 1:")
    precio_op1 = st.text_input("Ingrese el precio de la Excursión Opcional 1:")
    op2 = st.text_input("Ingrese la Excursión Opcional 2 (Opcional):")
    precio_op2 = st.text_input("Ingrese el precio de la Excursión Opcional 2 (Opcional):")
    
    if st.button("Generar Cartel"):
        archivo_generado = generar_cartel(ciudad, fecha, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idiomas_seleccionados[0], idiomas_seleccionados[1])
        with open(archivo_generado, "rb") as file:
            st.download_button(label="Descargar Cartel", data=file, file_name=archivo_generado, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
