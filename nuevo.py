import streamlit as st
import pandas as pd
import joblib

# Cargar el modelo
# Asegúrate de que 'modelo_xgboost_pipeline.pkl' esté en el mismo directorio o proporciona la ruta completa.
try:
    modelo = joblib.load('modelo_xgboost_nuevo_pipeline.pkl')
except FileNotFoundError:
    st.error("Error: El archivo 'modelo_xgboost_pipeline.pkl' no se encontró. Asegúrate de que esté en el directorio correcto.")
    st.stop()  # Detiene la ejecución si el modelo no se carga

# Diccionario completo de recodificaciones
recodificaciones = {
    "Sexo - ¿Cuál fue su sexo al nacer? (P3271)": {1: "Hombre", 2: "Mujer"},
    "Estado civil - Actualmente (P6070)": {
        "1": "No está casado(a) y vive en pareja <2 años",
        "2": "No está casado(a) y vive en pareja ≥2 años",
        "3": "Está casado(a)",
        "4": "Está separado(a) o divorciado(a)",
        "5": "Está viudo(a)",
        "6": "Está soltero(a)"
    },
    "Grupo étnico - De acuerdo con su cultura, pueblo o rasgos físicos, se reconoce como (P6080)": {
        1: "Indígena", 2: "Gitano(a)", 3: "Raizal", 4: "Palenquero(a)", 5: "Afrodescendiente", 6: "Ninguno"
    },
    "Departamento (DPTO)": {
        5: "Antioquia", 8: "Atlántico", 11: "Bogotá, D.C.", 13: "Bolívar", 15: "Boyacá", 17: "Caldas", 18: "Caquetá",
        19: "Cauca", 20: "Cesar", 23: "Córdoba", 25: "Cundinamarca", 27: "Chocó", 41: "Huila", 44: "La Guajira",
        47: "Magdalena", 50: "Meta", 52: "Nariño", 54: "Norte de Santander", 63: "Quindío", 66: "Risaralda",
        68: "Santander", 70: "Sucre", 73: "Tolima", 76: "Valle del Cauca", 86: "Putumayo", 97: "Vaupés", 94: "Guainía",
        # Nota: Guaviare está duplicado con 99 y 95, se usará el primero que aparezca.
        91: "Amazonas", 85: "Casanare", 88: "Vichada", 81: "Arauca", 99: "Guaviare", 95: "Guaviare"
    },
    "Zona urbana/rural (CLASE)": {1: "Urbano", 2: "Rural"},
    "Orientación sexual - ¿Usted siente atracción sexual o romántica por? (P3038)": {
        1: "Hombres", 2: "Mujeres", 3: "Ambos sexos", 4: "Otro"
    },
    "Nivel educativo - ¿Cuál es el mayor nivel educativo alcanzado y último grado o semestre aprobado? (P3042)": {
        1: "Ninguno", 2: "Preescolar", 3: "Primaria", 4: "Secundaria", 5: "Media académica", 6: "Media técnica",
        7: "Normalista", 8: "Técnica profesional", 9: "Tecnológica", 10: "Universitaria", 11: "Especialización",
        12: "Maestría", 13: "Doctorado", 99: "No sabe, no informa"
    },
    "Tipo de institución - La institución a la que asiste es (P3041)": {1: "Pública", 2: "Privada"},
    "Estudia actualmente - ¿Asiste a la escuela, colegio o universidad? (P6170)": {1: "Sí", 2: "No"},
    "Contrato - ¿Tiene algún tipo de contrato para este trabajo? (P6440)": {1: "Sí", 2: "No"},
    "Horas extra - ¿Recibió ingresos por horas extras el mes pasado? (P6510)": {
        1: "Sí", 2: "No", 9: "No sabe, no informa"
    },
    "Dónde trabaja - ¿Dónde realiza principalmente su trabajo? (P6880)": {
        "1": "En esta vivienda", "2": "En otras viviendas", "3": "Kiosco/caseta", "4": "Vehículo",
        "5": "De puerta en puerta", "6": "Calle (ambulante)", "7": "Local/oficina/fábrica",
        "8": "Campo/área rural/mar/río", "9": "Obra en construcción", "10": "Mina/cantera", "11": "Otro"
    },
    "Ocupación principal - En este trabajo es (P6430)": {
        "1": "Obrero empresa privada", "2": "Empleado del gobierno", "3": "Empleado doméstico",
        "4": "Cuenta propia", "5": "Patrón/empleador", "6": "Familiar sin remuneración",
        "7": "Sin remuneración en otros hogares", "8": "Jornalero/peón", "9": "Otro"
    },
    "Tipo de contrato - ¿Contrato a término indefinido o fijo? (P6460)": {
        "1": "Indefinido", "2": "Fijo", "3": "No sabe"
    },
    "Tipo de contrato - ¿Verbal o escrito? (P6450)": {
        "1": "Verbal", "2": "Escrito", "3": "No sabe"
    },
    "Afiliación salud/pensión - ¿A cuál fondo está afiliado? (P6930)": {
        "1": "Fondo privado", "2": "ISS/Cajanal", "3": "Régimen especial", "4": "Subsidiado"
    },
    "Afiliación ARP - ¿Está afiliado a aseguradora de riesgos profesionales? (P6990)": {
        1: "Sí", 2: "No", 9: "No sabe"
    },
    "Afiliación caja compensación familiar - ¿Está afiliado? (P9450)": {
        1: "Sí", 2: "No", 9: "No sabe"
    },
    "Tipo de vivienda (P4000)": {
        "1": "Casa", "2": "Apartamento", "3": "Inquilinato", "4": "Otra estructura", "5": "Vivienda indígena",
        "6": "Otra (carpa, vagón, etc.)"
    },
    "Energía eléctrica - ¿Cuenta con servicio? (P4030S1)": {1: "Sí", 2: "No"},
    "Gas natural conectado a red pública (P4030S2)": {1: "Sí", 2: "No"},
    "Alcantarillado (P4030S3)": {1: "Sí", 2: "No"},
    "Recolección de basuras (P4030S4)": {1: "Sí", 2: "No"},
    "Acueducto (P4030S5)": {1: "Sí", 2: "No"},
    "Tenencia de vivienda - ¿Cómo es la vivienda ocupada por el hogar? (P5090)": {
        "1": "Propia, pagada", "2": "Propia, pagando", "3": "Arriendo", "4": "Usufructo",
        "5": "Posesión sin título", "6": "Otra"
    },
    "Estrato socioeconómico - Estrato para tarifa (P4030S1A1)": {
        1: "Bajo - Bajo", 2: "Bajo", 3: "Medio - Bajo", 4: "Medio", 5: "Medio - Alto", 6: "Alto",
        9: "No sabe / planta eléctrica", 0: "Conexión pirata"
    },
    "Trabajo anterior - ¿Tuvo otro trabajo antes del actual? (P7020)": {1: "Sí", 2: "No"},
    "Satisfacción con trabajo actual - ¿Se siente satisfecho con su trabajo? (P7170S1)": {1: "Sí", 2: "No"},
    "Está cotizando actualmente a un fondo de pensiones? (P6920)": {
        1: "Sí", 2: "No", 3: "Pensionado"
    },
    "Sabe leer o escribir? (P6160)": {
        1: "Sí", 2: "No"
    },
    # Nuevo campo para la rama de actividad
    "Rama de actividad (2 dígitos) - Actividad principal de la empresa o negocio (RAMA2D_R4)": [
        61.0, 46.0, 62.0, 10.0, 56.0, 47.0, 41.0, 86.0, 97.0, 1.0, 84.0, 68.0, 74.0, 75.0, 49.0, 85.0, 59.0, 20.0, 55.0,
        64.0, 3.0, 96.0, 45.0, 14.0, 15.0, 31.0, 82.0, 87.0, 88.0, 94.0, 50.0, 71.0, 42.0, 9.0, 23.0, 8.0, 35.0, 52.0,
        80.0, 16.0, 22.0, 92.0, 27.0, 65.0, 5.0, 25.0, 63.0, 29.0, 11.0, 73.0, 69.0, 32.0, 77.0, 95.0, 81.0, 43.0, 58.0,
        93.0, 21.0, 33.0, 36.0, 38.0, 53.0, 24.0, 78.0, 66.0, 90.0, 28.0, 99.0, 18.0, 13.0, 7.0, 2.0, 6.0, 60.0, 79.0,
        17.0, 30.0, 70.0, 72.0, 0.0, 51.0, 91.0, 39.0, 19.0, 26.0, 12.0, 37.0
    ]
}

st.set_page_config(page_title="Predicción de calidad salarial", page_icon="💰")
st.title("💰 Predicción de calidad salarial")

# Diccionario para almacenar las entradas del usuario
user_inputs = {}

# Helper para obtener el valor original de la recodificación


def get_original_value(category_key, selected_label):
    # Invertir el diccionario de recodificación para buscar el valor original
    # Asegurarse de que el valor sea un diccionario antes de intentar invertirlo
    if isinstance(recodificaciones[category_key], dict):
        reverse_map = {v: k for k, v in recodificaciones[category_key].items()}
        return reverse_map.get(selected_label)
    else:
        # Si no es un diccionario (ej. lista de valores numéricos), el valor seleccionado ya es el original
        return selected_label


# Sección de Datos Personales
st.header("Datos Personales")
user_inputs["Sexo - ¿Cuál fue su sexo al nacer? (P3271)"] = st.selectbox(
    "Sexo", options=list(recodificaciones["Sexo - ¿Cuál fue su sexo al nacer? (P3271)"].values())
)
# Se actualiza el nombre de la columna para 'Edad'
user_inputs["Edad - ¿Cuántos años cumplidos tiene...? (si es menor de 1 año, escriba 00) (P6040)"] = st.number_input(
    "Edad", min_value=0, max_value=120, value=30)

user_inputs["Grupo étnico - De acuerdo con su cultura, pueblo o rasgos físicos, se reconoce como (P6080)"] = st.selectbox(
    "Grupo étnico", options=list(recodificaciones["Grupo étnico - De acuerdo con su cultura, pueblo o rasgos físicos, se reconoce como (P6080)"].values())
)
user_inputs["Nivel educativo - ¿Cuál es el mayor nivel educativo alcanzado y último grado o semestre aprobado? (P3042)"] = st.selectbox(
    "Nivel educativo", options=list(recodificaciones["Nivel educativo - ¿Cuál es el mayor nivel educativo alcanzado y último grado o semestre aprobado? (P3042)"].values())
)


# Sección de Información Laboral
st.header("Información Laboral")
# Se actualiza el nombre de la columna para 'Número de horas trabajadas'
user_inputs["Número de horas trabajadas - ¿Cuántas horas trabajó la semana pasada? (P6850)"] = st.number_input(
    "Número de horas trabajadas", min_value=0, max_value=168, value=40
)

user_inputs["Dónde trabaja - ¿Dónde realiza principalmente su trabajo? (P6880)"] = st.selectbox(
    "¿Dónde trabaja?", options=list(recodificaciones["Dónde trabaja - ¿Dónde realiza principalmente su trabajo? (P6880)"].values())
)
user_inputs["Afiliación caja compensación familiar - ¿Está afiliado? (P9450)"] = st.selectbox(
    "¿Afiliado a caja de compensación familiar?", options=list(recodificaciones["Afiliación caja compensación familiar - ¿Está afiliado? (P9450)"].values())
)
# Sección de Vivienda y Servicios
st.header("Vivienda y Servicios")


# Botón para predecir
if st.button("Predecir"):
    # Preparar los datos de entrada para el modelo
    # Se crea un diccionario para la entrada del modelo, mapeando los valores seleccionados
    # por el usuario a sus códigos originales usando el diccionario de recodificaciones.
    model_input_data = {}
    for key, selected_value in user_inputs.items():
        if key in recodificaciones and isinstance(recodificaciones[key], dict):
            # Encontrar el código original para la opción seleccionada si es un diccionario de recodificaciones
            original_code = get_original_value(key, selected_value)
            model_input_data[key] = [original_code]
        else:
            # Para campos numéricos o listas de valores que no necesitan recodificación (como RAMA2D_R4)
            model_input_data[key] = [selected_value]

    # Crear DataFrame con la entrada del usuario para la predicción
    entrada_df = pd.DataFrame(model_input_data)

    # Realizar la predicción
    try:
        prediccion = modelo.predict(entrada_df)[0]
        st.success(f"El Ingreso laboral mensual predicho es de: ${prediccion} COP")
    except Exception as e:
        st.error(f"Error al realizar la predicción: {e}")
        st.warning(
            "Asegúrate de que todas las columnas de entrada coincidan con las esperadas por el modelo.")

    # Mostrar los datos de entrada como resumen
    with st.expander("Ver datos de entrada para el modelo"):
        st.write(entrada_df)

st.caption("Desarrollado por tu equipo 🚀")
