# Chatbot con Streamlit y Phi-3 Mini

Este proyecto es un ejemplo de chatbot que combina **Streamlit** con el modelo **Phi-3 Mini 3.8B** para responder preguntas basadas en los datos de un archivo CSV. El usuario puede subir su propio conjunto de datos y obtener respuestas contextualizadas.

## Requisitos de instalación

Se recomienda usar un entorno virtual de **Python 3.10 o 3.11** (las versiones más nuevas,
como Python 3.13, no son compatibles actualmente con `ctransformers`).
Instale las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

Además, es necesario descargar el modelo `Phi-3-mini-4k-instruct-q4.gguf` y colocarlo en la carpeta `models` (consulte `models/Phi-3-mini-4k-instruct-q4.gguf.md` para más detalles).

### Descarga desde la línea de comandos

Puede utilizar la utilidad `huggingface-cli` para descargar directamente el archivo GGUF:

```bash
pip install huggingface-hub>=0.17.1
huggingface-cli login
huggingface-cli download microsoft/Phi-3-mini-4k-instruct-gguf \
    Phi-3-mini-4k-instruct-q4.gguf \
    --local-dir ./models --local-dir-use-symlinks False
```

El modelo se guardará en la carpeta `models`.

## Ejecución

Inicie la aplicación con:

```bash
streamlit run model.py
```

Aparecerá una interfaz web donde podrá cargar un archivo CSV desde la barra lateral. Tras la carga, el sistema generará un índice con FAISS y podrá escribir preguntas en el cuadro de texto para obtener respuestas basadas en la información del CSV.

El índice se crea únicamente para la sesión actual y no se guarda en disco. Si reinicia la aplicación o carga un nuevo CSV, se generará un índice temporal nuevo.

## Créditos y enlaces útiles

- [Modelo Phi-3 Mini 3.8B](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-GGUF)
- Inspirado en el repositorio [ThisIs-Developer/Llama-2-GGML-CSV-Chatbot](https://github.com/ThisIs-Developer/Llama-2-GGML-CSV-Chatbot)
