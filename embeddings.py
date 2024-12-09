import os
import openai
import json
from PyPDF2 import PdfReader

# Carga la clave API de OpenAI
from dotenv import load_dotenv
#load_dotenv()
openai.api_key = "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"

# Función para leer documentos PDF
def leer_documento(ruta):
    reader = PdfReader(ruta)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

# Generar embeddings usando OpenAI
def generar_embeddings(texto):
    respuesta = openai.Embedding.create(
        input=texto,
        model="text-embedding-ada-002"
    )
    return respuesta['data'][0]['embedding']



# Procesar documentos
def procesar_documentos(directorio):
    documentos = []
    embeddings = []

    for archivo in os.listdir(directorio):
        ruta = os.path.join(directorio, archivo)
        if archivo.endswith(".pdf"):
            texto = leer_documento(ruta)
            documentos.append(texto)
            embeddings.append(generar_embeddings(texto))

    # Guardar embeddings en un archivo JSON
    with open("embeddings.json", "w") as f:
        json.dump({"documentos": documentos, "embeddings": embeddings}, f)

    print("Documentos procesados y embeddings generados.")

# Procesar los documentos del directorio
procesar_documentos("documents/")
