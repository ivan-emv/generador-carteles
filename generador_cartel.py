import streamlit as st
from fpdf import FPDF
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

def generar_cartel_pdf(ciudad, fecha, actividad, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idiomas):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_text_color(44, 66, 148)
    
    # Agregar logo si existe
    logo_path = "logo.png"  # Ruta del logo, actualizar según sea necesario
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=50)
    pdf.ln(20)
    
    pdf.set_font("Arial", style='B', size=18)
    pdf.cell(0, 10, "Generador de Carteles", ln=True, align='C')
    pdf.ln(10)
    
    fecha_formateada = obtener_dia_semana(fecha, idiomas)
    
    traducciones = {
        "Español": {"Bienvenidos": "¡Bienvenidos!", "Guía": "GUÍA", "Opcional": "Paseo opcional", "NoOpcionales": "No hay Excursiones Opcionales para el Día de Hoy", "Actividad": "Actividad", "Desayuno": "Desayuno", "Salida": "Salida"},
        "Portugués": {"Bienvenidos": "Bem-Vindos!", "Guía": "GUIA", "Opcional": "Passeio opcional", "NoOpcionales": "Não há passeios opcionais para hoje", "Actividad": "Atividade", "Desayuno": "Café da Manhã", "Salida": "Saída"},
        "Inglés": {"Bienvenidos": "Welcome!", "Guía": "GUIDE", "Opcional": "Optional excursion", "NoOpcionales": "There are no optional excursions for today", "Actividad": "Activity", "Desayuno": "Breakfast", "Salida": "Departure"}
    }
    
    textos_traducidos = [traducciones.get(idioma, traducciones["Español"]) for idioma in idiomas]
    
    bienvenida = " / ".join([texto['Bienvenidos'] for texto in textos_traducidos])
    guia_traducido = " / ".join([texto['Guía'] for texto in textos_traducidos])
    actividad_traducida = " / ".join([texto['Actividad'] for texto in textos_traducidos]) + f" - {actividad}"
    desayuno_traducido = " / ".join([texto['Desayuno'] for texto in textos_traducidos]) + f": {desayuno}"
    no_opcionales_texto = " / ".join([texto['NoOpcionales'] for texto in textos_traducidos])
    
    def safe_text(text):
        return text.encode("latin-1", "ignore").decode("latin-1")
    
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(0, 10, safe_text(bienvenida), ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(0, 10, safe_text(ciudad), ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, safe_text(f"📅 {fecha_formateada}"), ln=True)
    pdf.cell(0, 10, safe_text(f"➡️ {desayuno_traducido}"), ln=True)
    pdf.cell(0, 10, safe_text(actividad_traducida), ln=True)
    pdf.cell(0, 10, safe_text(f"⏰ {hora_encuentro}"), ln=True)
    pdf.cell(0, 10, safe_text(f"📍 {punto_encuentro}"), ln=True)
    pdf.cell(0, 10, safe_text(f"🧑‍💼 {guia_traducido}: {nombre_guia}"), ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, safe_text("✨ Paseo opcional / Passeio opcional / Optional excursion"), ln=True)
    pdf.set_font("Arial", size=12)
    
    if not op1 and not op2:
        pdf.cell(0, 10, safe_text(no_opcionales_texto), ln=True)
    else:
        if op1:
            pdf.cell(0, 10, safe_text(f"{op1} - 💰 {precio_op1}"), ln=True)
        if op2:
            pdf.cell(0, 10, safe_text(f"{op2} - 💰 {precio_op2}"), ln=True)
    
    output_path = os.path.join(os.getcwd(), f"Cartel_{ciudad}_{'_'.join(idiomas)}.pdf")
    pdf.output(output_path)
    return output_path
st.title("Generador de Carteles para Pasajeros")

idiomas_disponibles = ["Español", "Portugués", "Inglés"]
idiomas_seleccionados = st.multiselect("Seleccione los idiomas:", idiomas_disponibles, default=["Español"])

if len(idiomas_seleccionados) == 0:
    st.warning("Debe seleccionar al menos un idioma para generar el cartel.")
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
        archivo_generado = generar_cartel(ciudad, fecha, actividad, hora_encuentro, punto_encuentro, desayuno, nombre_guia, op1, precio_op1, op2, precio_op2, idiomas_seleccionados)
        if archivo_generado.startswith("Error"):
            st.error(archivo_generado)
        else:
            with open(archivo_generado, "rb") as file:
                st.download_button(label="Descargar Cartel", data=file, file_name=os.path.basename(archivo_generado), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
