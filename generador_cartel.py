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

def generar_cartel(ciudad, fecha, actividad, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idioma1, idioma2):
    doc_path = "EJEMPLO CARTEL EMV.docx"
    doc = Document(doc_path)
    
    fecha_formateada = obtener_dia_semana(fecha, idioma1, idioma2)
    
    traducciones = {
        "Español": {"Bienvenidos": "¡Bienvenidos", "Guía": "GUÍA", "Opcional": "Paseo opcional", "NoOpcionales": "No hay Excursiones Opcionales para el Día de Hoy", "Actividad": "Actividad"},
        "Portugués": {"Bienvenidos": "Bem-Vindos", "Guía": "GUIA", "Opcional": "Passeio opcional", "NoOpcionales": "Não há passeios opcionais para hoje", "Actividad": "Atividade"},
        "Inglés": {"Bienvenidos": "Welcome", "Guía": "GUIDE", "Opcional": "Optional excursion", "NoOpcionales": "There are no optional excursions for today", "Actividad": "Activity"}
    }
    
    texto1 = traducciones[idioma1]
    texto2 = traducciones[idioma2]
    
    actividad_traducida = f"{texto1['Actividad']} / {texto2['Actividad']} - {actividad}"
    
    if not op1 and not op2:
        opcional_traducida = f"{texto1['NoOpcionales']} / {texto2['NoOpcionales']}"
        precio_op1 = ""
        precio_op2 = ""
    else:
        opcional_traducida = f"{op1} - 💰A {precio_op1} 📌Reserva con su guía. / Reserve com seu guia. / Reserve with your guide"
        if op2:
            opcional_traducida += f"\n{op2} - 💰B {precio_op2} 📌Reserva con su guía. / Reserve com seu guía. / Reserve with your guide"
    
    reemplazos = {
        "¡Bienvenidos / Welcome / Bem-Vindos": f"{texto1['Bienvenidos']} / {texto2['Bienvenidos']}",
        "(CIUDAD)": f"{ciudad}",
        "📅": f"📅 {fecha_formateada}\n{actividad_traducida}",
        "⏰": f"⏰ {hora_encuentro}",
        "📍": f"📍 {punto_encuentro}",
        "➡️": f"➡️ {desayuno}",
        "🧑‍💼": f"🧑‍💼 {texto1['Guía']} / {texto2['Guía']}: {nombre_guia}",
        "OP1 =": opcional_traducida
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
    actividad = st.text_input("Ingrese el nombre de la actividad principal:")
    hora_encuentro = st.text_input("Ingrese la hora de encuentro:")
    punto_encuentro = st.text_input("Ingrese el punto de encuentro:")
    desayuno = st.text_input("Ingrese la hora del desayuno:")
    nombre_guia = st.text_input("Ingrese el nombre del guía:")
    op1 = st.text_input("Ingrese la Excursión Opcional 1 (Opcional):")
    precio_op1 = st.text_input("Ingrese el precio de la Excursión Opcional 1 (Opcional):")
    op2 = st.text_input("Ingrese la Excursión Opcional 2 (Opcional):")
    precio_op2 = st.text_input("Ingrese el precio de la Excursión Opcional 2 (Opcional):")
    
    if st.button("Generar Cartel"):
        archivo_generado = generar_cartel(ciudad, fecha, actividad, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idiomas_seleccionados[0], idiomas_seleccionados[1])
        with open(archivo_generado, "rb") as file:
            st.download_button(label="Descargar Cartel", data=file, file_name=archivo_generado, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
