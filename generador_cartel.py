import streamlit as st
from docx import Document
from datetime import datetime

def obtener_dia_semana(fecha):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    try:
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        return dias[fecha_dt.weekday()]
    except ValueError:
        return "Día inválido"

def generar_cartel(ciudad, fecha, hora_reunion, nombre_guia, info_paseo, precio_paseo, idiomas):
    doc_path = "EJEMPLO CARTEL BUDAPEST NUEVO LOGO EMV.docx"
    doc = Document(doc_path)
    
    dia_semana = obtener_dia_semana(fecha)
    fecha_formateada = f"{dia_semana} - {fecha}"
    
    traducciones = {
        "Español": {
            "Bienvenidos": "¡Bienvenidos a",
            "Reunión de Bienvenida": "REUNIÓN DE BIENVENIDA",
            "Guía": "Guía",
            "Excursión Opcional": "Paseo opcional",
            "Emergencia 24h": "Emergencia 24 horas",
        },
        "Portugués": {
            "Bienvenidos": "Bem-Vindos a",
            "Reunión de Bienvenida": "REUNIÃO DE BOAS-VINDAS",
            "Guía": "Guia",
            "Excursión Opcional": "Passeio opcional",
            "Emergencia 24h": "Emergência 24 horas",
        },
        "Inglés": {
            "Bienvenidos": "Welcome to",
            "Reunión de Bienvenida": "WELCOME MEETING",
            "Guía": "Guide",
            "Excursión Opcional": "Optional Tour",
            "Emergencia 24h": "24h Emergency",
        }
    }
    
    textos_traducidos = [traducciones[idioma] for idioma in idiomas if idioma in traducciones]
    if not textos_traducidos:
        textos_traducidos = [traducciones["Español"]]
    
    texto1 = textos_traducidos[0]
    texto2 = textos_traducidos[1] if len(textos_traducidos) > 1 else texto1
    
    reemplazos = {
        "Budapest": ciudad,
        "Lunes / Segunda-Feira - 04/Mar/2025": fecha_formateada,
        "08:45 PM": hora_reunion,
        "Eduardo": nombre_guia,
        '"Budapest iluminado y crucero por el Danubio"': info_paseo,
        "45€": precio_paseo,
        "¡Bienvenidos A": f"{texto1['Bienvenidos']} {ciudad}! / {texto2['Bienvenidos']} {ciudad}!",
        "REUNIÓN DE BIENVENIDA": f"{texto1['Reunión de Bienvenida']} / {texto2['Reunión de Bienvenida']}",
        "Guía": f"{texto1['Guía']} / {texto2['Guía']}",
        "Paseo opcional": f"{texto1['Excursión Opcional']} / {texto2['Excursión Opcional']}",
        "Emergencia 24 horas": f"{texto1['Emergencia 24h']} / {texto2['Emergencia 24h']}",
    }
    
    for p in doc.paragraphs:
        for key, value in reemplazos.items():
            if key in p.text:
                p.text = p.text.replace(key, value)
    
    output_path = f"Cartel_{ciudad}_{idiomas[0]}_{idiomas[1]}.docx"
    doc.save(output_path)
    return output_path

st.title("Generador de Carteles para Pasajeros")

idiomas_disponibles = ["Español", "Portugués", "Inglés"]
idiomas_seleccionados = st.multiselect("Seleccione hasta 2 idiomas:", idiomas_disponibles, default=["Español"], max_selections=2)

ciudad = st.text_input("Ingrese la ciudad:")
fecha = st.text_input("Ingrese la fecha (dd/mm/aaaa):")
hora_reunion = st.text_input("Ingrese la hora de reunión (ej. 08:45 PM):")
nombre_guia = st.text_input("Ingrese el nombre del guía:")
info_paseo = st.text_area("Ingrese la información del paseo opcional:")
precio_paseo = st.text_input("Ingrese el precio del paseo opcional:")

if st.button("Generar Cartel"):
    archivo_generado = generar_cartel(ciudad, fecha, hora_reunion, nombre_guia, info_paseo, precio_paseo, idiomas_seleccionados)
    with open(archivo_generado, "rb") as file:
        st.download_button(label="Descargar Cartel", data=file, file_name=archivo_generado, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
