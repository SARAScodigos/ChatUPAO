from flask import Flask, request, jsonify, render_template
import openai
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

# Configurar OpenAI y Flask
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

# Cargar embeddings y documentos
with open("embeddings.json", "r") as f:
    data = json.load(f)
    documentos = data['documentos']
    embeddings = np.array(data['embeddings'])


# Convertir tablas en texto plano a HTML
def convertir_tabla_a_html(texto):
    """
    Convierte una tabla en texto plano (separada por |) a una tabla en HTML.
    """
    lineas = texto.strip().split("\n")
    tabla_html = "<table class='table table-striped table-bordered table-hover'>"
    for i, linea in enumerate(lineas):  # Usar enumerate para obtener el índice
        if "|" in linea and not all(celda.strip("-") == "" for celda in linea.split("|")):  # Detectar líneas con formato de tabla
            celdas = [celda.strip() for celda in linea.split("|") if celda.strip()]
            if i == 0:  # Primera fila como encabezado
                fila = "<tr>" + "".join(f"<th>{celda.strip()}</th>" for celda in celdas) + "</tr>"
            else:  # Otras filas como datos
                fila = "<tr>" + "".join(f"<td>{celda.strip()}</td>" for celda in celdas) + "</tr>"
            tabla_html += fila
    tabla_html += "</table>"
    return tabla_html


# Convertir listas a HTML



# Buscar contexto más relevante
def buscar_contexto(pregunta, embeddings, documentos):
    # Generar embedding para la pregunta
    respuesta = openai.Embedding.create(
        input=pregunta,
        model="text-embedding-ada-002"
    )
    pregunta_embedding = np.array(respuesta['data'][0]['embedding'])

    # Calcular similitud coseno
    similitudes = cosine_similarity([pregunta_embedding], embeddings)[0]
    indice = np.argmax(similitudes)
    return documentos[indice]


# Ruta principal para la interfaz gráfica
@app.route('/')
def index():
    return render_template("test.html")


# Ruta para procesar preguntas
@app.route('/preguntar', methods=['POST'])
def preguntar():
    data = request.get_json()
    pregunta = data.get('pregunta')

    if not pregunta:
        return jsonify({"error": "No se proporcionó una pregunta"}), 400

    # Buscar contexto relevante
    contexto = buscar_contexto(pregunta, embeddings, documentos)

    # Generar respuesta con GPT-3.5-turbo
    respuesta_completa = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en guías de laboratorio. Y responde de manera coherente a los saludos"},
            {"role": "user", "content": f"Contexto: {contexto}\nPregunta: {pregunta}"}
        ],
        max_tokens=250
    )

    # Obtener solo el contenido de la respuesta
    respuesta = respuesta_completa['choices'][0]['message']['content']

    # Procesar tablas y listas
    if "|" in respuesta:  # Detectar si la respuesta incluye una tabla
        respuesta = convertir_tabla_a_html(respuesta)
    

    return jsonify({"respuesta": respuesta})


if __name__ == '__main__':
    app.run(port=5000)
