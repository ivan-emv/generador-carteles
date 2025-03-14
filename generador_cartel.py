import streamlit as st
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime

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
    doc = Document(doc_path)
    
    fecha_formateada = obtener_dia_semana(fecha, idiomas)
    
    traducciones = {
        "Español": {"Bienvenidos": "¡Bienvenidos!", "Guía": "GUÍA", "Opcional": "Paseo opcional", "NoOpcionales": "No hay Excursiones Opcionales para el Día de Hoy", "Actividad": "Actividad", "Desayuno": "Desayuno"},
        "Portugués": {"Bienvenidos": "Bem-Vindos!", "Guía": "GUIA", "Opcional": "Passeio opcional", "NoOpcionales": "Não há passeios opcionais para hoje", "Actividad": "Atividade", "Desayuno": "Café da Manhã"},
        "Inglés": {"Bienvenidos": "Welcome!", "Guía": "GUIDE", "Opcional": "Optional excursion", "NoOpcionales": "There are no optional excursions for today", "Actividad": "Activity", "Desayuno": "Breakfast"}
    }
    
    textos_traducidos = [traducciones.get(idioma, traducciones["Español"]) for idioma in idiomas]
    
    bienvenida = " / ".join([texto['Bienvenidos'] for texto in textos_traducidos])
    guia_traducido = " / ".join([texto['Guía'] for texto in textos_traducidos])
    actividad_traducida = " / ".join([texto['Actividad'] for texto in textos_traducidos]) + f" - {actividad}"
    desayuno_traducido = " / ".join([texto['Desayuno'] for texto in textos_traducidos]) + f": {desayuno}"
    
    opcionales_texto = "✨ Paseo opcional / Passeio opcional / Optional excursion"
    if not op1 and not op2:
        opcionales_texto += f"\n{' / '.join([texto['NoOpcionales'] for texto in textos_traducidos])}"
    else:
        if op1:
            opcionales_texto += f"\n{op1}\n💰 {precio_op1}"
        if op2:
            opcionales_texto += f"\n{op2}\n💰 {precio_op2}"
    
    reemplazos = {
        "(BIENVENIDA)": bienvenida,
        "(CIUDAD)": f"{ciudad}",
        "📅": f"📅 {fecha_formateada}\n➡️ {desayuno_traducido}\n{actividad_traducida}",
        "⏰": f"⏰ {hora_encuentro}",
        "📍": f"📍 {punto_encuentro}",
        "🧑‍💼": f"🧑‍💼 {guia_traducido}: {nombre_guia}",
        "✨ Paseo opcional / Passeio opcional / Optional excursion": opcionales_texto
    }
    
    for p in doc.paragraphs:
        for key, value in reemplazos.items():
            if key in p.text:
                p.text = p.text.replace(key, value)
                for run in p.runs:
                    if key in ["(BIENVENIDA)", "(CIUDAD)"]:
                        run.font.name = "Neulis Sans Black"
                        run.font.size = Pt(18)
                        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    elif key == "📅":
                        run.font.name = "Neulis Sans Black"
                        run.font.size = Pt(14)
                        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
                    else:
                        run.font.name = "Neulis Sans"
                        run.font.size = Pt(14)
                        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    
    output_path = f"Cartel_{ciudad}_{'_'.join(idiomas)}.docx"
    doc.save(output_path)
    return output_path

st.title("Generador de Carteles para Pasajeros")
