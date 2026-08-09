# 🌿 AgroDetect Café

### Servicio Web para la Detección de Enfermedades en Hojas de Café mediante Inteligencia Artificial

AgroDetect Café es una aplicación web desarrollada con Python y Streamlit que permite analizar imágenes de hojas de café mediante un modelo de Inteligencia Artificial y determinar la condición o enfermedad detectada.

El sistema combina un modelo de clasificación de imágenes desarrollado con TensorFlow/Keras con la API de Groq para generar orientación técnica, recomendaciones de manejo preventivo, buenas prácticas agrícolas y acciones de monitoreo y seguimiento.

---

## 🎯 Objetivo

Desarrollar un Servicio Web basado en principios de Computación en la Nube que permita clasificar imágenes de hojas de café dentro de las categorías aprendidas por el modelo mediante Inteligencia Artificial y proporcionar recomendaciones técnicas para su manejo preventivo.

La aplicación permite al usuario:

* Cargar una imagen de una hoja de café.
* Visualizar la imagen seleccionada.
* Analizar la imagen mediante un modelo de Inteligencia Artificial.
* Obtener la enfermedad o condición detectada.
* Visualizar el porcentaje de confianza de la predicción.
* Obtener orientación técnica generada mediante la API de Groq.
* Consultar recomendaciones de manejo preventivo.
* Consultar buenas prácticas para el cuidado del cultivo.
* Consultar acciones de monitoreo y seguimiento.

---

## 🌐 Aplicación desplegada

La aplicación se encuentra disponible públicamente en:

**[🚀 Abrir AgroDetect Café](https://agrodetectordecafe-oscarespino.streamlit.app/)**

El Servicio Web se encuentra desplegado mediante **Streamlit Community Cloud**, permitiendo el acceso a la aplicación a través de Internet sin necesidad de ejecutar el proyecto localmente.

---

## 📂 Repositorio

El código fuente completo del proyecto se encuentra disponible en GitHub:

**[📁 Repositorio AgroDetect Café](https://github.com/OsEspino-Sen/agrodetect-cafe)**

Repositorio:

`https://github.com/OsEspino-Sen/agrodetect-cafe`

---

## ✨ Características principales

* 📷 Carga de imágenes de hojas de café.
* 🖼️ Visualización de la imagen seleccionada.
* 🧠 Clasificación mediante Inteligencia Artificial.
* 📊 Porcentaje de confianza de la predicción.
* 📈 Distribución de probabilidades de las cuatro clases.
* 🔎 Comparación entre la primera y segunda predicción.
* 📊 Diferencia porcentual entre las principales posibilidades.
* ⚠️ Indicador de competencia entre clases para interpretar predicciones con valores cercanos.
* 🌱 Identificación de la condición o enfermedad detectada.
* 🤖 Integración con la API de Groq.
* 📋 Descripción y diferenciación de la enfermedad.
* 🌿 Recomendaciones de manejo agronómico preventivo.
* 👨‍🌾 Recomendación de consulta con un técnico agrícola.
* 🔎 Monitoreo y seguimiento.
* 📝 Registro y trazabilidad.
* ☁️ Despliegue en Streamlit Community Cloud.
* 🔐 Manejo seguro de la API Key mediante Secrets.

---

## 🛠️ Tecnologías utilizadas

| Tecnología                | Uso                                                          |
| ------------------------- | ------------------------------------------------------------ |
| Python 3.11               | Lenguaje de programación                                     |
| TensorFlow / Keras        | Desarrollo y ejecución del modelo de Inteligencia Artificial |
| NumPy                     | Procesamiento numérico                                       |
| Pillow                    | Procesamiento de imágenes                                    |
| Streamlit                 | Desarrollo de la interfaz web                                |
| Groq API                  | Generación de orientación técnica mediante IA generativa     |
| Git                       | Control de versiones                                         |
| GitHub                    | Repositorio y gestión del código fuente                      |
| Streamlit Community Cloud | Despliegue del Servicio Web                                  |
| ReportLab                 | Generación de documentos PDF                                 |

---

## 🏗️ Arquitectura del sistema

El sistema está compuesto por una aplicación web desarrollada con Streamlit, un modelo de clasificación de imágenes desarrollado con TensorFlow/Keras y la API de Groq para la generación de orientación técnica.

```text
                         USUARIO
                            │
                            ▼
                  ┌───────────────────┐
                  │     Streamlit     │
                  │   Interfaz Web    │
                  └─────────┬─────────┘
                            │
                     Imagen de hoja
                            │
                            ▼
                  ┌───────────────────┐
                  │ Modelo TensorFlow │
                  │      / Keras      │
                  └─────────┬─────────┘
                            │
                  Predicción + confianza
                            │
                            ▼
                  ┌───────────────────┐
                  │     API Groq      │
                  │ IA generativa     │
                  └─────────┬─────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │ Orientación técnica        │
              │                            │
              │ • Diferenciación           │
              │ • Manejo preventivo        │
              │ • Consulta técnica         │
              │ • Monitoreo                │
              │ • Registro                 │
              └────────────────────────────┘
```

---

## 🔄 Flujo de funcionamiento

El funcionamiento general del sistema es el siguiente:

1. El usuario ingresa al Servicio Web.
2. El usuario selecciona una imagen de una hoja de café.
3. Streamlit recibe y muestra la imagen.
4. La imagen es procesada para adaptarla al formato requerido por el modelo.
5. El modelo TensorFlow/Keras realiza la clasificación.
6. El sistema obtiene la clase predicha.
7. Se calcula y muestra el porcentaje de confianza asociado a la predicción.
8. La condición o enfermedad detectada se utiliza como contexto para la solicitud a la API de Groq.
9. Groq genera la orientación técnica correspondiente.
10. Streamlit presenta los resultados al usuario.
11. El usuario puede consultar las recomendaciones de manejo preventivo, monitoreo y seguimiento.

El flujo puede resumirse como:

```text
Imagen
   │
   ▼
Procesamiento
   │
   ▼
Modelo IA
   │
   ├──► Enfermedad / condición
   │
   └──► Porcentaje de confianza
              │
              ▼
           API Groq
              │
              ▼
    Orientación técnica
              │
              ▼
          Usuario
```

---

## 🧠 Modelo de Inteligencia Artificial

El sistema utiliza un modelo de clasificación de imágenes desarrollado con **TensorFlow/Keras**.

El modelo fue entrenado utilizando imágenes correspondientes a diferentes condiciones de hojas de café y posteriormente exportado en formato `.keras`.

El archivo utilizado por la aplicación es:

```text
modelo_cafe.keras
```

Durante la inferencia, la imagen cargada por el usuario es procesada y enviada al modelo.

El modelo genera probabilidades para las clases disponibles. La aplicación selecciona la clase con mayor probabilidad y muestra el diagnóstico junto con el porcentaje de confianza correspondiente.

Las clases utilizadas por el modelo se encuentran definidas en:

```text
class_names.json
```

### Rendimiento durante la evaluación

Durante la evaluación realizada sobre las imágenes disponibles del
dataset se obtuvo:

- Accuracy: **83.44%**
- Clases evaluadas: **4**
- Imágenes evaluadas: **1,800**

La matriz de confusión y el reporte de clasificación mostraron
diferencias de rendimiento entre las clases. Por esta razón, el
porcentaje mostrado por el modelo debe interpretarse como una
probabilidad de clasificación y no como una confirmación absoluta
del diagnóstico.

### Interpretación de la confianza

El porcentaje mostrado corresponde a la probabilidad producida por el
clasificador para la clase seleccionada.

Una confianza elevada **no garantiza que la enfermedad esté realmente
presente**, especialmente cuando la imagen corresponde a una condición
que no pertenece a las clases utilizadas durante el entrenamiento.

La aplicación también muestra la distribución de probabilidades entre
las cuatro clases para permitir una interpretación más transparente de
la predicción.

---

## 🌱 Dataset

El modelo fue entrenado con 1,800 imágenes de hojas de café distribuidas
en cuatro clases:

| Clase | Imágenes |
|---|---:|
| Healthy | 400 |
| Minador | 500 |
| Phoma | 500 |
| Roya | 400 |

Las clases corresponden exclusivamente a las categorías disponibles
en el dataset utilizado para entrenar el modelo.

Por lo tanto, el sistema **no puede identificar de forma confiable
enfermedades que no formen parte de estas cuatro clases**. Una
enfermedad externa al conjunto de entrenamiento puede ser clasificada
incorrectamente como alguna de las clases conocidas.

---

## 🤖 Integración con la API de Groq

La aplicación utiliza la **API de Groq** como servicio externo de
Inteligencia Artificial generativa.

La API recibe como contexto:

- La clase principal predicha.
- El porcentaje de confianza.
- La distribución de probabilidades entre las clases.

A partir de esta información, el modelo generativo produce orientación
técnica estructurada para el usuario.

La integración se realiza mediante la API compatible con el formato
OpenAI proporcionado por GroqCloud. La clave utilizada corresponde a
una credencial de **Groq** y no a una API Key de OpenAI.

El modelo puede llamarse `openai/gpt-oss-120b` dentro de Groq y seguir
siendo una solicitud hecha a Groq. La API Key sigue siendo
`GROQ_API_KEY`.

La información generada incluye:

### 01. Diferenciación a simple vista

Información que permite comprender características visuales de la condición detectada y diferenciarla de otras posibles afectaciones.

### 02. Manejo agronómico preventivo

Recomendaciones relacionadas con prácticas preventivas y manejo del cultivo.

### 03. Consulta a un técnico

Orientación sobre situaciones en las que es recomendable consultar a un profesional agrícola.

### 04. Monitoreo y seguimiento

Recomendaciones para realizar inspecciones periódicas y observar la evolución de la condición.

### 05. Registro y trazabilidad

Recomendaciones relacionadas con el registro de fechas, ubicación, evolución y medidas aplicadas.

La integración permite combinar:

```text
Modelo de visión artificial
          +
    API de Groq
          =
Diagnóstico + orientación técnica
```

---

## 🔐 Seguridad de la API

La clave de acceso a Groq **no se almacena directamente en el código fuente ni se publica en GitHub**.

En el entorno local se utiliza:

```text
.streamlit/secrets.toml
```

y en Streamlit Community Cloud se utiliza el sistema de **Secrets** de la plataforma.

La aplicación accede a la clave mediante:

```python
st.secrets["GROQ_API_KEY"]
```

La clave utilizada para acceder a la API no forma parte del repositorio público.

El archivo:

```text
.streamlit/secrets.toml
```

se encuentra excluido mediante `.gitignore`.

---

## ☁️ Computación en la Nube

El proyecto implementa un enfoque de Computación en la Nube mediante diferentes servicios.

### GitHub

GitHub se utiliza como repositorio para:

* Almacenar el código fuente.
* Controlar las versiones del proyecto.
* Gestionar los archivos de la aplicación.
* Facilitar el despliegue del proyecto.

### Streamlit Community Cloud

Streamlit Community Cloud se utiliza para desplegar la aplicación y proporcionar una URL pública accesible mediante Internet.

### Groq API

Groq se utiliza como servicio externo de Inteligencia Artificial generativa para producir orientación técnica y recomendaciones relacionadas con la condición detectada.

### Arquitectura en la nube

```text
                         USUARIO
                            │
                            ▼
                ┌─────────────────────┐
                │ Streamlit Community │
                │       Cloud         │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Aplicación       │
                │     Streamlit       │
                │                     │
                │  ┌───────────────┐  │
                │  │ TensorFlow /  │  │
                │  │     Keras     │  │
                │  └───────┬───────┘  │
                └──────────┼──────────┘
                           │
                    Predicción
                           │
                           ▼
                    ┌────────────┐
                    │  Groq API  │
                    └─────┬──────┘
                          │
                          ▼
                Orientación técnica
                          │
                          ▼
                        USUARIO
```

TensorFlow/Keras se ejecuta como parte de la aplicación desplegada en
Streamlit Community Cloud, mientras que Groq funciona como un servicio
externo de IA generativa.

Gracias a esta arquitectura, el usuario puede acceder al sistema desde Internet sin necesidad de ejecutar el modelo o la aplicación directamente en su computadora.

---

## 📁 Estructura del proyecto

```text
agrodetect-cafe/
│
├── .streamlit/
│   └── config.toml
│
├── app.py
├── modelo_cafe.keras
├── class_names.json
├── requirements.txt
├── README.md
└── .gitignore
```

### Descripción de archivos

| Archivo                  | Descripción                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| `app.py`                 | Código principal de la aplicación web desarrollada con Streamlit |
| `modelo_cafe.keras`      | Modelo de clasificación de imágenes                              |
| `class_names.json`       | Clases utilizadas por el modelo                                  |
| `requirements.txt`       | Dependencias necesarias para ejecutar el proyecto                |
| `.streamlit/config.toml` | Configuración de la aplicación Streamlit                         |
| `.gitignore`             | Archivos y directorios excluidos del control de versiones        |
| `README.md`              | Documentación del proyecto                                       |

---

## 📦 Dependencias

Las principales dependencias del proyecto son:

```text
streamlit
tensorflow
numpy
pillow
groq
reportlab
```

Las dependencias se encuentran especificadas en:

```text
requirements.txt
```

---

## 💻 Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/OsEspino-Sen/agrodetect-cafe.git
```

Entrar al directorio:

```bash
cd agrodetect-cafe
```

### 2. Crear un entorno virtual

Se recomienda utilizar Python 3.11.

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar la API de Groq

Crear:

```text
.streamlit/secrets.toml
```

y agregar:

```toml
GROQ_API_KEY = "TU_CLAVE_DE_GROQ"
```

No se debe publicar este archivo ni compartir la clave.

### 6. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible normalmente en:

```text
http://localhost:8501
```

---

## ☁️ Despliegue en Streamlit Community Cloud

El proyecto se encuentra desplegado mediante Streamlit Community Cloud.

El proceso utilizado fue:

1. Crear el repositorio en GitHub.
2. Subir el código fuente.
3. Incluir el modelo `modelo_cafe.keras`.
4. Configurar `requirements.txt`.
5. Conectar el repositorio con Streamlit Community Cloud.
6. Seleccionar la rama `main`.
7. Seleccionar `app.py` como archivo principal.
8. Configurar `GROQ_API_KEY` mediante Streamlit Secrets.
9. Ejecutar el despliegue.
10. Verificar la aplicación mediante la URL pública.

### URL pública

**[https://agrodetectordecafe-oscarespino.streamlit.app/](https://agrodetectordecafe-oscarespino.streamlit.app/)**

---

## 🖥️ Uso de la aplicación

Para utilizar AgroDetect Café:

1. Ingresar a la aplicación web.
2. Seleccionar una imagen de una hoja de café.
3. Verificar la imagen seleccionada.
4. Presionar el botón de análisis.
5. Esperar el resultado del modelo.
6. Revisar la condición o enfermedad detectada.
7. Revisar el porcentaje de confianza.
8. Consultar la orientación técnica generada por Groq.
9. Revisar las recomendaciones de manejo preventivo.
10. Revisar las recomendaciones de monitoreo y seguimiento.

---

## 📊 Resultados

El sistema permite realizar el flujo completo:

```text
Imagen
   ↓
Procesamiento
   ↓
Modelo de Inteligencia Artificial
   ↓
Enfermedad / condición detectada
   ↓
Porcentaje de confianza
   ↓
API de Groq
   ↓
Orientación técnica
   ↓
Recomendaciones preventivas
```

Durante las pruebas, la aplicación desplegada fue capaz de recibir imágenes de hojas de café, realizar la clasificación mediante el modelo de Inteligencia Artificial y presentar el resultado al usuario.

Posteriormente, la API de Groq genera orientación técnica relacionada con el diagnóstico obtenido.

---

## ⚠️ Alcance del modelo

AgroDetect Café es un sistema de clasificación desarrollado para las
cuatro clases presentes en el dataset:

- Healthy
- Minador
- Phoma
- Roya

El modelo no fue entrenado con todas las enfermedades que pueden
afectar al cultivo de café.

Por esta razón, si una hoja presenta una enfermedad diferente a las
clases disponibles, el modelo puede asignarla incorrectamente a una de
las categorías conocidas.

El resultado debe utilizarse como herramienta de apoyo y no como
diagnóstico fitopatológico definitivo.

---

## ⚠️ Limitaciones y consideraciones

Los resultados proporcionados por el sistema corresponden a predicciones realizadas mediante un modelo de Inteligencia Artificial.

La precisión puede verse afectada por factores como:

* Calidad de la imagen.
* Iluminación.
* Enfoque de la fotografía.
* Ángulo de la hoja.
* Similitud visual entre diferentes enfermedades.
* Condiciones reales del cultivo.

Las recomendaciones generadas mediante Inteligencia Artificial deben considerarse como orientación y no sustituyen un diagnóstico profesional.

En casos de alta severidad, incertidumbre o propagación de la enfermedad, se recomienda consultar a un técnico o profesional agrícola.

---

## 🎓 Contexto académico

Este proyecto fue desarrollado como parte de la asignatura:

**Computación en la Nube**

### Objetivo académico

Aplicar conceptos de:

* Computación en la Nube.
* Inteligencia Artificial.
* Aprendizaje automático.
* Desarrollo de aplicaciones web.
* APIs.
* Control de versiones.
* Despliegue de servicios web.
* Manejo seguro de credenciales.

---

## 👨‍💻 Autor

**Nombre:** Oscar Noe Espino Aguirre
**Carrera:** Ingeniería en Sistemas
**Número de cuenta:** 202310110465

### Proyecto

**AgroDetect Café — Servicio Web para la Detección de Enfermedades en Hojas de Café mediante Inteligencia Artificial**

---

## 📄 Licencia

Proyecto desarrollado con fines académicos.