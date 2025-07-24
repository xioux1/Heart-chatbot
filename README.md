# Chatbot con Streamlit y ChatGPT

Este proyecto es un ejemplo de chatbot que combina **Streamlit** con **ChatGPT** (modelo ``gpt-3.5-turbo``) para responder preguntas basadas en los datos de un archivo CSV. Para simplificar la demostración se incluye un conjunto de datos de ejemplo (``heart.csv``) que se carga automáticamente y no existe la opción de subir archivos personalizados.

## Requisitos de instalación

Se recomienda usar un entorno virtual de **Python 3.10 o 3.11** (las versiones más nuevas
pueden no ser compatibles con todas las dependencias).
Instale las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

Configure la variable de entorno `OPENAI_API_KEY` con su clave de API de OpenAI:

```bash
export OPENAI_API_KEY="sk-..."
```


## Ejecución

Inicie la aplicación con:

```bash
streamlit run model.py
```

Aparecerá una interfaz tipo chat que utiliza automáticamente el archivo ``heart.csv`` incluido en el repositorio. El sistema genera un índice con FAISS y podrás conversar manteniendo el contexto de las preguntas previas para obtener respuestas basadas en la información del CSV.

El índice se crea únicamente para la sesión actual y no se guarda en disco. Si reinicia la aplicación, se generará nuevamente a partir del dataset predefinido.

## Créditos y enlaces útiles

- [API de OpenAI](https://platform.openai.com/docs/api-reference)

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/94ea0b5f-bab1-4fee-871c-c0eb7b291c8b" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/d6a569f3-dc92-441f-bcd1-2a5be92752d4" />

