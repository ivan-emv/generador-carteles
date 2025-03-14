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
        return f"{' / '.join([dias[idioma][fecha_dt.weekday()] for idioma in idiomas])} - {fecha}"
    except ValueError:
        return "Día inválido"

def generar_cartel(ciudad, fecha, actividad, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idiomas):
    try:
        st.write("Iniciando procesamiento del cartel...")
        doc = Document("EJEMPLO CARTEL EMV.docx")
        
        traducciones = {
            "Español": {"Bienvenidos": "¡Bienvenidos", "Guía": "GUÍA", "Opcional": "Paseo opcional", "NoOpcionales": "No hay Excursiones Opcionales para el Día de Hoy", "Actividad": "Actividad", "Desayuno": "Desayuno", "Prevision": "Por favor, preséntense 10-15 min antes."},
            "Portugués": {"Bienvenidos": "Bem-Vindos", "Guía": "GUIA", "Opcional": "Passeio opcional", "NoOpcionales": "Não há passeios opcionais para hoje", "Actividad": "Atividade", "Desayuno": "Café da Manhã", "Prevision": "Por favor, apresentem-se 10-15 min antes."},
            "Inglés": {"Bienvenidos": "Welcome", "Guía": "GUIDE", "Opcional": "Optional excursion", "NoOpcionales": "There are no optional excursions for today", "Actividad": "Activity", "Desayuno": "Breakfast", "Prevision": "Please, be at least 10-15 min. In Advance."}
        }
        
        textos_traducidos = [traducciones[idioma] for idioma in idiomas]
        
        reemplazos = {
            "(BIENVENIDA)": " / ".join([t['Bienvenidos'] for t in textos_traducidos]),
            "(CIUDAD)": ciudad,
            "📅": f"📅 {obtener_dia_semana(fecha, idiomas)}\n➡️ {' / '.join([t['Desayuno'] for t in textos_traducidos])}: {desayuno}\n{' / '.join([t['Actividad'] for t in textos_traducidos])} - {actividad}",
            "⏰": f"⏰ {hora_encuentro}",
            "📍": f"📍 {punto_encuentro}",
            "🧑‍💼": f"🧑‍💼 {' / '.join([t['Guía'] for t in textos_traducidos])}: {nombre_guia}",
            "(PREVISION1)": " / ".join([t['Prevision'] for t in textos_traducidos]),
            "(PREVISION2)": " / ".join([t['Prevision'] for t in textos_traducidos]),
            "✨ Paseo opcional / Passeio opcional / Optional excursion": f"✨ Paseo opcional / Passeio opcional / Optional excursion\n{op1 if op1 else ''}{'\n💰A ' + precio_op1 if op1 else ''}{'\n' + op2 if op2 else ''}{'\n💰B ' + precio_op2 if op2 else ''}" if op1 or op2 else "✨ Paseo opcional / Passeio opcional / Optional excursion\n" + textos_traducidos[0]['NoOpcionales']
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
        st.write("Cartel generado exitosamente.")
        return output_path
    except Exception as e:
        st.error(f"Error al generar el cartel: {str(e)}")
        return None

st.title("Generador de Carteles para Pasajeros")
