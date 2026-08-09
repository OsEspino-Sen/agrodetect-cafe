import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io
from datetime import datetime
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def mostrar_html(contenido):
    st.html(contenido)


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="AgroDetect Café | Oscar Espino | 202310110465",
    page_icon="🌿",
    layout="wide",
)

# ============================================================
# ESTILOS
# ============================================================

mostrar_html(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,600;0,700;0,900;1,500;1,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

/* ---------- FONDO GENERAL ---------- */

.stApp {
    background: #F4F0E6;
}

.block-container {
    max-width: 1520px;
    padding: 4.2rem 2rem 2.2rem;
}

/* ---------- ENCABEZADO ---------- */

.pl-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    flex-wrap: wrap;
    box-sizing: border-box;
    width: 100%;
    position: relative;
    z-index: 1;
    background: linear-gradient(120deg, #1B3B28, #2F6B45 75%);
    border-radius: 20px;
    padding: 16px 24px;
    margin-bottom: 22px;
    box-shadow: 0 16px 36px -22px rgba(27, 59, 40, 0.65);
}

.pl-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.pl-logo {
    width: 50px;
    height: 50px;
    flex: none;
    display: grid;
    place-items: center;
    font-size: 26px;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 14px;
}

.pl-brand-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 9.5px;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #C9E2BC;
    margin-bottom: 3px;
}

.pl-brand-title {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 900;
    font-size: 24px;
    line-height: 1.05;
    color: #FFFDF7;
}

.pl-brand-title em {
    font-style: italic;
    font-weight: 600;
    color: #F0C567;
}

.pl-top-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.pl-chip {
    font-family: 'Inter', sans-serif;
    font-size: 11.5px;
    font-weight: 500;
    color: rgba(255, 253, 247, 0.85);
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 999px;
    padding: 6px 13px;
    white-space: nowrap;
}

.pl-chip strong {
    color: #F0C567;
    font-weight: 600;
}

/* ---------- PANELES ---------- */

.pl-panel {
    background: #FFFFFF;
    border: 1px solid #E6DCC9;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 12px 30px -24px rgba(27, 59, 40, 0.4);
}

.pl-eyebrow {
    display: flex;
    align-items: center;
    gap: 9px;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4C7A5C;
    margin-bottom: 7px;
}

.pl-eyebrow::before {
    content: "";
    width: 22px;
    height: 3px;
    border-radius: 3px;
    background: #E3A93C;
}

.pl-title-lg {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 700;
    font-size: 22px;
    color: #26201A;
    margin-bottom: 6px;
}

.pl-body {
    font-family: 'Inter', sans-serif;
    font-size: 13.5px;
    line-height: 1.65;
    color: #7A7164;
    margin-bottom: 14px;
}

/* ---------- UPLOADER ---------- */

[data-testid="stFileUploader"] {
    background: #FAF7EF;
    border: 2px dashed #C9BCA3;
    border-radius: 14px;
    padding: 8px 12px;
    transition: border-color 0.2s ease, background 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #4C8A5C;
    background: #F7F3E8;
}

[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
    min-height: 64px !important;
}

[data-testid="stFileUploader"] [data-testid="stFileUploaderSection"] {
    text-align: center;
}

/* ---------- PASOS ---------- */

.pl-steps {
    margin-top: 16px;
    border-top: 1px dashed #E0D5C0;
    padding-top: 14px;
}

.pl-step {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Inter', sans-serif;
    font-size: 12.5px;
    color: #6E6557;
    padding: 4px 0;
}

.pl-step b {
    display: inline-grid;
    place-items: center;
    width: 22px;
    height: 22px;
    flex: none;
    font-size: 10.5px;
    font-weight: 700;
    color: #2F6B45;
    background: #EAF2E6;
    border-radius: 7px;
}

/* ---------- IMAGEN ---------- */

.pl-imagen {
    margin-top: 14px;
}

[data-testid="stImage"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #E6DCC9;
    box-shadow: 0 12px 26px -18px rgba(27, 59, 40, 0.4);
}

[data-testid="stImage"] img {
    max-height: 200px;
    width: 100%;
    object-fit: contain;
}

/* ---------- BOTÓN ---------- */

.stButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
    color: #FFFFFF !important;
    background: linear-gradient(135deg, #2F6B45, #3E8A58) !important;
    border: none !important;
    border-radius: 14px !important;
    min-height: 50px;
    box-shadow: 0 12px 24px -12px rgba(47, 107, 69, 0.75);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 16px 30px -12px rgba(47, 107, 69, 0.85);
}

.stDownloadButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    color: #2F6B45 !important;
    background: #FFFFFF !important;
    border: 1.5px solid #B9CFAE !important;
    border-radius: 14px !important;
    min-height: 50px;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.stDownloadButton > button:hover {
    background: #EFF6EA !important;
    border-color: #2F6B45 !important;
}

.stButton > button:focus-visible,
.stDownloadButton > button:focus-visible {
    outline: 3px solid #E3A93C;
    outline-offset: 2px;
}

/* ---------- ESTADÍSTICAS ---------- */

.pl-stats {
    display: flex;
    gap: 10px;
    margin-top: 18px;
}

.pl-stat {
    flex: 1 1 0;
    min-width: 0;
    background: #F7F3EA;
    border: 1px solid #E6DCC9;
    border-radius: 14px;
    padding: 12px 16px;
}

.pl-stat b {
    display: block;
    font-family: 'Fraunces', Georgia, serif;
    font-size: 15px;
    font-weight: 700;
    color: #26201A;
    white-space: nowrap;
}

.pl-stat span {
    display: block;
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9A8F7D;
    margin-top: 3px;
    white-space: nowrap;
}

/* ---------- CABECERA DE RESULTADO ---------- */

.pl-result-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    margin: 18px 0 14px;
}

.pl-result-head .pl-eyebrow {
    margin-bottom: 0;
}

.pl-chip-claro {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: #2F6B45;
    background: #EAF2E6;
    border: 1px solid #CFE0C8;
    border-radius: 999px;
    padding: 5px 12px;
    white-space: nowrap;
}

/* ---------- DIAGNÓSTICO ---------- */

.pl-dx {
    display: flex;
    align-items: center;
    gap: 22px;
    background: linear-gradient(135deg, #EAF2E6, #FFFFFF 65%);
    border: 1px solid #CFE0C8;
    border-radius: 18px;
    padding: 18px 22px;
}

.pl-dx-info {
    flex: 1;
    min-width: 0;
}

.pl-dx-label {
    font-family: 'Inter', sans-serif;
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5E8066;
    margin-bottom: 5px;
}

.pl-dx-nombre {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 700;
    font-size: 25px;
    line-height: 1.15;
    color: #26201A;
    margin-bottom: 5px;
    word-break: break-word;
}

.pl-dx-sub {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: #8A8071;
}

/* ---------- ANILLO DE CONFIANZA ---------- */

.pl-ring {
    position: relative;
    width: 116px;
    height: 116px;
    flex: none;
    display: grid;
    place-items: center;
    border-radius: 50%;
    box-shadow: 0 10px 24px -12px rgba(47, 107, 69, 0.5);
}

.pl-ring-core {
    position: relative;
    width: 88px;
    height: 88px;
    border-radius: 50%;
    background: #FFFFFF;
    display: grid;
    place-items: center;
    box-shadow: inset 0 2px 8px rgba(38, 32, 26, 0.08);
}

.pl-ring-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 21px;
    font-weight: 600;
    color: #26201A;
    line-height: 1;
    text-align: center;
}

.pl-ring-label {
    font-family: 'Inter', sans-serif;
    font-size: 8px;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: #8A8071;
    text-align: center;
    margin-top: 3px;
}

/* ---------- SECCIÓN ---------- */

.pl-section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 700;
    font-size: 19px;
    color: #26201A;
    margin: 24px 0 14px;
}

.pl-section-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #D8CCB4, transparent);
}

/* ---------- RECOMENDACIONES ---------- */

.pl-reco-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 12px;
}

.pl-reco-grid .pl-reco {
    margin-bottom: 0;
    align-self: stretch;
}

.pl-reco-grid .pl-reco:nth-child(-n+3) {
    grid-column: span 2;
}

.pl-reco-grid .pl-reco:nth-child(n+4) {
    grid-column: span 3;
}

.pl-reco {
    background: #FFFFFF;
    border: 1px solid #E6DCC9;
    border-radius: 16px;
    padding: 16px 18px 17px;
    box-shadow: 0 6px 18px -16px rgba(27, 59, 40, 0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.pl-reco:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 24px -16px rgba(27, 59, 40, 0.45);
}

.pl-reco-top {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 9px;
}

.pl-reco-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    flex: none;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    color: #F2F9EE;
    background: #2F6B45;
    border-radius: 9px;
}

.pl-reco-titulo {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #2C4A35;
    line-height: 1.35;
    padding-top: 3px;
}

.pl-reco-texto {
    font-family: 'Inter', sans-serif;
    font-size: 12.5px;
    line-height: 1.6;
    color: #6E6557;
    text-align: justify;
    hyphens: auto;
}

/* ---------- ESTADO VACÍO ---------- */

.pl-empty {
    background: #FFFFFF;
    border: 1.5px dashed #C9BCA3;
    border-radius: 18px;
    text-align: center;
    padding: 42px 20px;
    color: #7A7164;
}

.pl-empty-icono {
    display: grid;
    place-items: center;
    width: 58px;
    height: 58px;
    margin: 0 auto 12px;
    font-size: 28px;
    background: #F7F3EA;
    border-radius: 18px;
}

.pl-empty-titulo {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 18px;
    font-weight: 700;
    color: #26201A;
    margin-bottom: 6px;
}

.pl-empty-texto {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    line-height: 1.6;
    max-width: 280px;
    margin: 0 auto;
}

/* ---------- PIE ---------- */

.pl-footer {
    text-align: center;
    max-width: 720px;
    margin: 28px auto 0;
    padding: 22px 16px 8px;
    border-top: 1px dashed #D8CCB4;
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    line-height: 1.9;
    color: #9A8F7D;
}

.pl-footer-brand {
    display: block;
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: 0.14em;
    color: #2F6B45;
    margin-bottom: 5px;
}

/* ---------- RESPONSIVE ---------- */

@media (max-width: 1100px) {
    .pl-reco-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .pl-reco-grid .pl-reco:nth-child(n) {
        grid-column: span 1;
    }
}

@media (max-width: 768px) {

    .block-container {
        padding: 3rem 0.9rem 1.5rem;
    }

    [data-testid="stColumn"] {
        flex: 1 1 100% !important;
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
    }

    .pl-top {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
        padding: 18px;
    }

    .pl-top-meta {
        justify-content: flex-start;
    }

    .pl-chip {
        white-space: normal;
    }

    .pl-panel {
        padding: 18px;
    }

    .pl-stats {
        flex-direction: column;
        gap: 8px;
    }

    .pl-stat b,
    .pl-stat span {
        white-space: normal;
    }

    .pl-reco-grid {
        grid-template-columns: 1fr;
    }

    .pl-reco-grid .pl-reco:nth-child(n) {
        grid-column: span 1;
    }

    .pl-dx {
        flex-direction: column;
        text-align: center;
    }

    .pl-ring {
        margin: 0 auto;
    }

    .pl-dx-nombre {
        font-size: 22px;
    }

    [data-testid="stImage"] img {
        max-height: 260px;
    }

}

/* ---------- ACCESIBILIDAD ---------- */

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        transition: none !important;
    }
}

</style>
"""
)

# ============================================================
# CARGAR MODELO
# ============================================================


@st.cache_resource
def cargar_modelo():

    return tf.keras.models.load_model("modelo_cafe.keras")


@st.cache_data
def cargar_clases():

    with open("class_names.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


modelo = cargar_modelo()
clases = cargar_clases()

# ============================================================
# PREDICCIÓN
# ============================================================


def predecir(imagen):

    imagen = imagen.convert("RGB")

    imagen = imagen.resize((224, 224))

    array = np.array(imagen).astype("float32")

    array = np.expand_dims(array, axis=0)

    predicciones = modelo.predict(array, verbose=0)[0]

    indice = int(np.argmax(predicciones))

    enfermedad = clases[indice]

    confianza = float(predicciones[indice]) * 100

    return (enfermedad, confianza, predicciones)


# ============================================================
# GROQ
# ============================================================


def obtener_cliente_groq():

    try:
        api_key = st.secrets["GROQ_API_KEY"]

        return Groq(api_key=api_key)

    except Exception:
        return None


def generar_recomendaciones(enfermedad, confianza):

    cliente = obtener_cliente_groq()

    if cliente is None:
        return {
            "descripcion": "La API de Groq no está configurada.",
            "diferenciacion": "No disponible.",
            "manejo": "No disponible.",
            "consulta": "Se recomienda consultar a un técnico agrícola.",
            "monitoreo": "Realice inspecciones periódicas.",
            "registro": "Registre fecha, ubicación y evolución.",
        }

    prompt = f"""
Eres un asistente técnico especializado
en enfermedades del cultivo de café.

Un modelo de inteligencia artificial analizó
una fotografía de una hoja de café.

Diagnóstico:
{enfermedad}

Confianza:
{confianza:.2f}%

Genera información técnica para un agricultor
o estudiante.

RESPONDE ÚNICAMENTE en este formato:

DESCRIPCION:
texto

DIFERENCIACION:
texto

MANEJO:
texto

CONSULTA:
texto

MONITOREO:
texto

REGISTRO:
texto

REQUISITOS:

- Explica brevemente la enfermedad detectada.
- Describe características que ayuden a diferenciarla.
- Proporciona manejo preventivo y agronómico.
- Incluye buenas prácticas para el cultivo.
- Indica cuándo consultar a un técnico.
- Explica qué debe monitorearse.
- Indica qué información conviene registrar.
- No inventes datos.
- No proporciones dosis de productos químicos.
- Para productos fitosanitarios indica seguir la etiqueta
  autorizada y consultar a un profesional local.
- Utiliza lenguaje claro y profesional.
"""

    try:
        respuesta = cliente.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un asistente técnico agrícola."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1800,
        )

        texto = respuesta.choices[0].message.content

        return interpretar_respuesta(texto)

    except Exception as error:
        return {
            "descripcion": f"No fue posible obtener información de Groq.",
            "diferenciacion": "No disponible.",
            "manejo": "No disponible.",
            "consulta": "Consultar a un técnico agrícola.",
            "monitoreo": "Realizar seguimiento periódico.",
            "registro": "Registrar la evolución del cultivo.",
            "error": str(error),
        }


# ============================================================
# INTERPRETAR RESPUESTA DE GROQ
# ============================================================


def interpretar_respuesta(texto):

    resultado = {
        "descripcion": "",
        "diferenciacion": "",
        "manejo": "",
        "consulta": "",
        "monitoreo": "",
        "registro": "",
    }

    secciones = {
        "DESCRIPCION:": "descripcion",
        "DIFERENCIACION:": "diferenciacion",
        "MANEJO:": "manejo",
        "CONSULTA:": "consulta",
        "MONITOREO:": "monitoreo",
        "REGISTRO:": "registro",
    }

    actual = None

    for linea in texto.splitlines():
        linea_limpia = linea.strip()

        if linea_limpia in secciones:
            actual = secciones[linea_limpia]

        elif actual and linea_limpia:
            resultado[actual] += linea_limpia + " "

    return resultado


# ============================================================
# PDF
# ============================================================


def crear_pdf(enfermedad, confianza, recomendaciones):

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)

    ancho, alto = letter

    y = alto - 55

    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawString(50, y, "AgroDetect Café")

    y -= 30

    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, y, f"Diagnóstico: {enfermedad}")

    y -= 18

    pdf.drawString(50, y, f"Confianza: {confianza:.2f}%")

    y -= 18

    pdf.drawString(50, y, datetime.now().strftime("Fecha: %d/%m/%Y %H:%M"))

    y -= 30

    secciones = [
        ("Descripción", recomendaciones["descripcion"]),
        ("Diferenciación", recomendaciones["diferenciacion"]),
        ("Manejo", recomendaciones["manejo"]),
        ("Consulta técnica", recomendaciones["consulta"]),
        ("Monitoreo", recomendaciones["monitoreo"]),
        ("Registro", recomendaciones["registro"]),
    ]

    for titulo, contenido in secciones:
        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(50, y, titulo)

        y -= 16

        pdf.setFont("Helvetica", 9)

        palabras = contenido.split()

        linea = ""

        for palabra in palabras:
            prueba = linea + " " + palabra

            if len(prueba) > 95:
                pdf.drawString(55, y, linea)

                y -= 12

                linea = palabra

                if y < 60:
                    pdf.showPage()

                    y = alto - 55

            else:
                linea = prueba

        if linea:
            pdf.drawString(55, y, linea)

            y -= 20

    pdf.save()

    buffer.seek(0)

    return buffer


# ============================================================
# INTERFAZ
# ============================================================

mostrar_html(
    """
    <div class="pl-top">

        <div class="pl-brand">

            <div class="pl-logo">🌿</div>

            <div>

                <div class="pl-brand-eyebrow">
                    Análisis foliar con IA
                </div>

                <div class="pl-brand-title">
                    AgroDetect <em>Café</em>
                </div>

            </div>

        </div>

        <div class="pl-top-meta">

            <div class="pl-chip">
                <strong>●</strong> Oscar Espino · 202310110465
            </div>

        </div>

    </div>
    """
)

columna_izquierda, columna_derecha = st.columns([5, 7], gap="large")

# ============================================================
# IZQUIERDA
# ============================================================

with columna_izquierda:
    mostrar_html(
        """
        <div class="pl-panel">

            <div class="pl-eyebrow">
                Paso 1 · Captura
            </div>

            <div class="pl-title-lg">
                Subir fotografía de la hoja
            </div>

            <div class="pl-body">
                Posicione la hoja bajo buena luz natural y
                encuádrela completa. Evite sombras y desenfoque
                para una detección más precisa.
            </div>

        </div>
        """
    )

    mostrar_html("<div style='height:14px'></div>")

    archivo = st.file_uploader(
        "Arrastre o seleccione una imagen",
        type=["jpg", "jpeg", "png"],
    )

    if archivo:
        imagen = Image.open(archivo).convert("RGB")

        mostrar_html("<div style='height:14px'></div>")

        mostrar_html(
            """
            <div class="pl-imagen">

                <div class="pl-eyebrow">
                    Vista previa
                </div>

            </div>
            """
        )

        st.image(imagen, use_container_width=True)

        mostrar_html("<div style='height:12px'></div>")

        if st.button("🔬 Analizar hoja", use_container_width=True):
            with st.spinner("Analizando imagen y generando recomendaciones..."):
                enfermedad, confianza, probabilidades = predecir(imagen)

                recomendaciones = generar_recomendaciones(enfermedad, confianza)

                st.session_state["diagnostico"] = enfermedad

                st.session_state["confianza"] = confianza

                st.session_state["recomendaciones"] = recomendaciones

    else:
        mostrar_html(
            """
            <div class="pl-empty">

                <div class="pl-empty-icono">🌿</div>

                <div class="pl-empty-titulo">
                    Esperando una foto
                </div>

                <div class="pl-empty-texto">
                    La fotografía aparecerá aquí junto con el
                    botón de análisis.
                </div>

            </div>
            """
        )

    mostrar_html(
        """
        <div class="pl-steps">

            <div class="pl-step">
                <b>1</b> Cargue la fotografía de la hoja
            </div>

            <div class="pl-step">
                <b>2</b> Obtenga el diagnóstico y la confianza
            </div>

            <div class="pl-step">
                <b>3</b> Descargue el informe en PDF
            </div>

        </div>
        """
    )

# ============================================================
# DERECHA
# ============================================================

with columna_derecha:
    mostrar_html(
        f"""
        <div class="pl-panel">

            <div class="pl-eyebrow">
                Resultado
            </div>

            <div class="pl-title-lg">
                Diagnóstico del análisis
            </div>

            <div class="pl-body">
                El sistema evalúa la imagen con un modelo de
                visión por computadora y complementa la respuesta
                con orientación técnica generada por IA.
            </div>

            <div class="pl-stats">

                <div class="pl-stat">
                    <b>TensorFlow</b>
                    <span>Modelo de visión CNN</span>
                </div>

                <div class="pl-stat">
                    <b>Groq LLM</b>
                    <span>Recomendaciones por IA</span>
                </div>

                <div class="pl-stat">
                    <b>PDF</b>
                    <span>Informe descargable</span>
                </div>

            </div>

        </div>
        """
    )

    if "diagnostico" not in st.session_state:
        mostrar_html(
            """
            <div style="height:16px"></div>

            <div class="pl-empty">

                <div class="pl-empty-icono">🧠</div>

                <div class="pl-empty-titulo">
                    Sin diagnóstico todavía
                </div>

                <div class="pl-empty-texto">
                    El resultado aparecerá aquí después de
                    analizar la fotografía desde la columna
                    izquierda.
                </div>

            </div>
            """
        )

    else:
        enfermedad = st.session_state["diagnostico"]

        confianza = st.session_state["confianza"]

        recomendaciones = st.session_state["recomendaciones"]

        grados = confianza * 3.6

        mostrar_html(
            """
            <div class="pl-result-head">

                <div class="pl-eyebrow">
                    Medición
                </div>

                <div class="pl-chip-claro">● Resultado en vivo</div>

            </div>
            """
        )

        mostrar_html(
            f"""
            <div class="pl-dx">

                <div class="pl-dx-info">

                    <div class="pl-dx-label">
                        Enfermedad identificada
                    </div>

                    <div class="pl-dx-nombre">
                        {enfermedad}
                    </div>

                    <div class="pl-dx-sub">
                        Detectado mediante inteligencia artificial
                    </div>

                </div>

                <div class="pl-ring" style="
                    background: conic-gradient(#2F6B45 0deg {grados:.2f}deg, #E2D9C6 {grados:.2f}deg 360deg);
                ">

                    <div class="pl-ring-core">

                        <div class="pl-ring-num">
                            {confianza:.1f}%
                        </div>

                        <div class="pl-ring-label">
                            CONFIANZA
                        </div>

                    </div>

                </div>

            </div>
            """
        )

        mostrar_html(
            """
            <div class="pl-section-title">
                Orientación y manejo preventivo
            </div>
            """
        )

        recomendaciones_visual = [
            (
                "01",
                "Diferenciación a simple vista",
                recomendaciones["diferenciacion"],
            ),
            (
                "02",
                "Manejo agronómico preventivo",
                recomendaciones["manejo"],
            ),
            (
                "03",
                "Consulta a un técnico",
                recomendaciones["consulta"],
            ),
            (
                "04",
                "Monitoreo y seguimiento",
                recomendaciones["monitoreo"],
            ),
            (
                "05",
                "Registro y trazabilidad",
                recomendaciones["registro"],
            ),
        ]

        tarjetas = ""

        for numero, titulo, texto in recomendaciones_visual:
            tarjetas = tarjetas + f"""
                <div class="pl-reco">

                    <div class="pl-reco-top">

                        <div class="pl-reco-num">
                            {numero}
                        </div>

                        <div class="pl-reco-titulo">
                            {titulo}
                        </div>

                    </div>

                    <div class="pl-reco-texto">
                        {texto}
                    </div>

                </div>
                """

        mostrar_html(
            f"""
            <div class="pl-reco-grid">
                {tarjetas}
            </div>
            """
        )

        pdf = crear_pdf(enfermedad, confianza, recomendaciones)

        mostrar_html("<div style='height:14px'></div>")

        st.download_button(
            "📄 Descargar informe PDF",
            data=pdf,
            file_name="diagnostico_agrodetect.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# ============================================================
# PIE
# ============================================================

mostrar_html(
    """
    <div class="pl-footer">

        <span class="pl-footer-brand">
            AGRODETECT CAFÉ
        </span>

        Sistema de apoyo para diagnóstico foliar mediante
        inteligencia artificial · 2026<br>

        Proyecto académico · Oscar Espino · 202310110465

    </div>
    """
)