# Chatbot con Streamlit y Llama-2

Este proyecto es un ejemplo de chatbot que combina **Streamlit** con el modelo **Llama-2** para responder preguntas basadas en los datos de un archivo CSV. El usuario puede subir su propio conjunto de datos y obtener respuestas contextualizadas.

## Requisitos de instalación

Se recomienda usar un entorno virtual de Python. Instale las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

Además, es necesario descargar el modelo `llama-2-7b-chat.ggmlv3.q4_0.bin` y colocarlo en la carpeta `models` (consulte `models/llama-2-7b-chat.ggmlv3.q4_0.bin.md` para más detalles).

## Ejecución

Inicie la aplicación con:

```bash
streamlit run model.py
```

Aparecerá una interfaz web donde podrá cargar un archivo CSV desde la barra lateral. Tras la carga, el sistema generará un índice con FAISS y podrá escribir preguntas en el cuadro de texto para obtener respuestas basadas en la información del CSV.

## Créditos y enlaces útiles

- [Modelo Llama-2-7B-Chat-GGML](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main)
- Inspirado en el repositorio [ThisIs-Developer/Llama-2-GGML-CSV-Chatbot](https://github.com/ThisIs-Developer/Llama-2-GGML-CSV-Chatbot)
