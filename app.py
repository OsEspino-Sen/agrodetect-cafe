import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io
import re
import unicodedata
from datetime import datetime
from groq import Groq
from markdown_it import MarkdownIt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def mostrar_html(contenido):
    st.html(contenido)


def es_dispositivo_movil():
    """
    Detecta si la aplicación se está usando desde un teléfono
    o tablet mediante el agente de usuario del navegador.
    Se puede forzar desde la URL con ?movil=1 o ?movil=0.
    """

    try:
        forzar = st.query_params.get("movil")

        if forzar == "1":
            return True

        if forzar == "0":
            return False

    except Exception:
        pass

    try:
        agente = st.context.headers.get("User-Agent", "")
    except Exception:
        agente = ""

    return bool(
        re.search(
            r"Mobile|Android|iPhone|iPad|iPod|IEMobile|"
            r"Opera Mini|Windows Phone|Silk|BlackBerry",
            agente,
        )
    )


renderizador_markdown = MarkdownIt(
    "commonmark", {"html": False}
).enable(["table", "strikethrough"])


def formatear_markdown(texto):
    """
    Convierte el texto con markdown de Groq a HTML para poder
    mostrarlo en las tarjetas de la interfaz.
    """

    if not texto:
        return ""

    return renderizador_markdown.render(texto)


def limpiar_markdown(texto):
    """
    Elimina el markdown y devuelve texto plano para el PDF.
    """

    if not texto:
        return ""

    texto = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)

    lineas = []

    for linea in texto.splitlines():

        linea = linea.strip()

        if linea.startswith("|"):
            celdas = [
                celda.strip()
                for celda in linea.strip("|").split("|")
            ]
            celdas = [
                celda
                for celda in celdas
                if celda and not re.fullmatch(r":?-{3,}:?", celda)
            ]
            linea = " · ".join(celdas)
        else:
            linea = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", linea)

        lineas.append(linea)

    texto = " ".join(lineas)

    texto = re.sub(r"\*\*|\*|`|~~|_", "", texto)

    return re.sub(r"\s+", " ", texto).strip()


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
    max-height: 240px;
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

.pl-head-chips {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
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
    margin: 28px 0 16px;
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
    grid-template-columns: 1fr;
    gap: 14px;
}

.pl-reco {
    background: #FFFFFF;
    border: 1px solid #E6DCC9;
    border-radius: 16px;
    padding: 18px 20px 20px;
    box-shadow: 0 6px 18px -16px rgba(27, 59, 40, 0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.pl-reco:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 24px -16px rgba(27, 59, 40, 0.45);
}

.pl-reco-top {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    margin: -18px -20px 15px;
    background: linear-gradient(135deg, #F4F0E6, #EDE8DA);
    border-bottom: 1px solid #E6DCC9;
    border-radius: 16px 16px 0 0;
}

.pl-reco-conclusion .pl-reco-top {
    background: linear-gradient(135deg, #EAF3E9, #E0EDDE);
}

.pl-reco-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    flex: none;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    color: #F2F9EE;
    background: #2F6B45;
    border-radius: 10px;
    box-shadow: 0 3px 8px -3px rgba(47, 107, 69, 0.5);
}

.pl-reco-titulo {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #2C4A35;
    line-height: 1.35;
}

.pl-reco-texto {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    line-height: 1.7;
    color: #6E6557;
    text-align: justify;
    hyphens: auto;
}

.pl-reco-texto p {
    margin: 0 0 8px;
}

.pl-reco-texto p:last-child {
    margin-bottom: 0;
}

.pl-reco-texto strong {
    color: #2C4A35;
}

.pl-reco-texto ul,
.pl-reco-texto ol {
    margin: 6px 0 8px 18px;
    padding: 0;
}

.pl-reco-texto li {
    margin-bottom: 5px;
}

.pl-reco-texto table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 10px;
    font-size: 12px;
}

.pl-reco-texto th,
.pl-reco-texto td {
    border: 1px solid #E6DCC9;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
}

.pl-reco-texto th {
    background: #F2F9EE;
    color: #2C4A35;
    font-weight: 700;
}

.pl-reco-conclusion {
    margin-top: 14px;
    border-left: 4px solid #2F6B45;
    background: #FBFAF6;
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

    .pl-top {
        padding: 18px 22px;
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

/* ---------- ANIMACIONES ---------- */

@keyframes pl-aparecer {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: none;
    }
}

.pl-panel,
.pl-dx,
.pl-reco,
.pl-result-head {
    animation: pl-aparecer 0.45s ease both;
}

.pl-reco:nth-of-type(2) {
    animation-delay: 0.05s;
}

/* ---------- ACCESIBILIDAD ---------- */

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        transition: none !important;
        animation: none !important;
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

colores_clase = {
    "Roya": "#C96F3B",
    "Minador": "#B0892E",
    "Phoma": "#7A7480",
    "Healthy": "#2F6B45",
}

tintes_clase = {
    "Roya": "#F8ECE2",
    "Minador": "#F5EFDF",
    "Phoma": "#EEEBF0",
    "Healthy": "#EAF2E6",
}

print("CLASES DEL MODELO:", clases)

# ============================================================
# PREDICCIÓN
# ============================================================


def predecir(imagen):

    imagen = imagen.convert("RGB")
    imagen = imagen.resize((224, 224))


    array = np.array(imagen).astype("float32")
    array = np.expand_dims(array, axis=0)


    predicciones = modelo.predict(array, verbose=0)[0]


    # ------------------------------------------------------------
    # PREDICCIÓN PRINCIPAL
    # ------------------------------------------------------------


    indice = int(np.argmax(predicciones))
    enfermedad = clases[indice]
    confianza = float(predicciones[indice]) * 100


    print("PREDICCIONES:", predicciones)
    print("INDICE:", indice)
    print("CLASE:", enfermedad)
    print("CONFIANZA:", confianza)


    return (enfermedad, confianza, predicciones)


# ============================================================
# GROQ
# ============================================================


def obtener_cliente_groq():

    api_key = None

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    if api_key is None:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            pass

    if not api_key or not str(api_key).strip():
        return None

    return Groq(api_key=api_key)


def generar_recomendaciones(enfermedad, confianza, probabilidades=None):
    """
    Genera orientación técnica mediante Groq con dos modelos en
    cascada (principal y de respaldo) y un modo de emergencia
    local si ambos fallan.
    """


    cliente = obtener_cliente_groq()


    # ------------------------------------------------------------
    # Si Groq no está configurado, usar orientación local
    # ------------------------------------------------------------
    if cliente is None:
        return generar_recomendacion_local(enfermedad, confianza, probabilidades)


    # ------------------------------------------------------------
    # Preparar distribución del modelo
    # ------------------------------------------------------------
    distribucion = ""


    if probabilidades is not None:
        for clase, probabilidad in zip(clases, probabilidades):
            distribucion += (
                f"- {clase}: {float(probabilidad) * 100:.2f}%\n"
            )


    # ------------------------------------------------------------
    # Primera y segunda posibilidad del modelo
    # ------------------------------------------------------------
    primera = "No disponible"

    segunda = "No disponible"

    nivel = ""

    diferencia = None

    diferencia_pct = "No disponible"


    if probabilidades is not None and len(probabilidades) >= 2:

        pares = sorted(
            zip(clases, probabilidades),
            key=lambda par: float(par[1]),
            reverse=True
        )

        primera = f"{pares[0][0]} ({float(pares[0][1]) * 100:.2f}%)"

        segunda = f"{pares[1][0]} ({float(pares[1][1]) * 100:.2f}%)"

        diferencia = float(pares[0][1]) - float(pares[1][1])

        diferencia_pct = f"{diferencia * 100:.2f}%"

        if diferencia >= 0.30:
            nivel = "Predicción claramente dominante"
        elif diferencia >= 0.15:
            nivel = "Separación moderada entre las dos primeras posibilidades"
        else:
            nivel = (
                "Alta competencia entre las dos primeras posibilidades; "
                "se recomienda verificación adicional en campo"
            )


    # ------------------------------------------------------------
    # Prompt técnico
    # ------------------------------------------------------------
    prompt = f"""
Eres un especialista en sanidad vegetal y manejo agronómico
del cultivo de café.


Estás apoyando un sistema académico de detección de enfermedades
en hojas de café.


IMPORTANTE:


El diagnóstico NO fue realizado por ti.


Fue producido por un modelo de inteligencia artificial para
clasificación de imágenes.


Tu función es interpretar técnicamente el resultado y proporcionar
orientación agronómica clara, responsable y útil.


RESULTADO DEL MODELO
--------------------


Clase principal:
{enfermedad}


Confianza:
{confianza:.2f}%


Distribución completa:
{distribucion}


Primera posibilidad:
{primera}


Segunda posibilidad:
{segunda}


Diferencia entre las dos primeras:
{diferencia_pct}


Nivel de separación:
{nivel}


El usuario necesita información sobre la clase identificada.


NORMAS DE CONTEXTO
------------------


1. NO afirmes que observaste directamente la fotografía.
   El diagnóstico fue producido por un modelo de clasificación
   de imágenes, no por ti.


2. NO inventes síntomas, estructuras, colores o características
   que supuestamente aparecen en la imagen.


3. Diferencia entre:
   - lo que predijo el modelo;
   - las características que normalmente se utilizan para reconocer
     la enfermedad en campo.


4. Una confianza alta del modelo NO significa que exista certeza
   absoluta de diagnóstico.


5. Si la predicción es Healthy:
   - explica que el modelo no detectó evidencia suficiente de
     Roya, Minador ni Phoma en la hoja analizada;
   - indica que esto no descarta la presencia de otros problemas;
   - recomienda mantener prácticas preventivas y monitoreo.


6. Si la separación entre la primera y la segunda posibilidad es
   baja (nivel "Alta competencia"), advierte que el diagnóstico
   del modelo es menos definitivo y que la verificación en campo
   es especialmente recomendable.


7. Si la predicción corresponde a una enfermedad, proporciona
   información técnica específica para esa enfermedad.


8. NO inventes dosis de fungicidas, insecticidas o fertilizantes.


9. Si mencionas productos fitosanitarios, indica que deben
   utilizarse únicamente conforme a la etiqueta autorizada y la
   normativa local, con orientación profesional.


10. No recomiendes tratamientos químicos como primera respuesta.
    Prioriza manejo preventivo, monitoreo y buenas prácticas
    agrícolas.


11. Utiliza lenguaje profesional pero fácil de entender para un
    estudiante o productor de café.


12. La respuesta debe ser específica. Evita frases genéricas como
    "realizar seguimiento" sin explicar qué debe observarse.


RESPONDE EXACTAMENTE CON ESTAS SECCIONES:


DESCRIPCION:
Explica qué es la enfermedad o condición identificada, su
importancia en el cultivo de café y, cuando sea apropiado, el
agente causal. Si la predicción es Healthy, explica que significa
ausencia de evidencia suficiente en la hoja analizada.


DIFERENCIACION:
Explica las características que normalmente permiten diferenciar
esta condición de otras enfermedades o daños similares: distribución
de las lesiones, posición en la hoja, color, textura u otros
criterios de identificación en campo. Aclara que son criterios
generales de identificación y que el modelo no constituye
confirmación definitiva.


MANEJO:
Proporciona medidas preventivas y agronómicas concretas y
específicas para la condición identificada. Considera aspectos como
humedad, ventilación, sombra, manejo del follaje, eliminación de
material afectado, nutrición equilibrada y densidad del cultivo.
Si la predicción es Healthy, indica las prácticas preventivas
recomendadas para mantener hoja sana.


CONSULTA:
Explica cuándo sería recomendable consultar a un técnico agrícola
o especialista: incertidumbre del diagnóstico, avance rápido de
síntomas, afectación importante en el lote, otras hojas o plantas
con síntomas, o dudas sobre productos a aplicar.


MONITOREO:
Indica exactamente qué debería vigilar el productor: síntomas,
distribución en la planta, nuevas hojas afectadas, progresión de
lesiones, presencia de insectos u otros indicadores relevantes.
Explica también cómo comparar observaciones en el tiempo para
detectar avance o retroceso.


REGISTRO:
Indica qué información debería registrarse para realizar
trazabilidad: fecha, ubicación, lote, porcentaje aproximado de
plantas afectadas, síntomas observados, fotografías, evolución y
medidas realizadas.


CONCLUSION:
Resume en pocas líneas qué significa el resultado de la IA y cuál
debería ser el siguiente paso recomendado.


La respuesta debe ser técnica, concreta y útil.
No utilices emojis.
"""


    # ------------------------------------------------------------
    # Modelo principal: openai/gpt-oss-120b
    # ------------------------------------------------------------
    try:


        respuesta = cliente.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un especialista en sanidad vegetal, "
                        "enfermedades del café y manejo agronómico. "
                        "Proporcionas información técnica responsable "
                        "sin inventar observaciones."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.25,
            max_tokens=3000
        )


        texto = respuesta.choices[0].message.content


        resultado = extraer_secciones(texto)


        if not respuesta_valida(resultado):
            raise ValueError(
                "Respuesta vacía o incompleta del modelo principal"
            )


        print("ORIENTACIÓN: modelo principal (openai/gpt-oss-120b)")


        return resultado


    except Exception as e:
        print("ERROR MODELO PRINCIPAL:", e)


    # ------------------------------------------------------------
    # Modelo de respaldo: llama-3.1-8b-instant
    # ------------------------------------------------------------
    try:


        respuesta = cliente.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un especialista en sanidad vegetal, "
                        "enfermedades del café y manejo agronómico. "
                        "Proporcionas información técnica responsable "
                        "sin inventar observaciones."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.25,
            max_tokens=1200
        )


        texto = respuesta.choices[0].message.content


        resultado = extraer_secciones(texto)


        if not respuesta_valida(resultado):
            raise ValueError(
                "Respuesta vacía o incompleta del modelo de respaldo"
            )


        print("ORIENTACIÓN: modelo de respaldo (llama-3.1-8b-instant)")


        return resultado


    except Exception as e:
        print("ERROR MODELO DE RESPALDO:", e)


    # ------------------------------------------------------------
    # Modo emergencia: orientación técnica local
    # ------------------------------------------------------------
    return generar_recomendacion_local(
        enfermedad,
        confianza,
        probabilidades
    )


# ============================================================
# SECCIONES DE RESPUESTA Y ORIENTACIÓN LOCAL DE EMERGENCIA
# ============================================================


def normalizar_encabezado(texto):
    """
    Quita acentos y adornos de markdown para tolerar variantes
    del modelo como **DESCRIPCION**, DESCRIPCIÓN o 1. DESCripcion.
    """

    texto = "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )

    return texto.strip().upper().lstrip("#*->·•0123456789 ).")


def extraer_secciones(texto):
    """
    Extrae las secciones de la respuesta de Groq tolerando
    encabezados con o sin tildes, con o sin dos puntos y adornos
    de markdown como negritas, listas o numeración.
    """

    resultado = {
        "descripcion": "",
        "diferenciacion": "",
        "manejo": "",
        "consulta": "",
        "monitoreo": "",
        "registro": "",
        "conclusion": ""
    }

    if not texto or not texto.strip():
        return resultado

    seccion_actual = None

    nombres = {
        "DESCRIPCION": "descripcion",
        "DIFERENCIACION": "diferenciacion",
        "MANEJO": "manejo",
        "CONSULTA": "consulta",
        "MONITOREO": "monitoreo",
        "REGISTRO": "registro",
        "CONCLUSION": "conclusion",
    }

    patron = re.compile(
        "^(" + "|".join(nombres.keys()) + r")(?::|\b)"
    )

    for linea in texto.splitlines():

        linea_limpia = linea.strip()

        if not linea_limpia:
            continue

        encabezado = patron.match(normalizar_encabezado(linea_limpia))

        if encabezado:

            nombre = encabezado.group(1)

            seccion_actual = nombres[nombre]

            if ":" in linea_limpia:
                contenido = linea_limpia.split(":", 1)[1].strip()

                if contenido:
                    resultado[seccion_actual] += contenido + "\n"

        elif seccion_actual is not None:
            resultado[seccion_actual] += linea_limpia + "\n"

    for clave in resultado:
        resultado[clave] = resultado[clave].strip()

    return resultado


def respuesta_valida(resultado):
    """
    Verifica que la respuesta contenga suficiente contenido
    técnico para ser considerada completa.
    """

    if not resultado:
        return False

    secciones_no_vacias = sum(
        1 for valor in resultado.values() if valor.strip()
    )

    if secciones_no_vacias < 4:
        return False

    if not resultado["descripcion"] or not resultado["manejo"]:
        return False

    return True


def generar_recomendacion_local(enfermedad, confianza, probabilidades=None):
    """
    Orientación técnica de emergencia generada localmente cuando
    la API de Groq no está disponible o ambos modelos fallan.
    """

    print("ORIENTACIÓN: modo local de emergencia (sin API de Groq)")

    plantillas = {
        "Roya": {
            "descripcion": (
                "La Roya del café es una enfermedad foliar causada por "
                "el hongo Hemileia vastatrix. Se considera la afección "
                "de mayor impacto económico en el cultivo de café a "
                "nivel mundial, ya que provoca la caída de hojas "
                "infectadas y reduce la capacidad fotosintética de la "
                "planta, afectando la producción de los años siguientes."
            ),
            "diferenciacion": (
                "Se caracteriza por manchas amarillentas o naranjas en "
                "el envés de la hoja que corresponden a las pústulas "
                "del hongo en forma de polvo. A diferencia de Phoma, no "
                "se observan anillos concéntricos ni muerte uniforme "
                "del tejido, y a diferencia del daño de Minador, no hay "
                "galerías sinuosas ni minas visibles en el interior de "
                "la lámina foliar."
            ),
            "manejo": (
                "Priorice variedades resistentes, regulación de sombra "
                "y buena ventilación del follaje. Elimine y separe el "
                "material vegetal afectado, evite el exceso de humedad "
                "en el dosel y mantenga una nutrición equilibrada, "
                "especialmente potasio, para reducir la severidad de la "
                "enfermedad. Cualquier producto fitosanitario debe "
                "usarse solo conforme a la etiqueta autorizada y con "
                "orientación profesional."
            ),
            "consulta": (
                "Consulte a un técnico agrícola si el porcentaje de "
                "hojas afectadas aumenta rápidamente, si la defoliación "
                "supera niveles tolerables o si desea confirmar el uso "
                "de fungicidas en la etapa de floración o llenado "
                "de frutos."
            ),
            "monitoreo": (
                "Vigile el envés de las hojas en busca de pústulas "
                "naranjas, la presencia de hojas amarillas en la "
                "plantación y la caída de follaje. Compare el avance "
                "semana a semana en los mismos árboles y registre "
                "cuántas hojas nuevas presentan síntomas."
            ),
            "registro": (
                "Registre fecha, lote, número de plantas afectadas, "
                "porcentaje estimado de hojas con pústulas, condiciones "
                "de humedad y lluvia, y las medidas preventivas "
                "aplicadas para comparar la evolución."
            ),
            "conclusion": (
                f"El modelo sugiere Roya con una confianza de "
                f"{confianza:.2f}%. Se recomienda confirmar la "
                "presencia de pústulas en campo y aplicar de inmediato "
                "manejo preventivo y monitoreo."
            )
        },
        "Minador": {
            "descripcion": (
                "El Minador de la hoja del café es un insecto de la "
                "familia Lepidoptera (Leucoptera coffeella) cuyas "
                "larvas se alimentan del tejido interno de la hoja, "
                "formando minas o galerías. Su presencia reduce el área "
                "fotosintética, debilita el árbol y puede causar "
                "defoliación en periodos secos."
            ),
            "diferenciacion": (
                "El daño se observa como líneas o manchas sinuosas de "
                "color pardo translúcido dentro de la lámina foliar, a "
                "diferencia de las pústulas naranjas de la Roya y de "
                "las lesiones oscuras con anillos de Phoma. En ataques "
                "fuertes, el tejido dañado se necrosa y la hoja cae."
            ),
            "manejo": (
                "Mantenga el cultivo con riego y sombra adecuados: el "
                "estrés hídrico favorece la plaga. Revise periódicamente "
                "las hojas jóvenes, elimine hojas muy dañadas y "
                "conserve enemigos naturales. Evite el uso de "
                "insecticidas de amplio espectro salvo indicación "
                "técnica, y si se usan, siga la etiqueta autorizada "
                "y la normativa local."
            ),
            "consulta": (
                "Consulte a un técnico si las minas se extienden a la "
                "mayoría de las hojas de un lote, si la defoliación "
                "aumenta o si observa una alta presencia simultánea de "
                "larvas y hojas necrosadas."
            ),
            "monitoreo": (
                "Vigile la aparición de galerías en hojas nuevas, "
                "cuente hojas con minas por rama y observe si las "
                "lesiones avanzan de la zona central hacia los bordes. "
                "Compare la intensidad del daño entre visitas para "
                "detectar incrementos."
            ),
            "registro": (
                "Registre fecha, lote, número de hojas con minas por "
                "muestra, etapa de desarrollo del cultivo, condiciones "
                "climáticas y cualquier acción de manejo realizada."
            ),
            "conclusion": (
                f"El modelo sugiere Minador con una confianza de "
                f"{confianza:.2f}%. Se recomienda inspeccionar las "
                "hojas en busca de galerías características y reforzar "
                "el monitoreo semanal."
            )
        },
        "Phoma": {
            "descripcion": (
                "Phoma es una enfermedad fúngica asociada al hongo "
                "Phoma costarricensis, que ataca principalmente hojas, "
                "ramas y frutos jóvenes del café. Se presenta con "
                "frecuencia en épocas de lluvia, humedad alta y "
                "densidades de siembra elevadas, favoreciendo la "
                "defoliación y el debilitamiento del árbol."
            ),
            "diferenciacion": (
                "Produce lesiones de color pardo oscuro a negro, "
                "generalmente de forma irregular y con aspecto de "
                "apagado, que pueden agruparse como anillos "
                "concéntricos. Se distingue de la Roya por la ausencia "
                "de pústulas naranjas y del Minador por la ausencia de "
                "galerías internas en la lámina foliar."
            ),
            "manejo": (
                "Reduzca la humedad excesiva del dosel con podas de "
                "aireación, regulación de sombra y distancias de "
                "siembra adecuadas. Recoja y retire hojas y ramas "
                "afectadas y evite el riego por aspersión prolongado. "
                "Mantenga la nutrición del cultivo para favorecer la "
                "recuperación; los fungicidas solo con etiqueta "
                "autorizada y asesoría técnica."
            ),
            "consulta": (
                "Consulte a un técnico si las lesiones se extienden a "
                "ramas o frutos, si la defoliación se generaliza en el "
                "lote o si convive con otras enfermedades que "
                "compliquen el diagnóstico."
            ),
            "monitoreo": (
                "Vigile la aparición de lesiones oscuras en hojas "
                "jóvenes y maduras, la extensión a ramas y frutos, y la "
                "relación con periodos lluviosos. Realice muestreos "
                "consecutivos en los mismos árboles para evaluar "
                "progresión."
            ),
            "registro": (
                "Registre fecha, lote, porcentaje de hojas con lesiones, "
                "presencia en ramas o frutos, condiciones de humedad y "
                "lluvia, y las podas o retiros de material realizados."
            ),
            "conclusion": (
                f"El modelo sugiere Phoma con una confianza de "
                f"{confianza:.2f}%. Se recomienda verificar la "
                "presencia de lesiones oscuras y priorizar la "
                "reducción de humedad en el follaje."
            )
        },
        "Healthy": {
            "descripcion": (
                "La hoja analizada no presenta evidencia suficiente de "
                "Roya, Minador ni Phoma para el modelo de clasificación. "
                "Un resultado Healthy indica una hoja aparentemente "
                "sana, aunque no descarta otros problemas no incluidos "
                "en el conjunto de clases del sistema."
            ),
            "diferenciacion": (
                "Una hoja sana presenta color verde uniforme, lámina "
                "sin manchas, pústulas ni galerías, y aspecto turgente. "
                "La ausencia de estos signos distingue el resultado "
                "Healthy de las tres condiciones que el modelo está "
                "entrenado para detectar."
            ),
            "manejo": (
                "Mantenga las prácticas preventivas: monitoreo foliar "
                "periódico, nutrición balanceada, control de la sombra, "
                "podas de ventilación y manejo adecuado del agua. Estas "
                "medidas reducen la probabilidad de aparición de "
                "enfermedades en el cultivo."
            ),
            "consulta": (
                "No es imprescindible consultar a un técnico en este "
                "momento. Haga la consulta si aparecen nuevos síntomas "
                "en otras hojas, si la plantación presenta daños "
                "diferentes a los evaluados o si sospecha de problemas "
                "no cubiertos por el sistema."
            ),
            "monitoreo": (
                "Vigile el envés y el haz de las hojas nuevas y "
                "maduras, la aparición de manchas amarillas, naranjas "
                "u oscuras y cualquier galería. Repita el muestreo en "
                "los mismos árboles cada semana para detectar cambios "
                "tempranos."
            ),
            "registro": (
                "Registre la fecha, el lote y el resultado del análisis "
                "como referencia de estado sano, y documente cualquier "
                "cambio posterior para detectar la aparición de "
                "enfermedades a tiempo."
            ),
            "conclusion": (
                f"El modelo no detectó evidencia de enfermedades con "
                f"una confianza de {confianza:.2f}%. Se recomienda "
                "mantener el monitoreo preventivo y repetir el análisis "
                "ante cualquier cambio visual."
            )
        }
    }

    plantilla = plantillas.get(enfermedad)

    if plantilla is None:
        plantilla = {
            "descripcion": (
                "El modelo identificó una clase que no pertenece al "
                "conjunto de condiciones evaluadas por este sistema. "
                "El resultado debe interpretarse con precaución y "
                "verificarse directamente en campo."
            ),
            "diferenciacion": (
                "No es posible establecer características de "
                "diferenciación para esta clase sin información "
                "adicional. Se recomienda comparar el aspecto de la "
                "hoja con los síntomas de Roya, Minador y Phoma para "
                "descartarlos."
            ),
            "manejo": (
                "Mantenga el cultivo con prácticas preventivas: "
                "monitoreo foliar, nutrición equilibrada, regulación "
                "de sombra y manejo de humedad, hasta confirmar la "
                "condición observada con un especialista."
            ),
            "consulta": (
                "Consulte a un técnico agrícola para identificar la "
                "condición real de la hoja, ya que el resultado del "
                "modelo no corresponde a las clases conocidas."
            ),
            "monitoreo": (
                "Vigile la evolución de los síntomas observados, "
                "su distribución en la planta y su propagación a "
                "otras hojas o árboles, y registre fotografías "
                "periódicas para comparar."
            ),
            "registro": (
                "Registre fecha, ubicación, lote, descripción de los "
                "síntomas, fotografías y evolución para apoyar el "
                "diagnóstico del especialista."
            ),
            "conclusion": (
                f"El modelo reporta la clase {enfermedad} con una "
                f"confianza de {confianza:.2f}%, pero no corresponde "
                "a las condiciones conocidas. Se recomienda verificar "
                "en campo con apoyo técnico."
            )
        }

    return plantilla


# ============================================================
# PDF
# ============================================================


def crear_pdf(enfermedad, confianza, recomendaciones, probabilidades=None):

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

    if probabilidades is not None:

        y -= 24

        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(50, y, "Distribución de probabilidades")

        for clase, probabilidad in zip(clases, probabilidades):

            y -= 14

            pdf.setFont("Helvetica", 10)

            pdf.drawString(60, y, f"{clase}: {float(probabilidad) * 100:.2f}%")

    y -= 30

    secciones = [
        ("Descripción", recomendaciones["descripcion"]),
        ("Diferenciación", recomendaciones["diferenciacion"]),
        ("Manejo", recomendaciones["manejo"]),
        ("Consulta técnica", recomendaciones["consulta"]),
        ("Monitoreo", recomendaciones["monitoreo"]),
        ("Registro", recomendaciones["registro"]),
        ("Conclusión", recomendaciones["conclusion"]),
    ]

    for titulo, contenido in secciones:
        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(50, y, titulo)

        y -= 16

        pdf.setFont("Helvetica", 9)

        palabras = limpiar_markdown(contenido).split()

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

    if y < 80:
        pdf.showPage()

        y = alto - 55

    pdf.setFont("Helvetica-Oblique", 8)

    pdf.drawString(
        50,
        y,
        "Clasificación: TensorFlow · "
        "Orientación técnica: Groq (openai/gpt-oss-120b)"
    )

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

columna_izquierda, columna_derecha = st.columns([6, 6], gap="large")

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

    movil = es_dispositivo_movil()

    imagen_capturada = None

    if movil:

        tab_archivo, tab_camara = st.tabs(
            ["📤 Subir galería", "📷 Tomar foto"]
        )

        with tab_archivo:
            archivo = st.file_uploader(
                "Arrastre o seleccione una imagen",
                type=["jpg", "jpeg", "png"],
            )

            if archivo is not None:
                imagen_capturada = Image.open(archivo).convert("RGB")

        with tab_camara:
            foto_camara = st.camera_input(
                "Enfocar la hoja y capturar con la cámara"
            )

            if foto_camara is not None:
                imagen_capturada = Image.open(foto_camara).convert("RGB")

    else:

        archivo = st.file_uploader(
            "Arrastre o seleccione una imagen",
            type=["jpg", "jpeg", "png"],
        )

        if archivo is not None:
            imagen_capturada = Image.open(archivo).convert("RGB")

    if imagen_capturada is not None:

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

        st.image(imagen_capturada, width="stretch")

        mostrar_html("<div style='height:12px'></div>")

        if st.button("🔬 Analizar hoja", width="stretch"):
            with st.spinner("Analizando imagen y generando recomendaciones..."):
                enfermedad, confianza, probabilidades = predecir(
                    imagen_capturada
                )

                recomendaciones = generar_recomendaciones(
                    enfermedad,
                    confianza,
                    probabilidades
                )

                st.session_state["diagnostico"] = enfermedad

                st.session_state["confianza"] = confianza

                st.session_state["probabilidades"] = probabilidades

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

    mostrar_html(
        """
        <div class="pl-panel">

            <div class="pl-eyebrow">
                Proceso del sistema
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

# ============================================================
# DERECHA
# ============================================================

with columna_derecha:
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

        color_clase = colores_clase.get(
            enfermedad,
            "#2F6B45"
        )

        tinte_clase = tintes_clase.get(
            enfermedad,
            "#EAF2E6"
        )

        if confianza >= 70:
            texto_confianza = "Confianza alta"
            color_confianza = "#2F6B45"
            fondo_confianza = "#EAF2E6"
            borde_confianza = "#CFE0C8"

        elif confianza >= 50:
            texto_confianza = "Confianza media"
            color_confianza = "#A07C18"
            fondo_confianza = "#F7F0D9"
            borde_confianza = "#E6D9A8"

        else:
            texto_confianza = "Confianza baja"
            color_confianza = "#B4472F"
            fondo_confianza = "#F8E9E2"
            borde_confianza = "#E8C8BC"

        mostrar_html(
            f"""
            <div class="pl-result-head">

                <div class="pl-eyebrow">
                    Medición
                </div>

                <div class="pl-head-chips">

                    <div class="pl-chip-claro">● Resultado en vivo</div>

                    <div class="pl-chip-claro" style="
                        color: {color_confianza};
                        background: {fondo_confianza};
                        border-color: {borde_confianza};
                    ">
                        ● {texto_confianza}
                    </div>

                </div>

            </div>
            """
        )

        mostrar_html(
            f"""
            <div class="pl-dx" style="
                background: linear-gradient(135deg, {tinte_clase}, #FFFFFF 65%);
                border-color: {color_clase}55;
            ">

                <div class="pl-dx-info">

                    <div class="pl-dx-label" style="color: {color_clase};">
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
                    background: conic-gradient({color_clase} 0deg {grados:.2f}deg, #E2D9C6 {grados:.2f}deg 360deg);
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
            <div style="height:28px"></div>
            """
        )

        probabilidades = st.session_state.get("probabilidades")

        if probabilidades is not None:

            porcentajes = [
                float(p) * 100
                for p in probabilidades
            ]

            resultados_ordenados = sorted(
                zip(clases, porcentajes),
                key=lambda x: x[1],
                reverse=True
            )

            primera_clase = resultados_ordenados[0][0]
            primera_prob = resultados_ordenados[0][1]

            segunda_clase = resultados_ordenados[1][0]
            segunda_prob = resultados_ordenados[1][1]

            diferencia = primera_prob - segunda_prob

            if diferencia >= 30:
                nivel_prediccion = "Predicción claramente dominante"
                descripcion_prediccion = (
                    "Una clase presenta una ventaja amplia sobre "
                    "las demás clases evaluadas."
                )

            elif diferencia >= 15:
                nivel_prediccion = "Predicción con separación moderada"
                descripcion_prediccion = (
                    "La clase principal supera a la segunda posibilidad, "
                    "aunque existe cierta competencia entre ambas."
                )

            else:
                nivel_prediccion = "Predicción con alta competencia"
                descripcion_prediccion = (
                    "Las primeras clases presentan valores cercanos. "
                    "La imagen debe interpretarse con mayor precaución."
                )

            mostrar_html(
                f"""
                <div style="
                    margin-top: 25px;
                    padding: 22px;
                    border: 1px solid #ddd5ca;
                    border-radius: 14px;
                    background: #faf8f4;
                ">

                    <div style="
                        font-size: 12px;
                        letter-spacing: 1.5px;
                        font-weight: 700;
                        margin-bottom: 12px;
                    ">
                        ANALISIS DE LA PREDICCION
                    </div>

                    <div style="
                        font-size: 25px;
                        font-weight: 700;
                        margin-bottom: 5px;
                    ">
                        {primera_clase}
                    </div>

                    <div style="
                        font-size: 14px;
                        margin-bottom: 20px;
                    ">
                        Predicción principal del modelo:
                        <b>{primera_prob:.1f}%</b>
                    </div>

                    <div style="
                        display: flex;
                        gap: 12px;
                        flex-wrap: wrap;
                    ">

                        <div style="
                            flex: 1;
                            min-width: 190px;
                            padding: 14px;
                            border-radius: 10px;
                            background: white;
                            border: 1px solid #e3ddd4;
                        ">
                            <div style="font-size: 11px; opacity: .65;">
                                PRIMERA POSIBILIDAD
                            </div>

                            <div style="
                                font-size: 19px;
                                font-weight: 700;
                                margin-top: 5px;
                            ">
                                {primera_clase}
                            </div>

                            <div style="font-size: 15px;">
                                {primera_prob:.1f}%
                            </div>
                        </div>

                        <div style="
                            flex: 1;
                            min-width: 190px;
                            padding: 14px;
                            border-radius: 10px;
                            background: white;
                            border: 1px solid #e3ddd4;
                        ">
                            <div style="font-size: 11px; opacity: .65;">
                                SEGUNDA POSIBILIDAD
                            </div>

                            <div style="
                                font-size: 19px;
                                font-weight: 700;
                                margin-top: 5px;
                            ">
                                {segunda_clase}
                            </div>

                            <div style="font-size: 15px;">
                                {segunda_prob:.1f}%
                            </div>
                        </div>

                        <div style="
                            flex: 1;
                            min-width: 190px;
                            padding: 14px;
                            border-radius: 10px;
                            background: white;
                            border: 1px solid #e3ddd4;
                        ">
                            <div style="font-size: 11px; opacity: .65;">
                                DIFERENCIA
                            </div>

                            <div style="
                                font-size: 19px;
                                font-weight: 700;
                                margin-top: 5px;
                            ">
                                {diferencia:.1f}
                            </div>

                            <div style="font-size: 15px;">
                                puntos porcentuales
                            </div>
                        </div>

                    </div>

                    <div style="
                        margin-top: 18px;
                        padding-top: 15px;
                        border-top: 1px solid #e3ddd4;
                    ">
                        <b>{nivel_prediccion}</b>
                        <br>
                        <span style="font-size: 13px;">
                            {descripcion_prediccion}
                        </span>
                    </div>

                </div>
                """
            )

            mostrar_html(
                """
                <div style="
                    margin-top: 26px;
                    margin-bottom: 14px;
                ">
                    <div style="
                        font-size: 12px;
                        letter-spacing: 1.5px;
                        font-weight: 700;
                    ">
                        DISTRIBUCION DE LA PREDICCION
                    </div>

                    <div style="
                        font-size: 13px;
                        opacity: .7;
                        margin-top: 4px;
                    ">
                        Valores generados por el modelo para cada clase.
                    </div>
                </div>
                """
            )

            barras = ""

            for clase, porcentaje in resultados_ordenados:

                ancho = max(0, min(100, porcentaje))

                barras = (
                    barras
                    + f"""
                    <div style="margin-bottom: 16px;">

                        <div style="
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            margin-bottom: 6px;
                        ">

                            <span style="
                                font-size: 14px;
                                font-weight: 600;
                            ">
                                {clase}
                            </span>

                            <span style="
                                font-size: 14px;
                                font-weight: 700;
                            ">
                                {porcentaje:.1f}%
                            </span>

                        </div>

                        <div style="
                            width: 100%;
                            height: 11px;
                            background: #e7e2da;
                            border-radius: 20px;
                            overflow: hidden;
                        ">

<div style="
                            width: {ancho:.2f}%;
                            height: 100%;
                            background: {colores_clase.get(clase, '#587052')};
                            border-radius: 20px;
                        "></div>

                        </div>

                    </div>
                    """
                )

            mostrar_html(barras)

# ============================================================
# BANDA: ORIENTACION Y MANEJO PREVENTIVO
# ============================================================

if "diagnostico" in st.session_state:

    recomendaciones = st.session_state["recomendaciones"]

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
        tarjetas = (
            tarjetas
            + f"""
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
                    {formatear_markdown(texto)}
                </div>

            </div>
            """
        )

    mostrar_html(
        f"""
        <div class="pl-reco-grid">
            {tarjetas}
        </div>
        """
    )

    mostrar_html(
        f"""
        <div class="pl-reco pl-reco-conclusion">

            <div class="pl-reco-top">

                <div class="pl-reco-num">
                    06
                </div>

                <div class="pl-reco-titulo">
                    Conclusión técnica
                </div>

            </div>

            <div class="pl-reco-texto">
                {formatear_markdown(recomendaciones["conclusion"])}
            </div>

        </div>
        """
    )

    pdf = crear_pdf(
        st.session_state["diagnostico"],
        st.session_state["confianza"],
        recomendaciones,
        st.session_state.get("probabilidades"),
    )

    mostrar_html("<div style='height:20px'></div>")

    centro_izquierda, centro_boton, centro_derecha = st.columns(
        [1, 4, 1],
        gap="medium",
    )

    with centro_boton:
        st.download_button(
            "📄 Descargar informe PDF",
            data=pdf,
            file_name="diagnostico_agrodetect.pdf",
            mime="application/pdf",
            width="stretch",
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
