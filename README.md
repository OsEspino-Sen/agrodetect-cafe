# 🌿 AgroDetect Café

### Servicio Web para la Detección de Enfermedades en Hojas de Café mediante Inteligencia Artificial

AgroDetect Café es una aplicación web desarrollada con Python y Streamlit que permite analizar imágenes de hojas de café mediante un modelo de Inteligencia Artificial y determinar la condición o enfermedad detectada.

El sistema combina un modelo de clasificación de imágenes desarrollado con TensorFlow/Keras con la API de Groq para generar orientación técnica, recomendaciones de manejo preventivo, buenas prácticas agrícolas y acciones de monitoreo y seguimiento.

---

## 🎯 Objetivo

Desarrollar un Servicio Web basado en principios de Computación en la Nube que permita detectar enfermedades en hojas de café mediante Inteligencia Artificial y proporcionar recomendaciones técnicas para su manejo preventivo.

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

---

## 🌱 Dataset

Para el desarrollo del modelo se utilizó un conjunto de imágenes de hojas de café proporcionado para el proyecto académico.

Durante el procesamiento del dataset se trabajó con imágenes correspondientes a diferentes condiciones, incluyendo:

* Hojas saludables.
* Roya.
* Minador de la hoja.
* Phoma.

El dataset fue utilizado durante la etapa de desarrollo y entrenamiento del modelo en Google Colab.

El modelo entrenado posteriormente fue exportado como:

```text
modelo_cafe.keras
```

para ser utilizado en la aplicación web.

---

## 🤖 Integración con la API de Groq

La API de Groq constituye un componente obligatorio del proyecto y se utiliza para complementar el diagnóstico generado por el modelo de visión artificial.

Una vez obtenida la predicción, la aplicación utiliza la enfermedad o condición detectada como contexto para solicitar a Groq orientación técnica.

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
                    GitHub
                       │
                       ▼
             Streamlit Community
                    Cloud
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
         Streamlit          TensorFlow
         Web App              / Keras
              │
              │ diagnóstico
              ▼
           Groq API
              │
              ▼
    Recomendaciones técnicas
```

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