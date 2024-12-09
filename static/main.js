// Evento para enviar la pregunta al presionar "Enter"
document.getElementById("pregunta").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevenir el salto de línea
        hacerPregunta();
    }
});

async function hacerPregunta() {
    const pregunta = document.getElementById("pregunta").value.trim();
    if (!pregunta) return; // No hacer nada si el campo está vacío

    // Mostrar la pregunta en el historial
    const historial = document.getElementById("historial");
    historial.innerHTML += `<p><strong>Alumno:</strong> ${pregunta}</p>`;

    // Enviar la pregunta al servidor
    const response = await fetch('/preguntar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pregunta })
    });

    // Procesar la respuesta del servidor
    const data = await response.json();
    const respuesta = data.respuesta || data.error;

    // Añadir la respuesta al historial
    historial.innerHTML += `<p><strong>Asistente:</strong> ${respuesta}</p>`;

    // Renderizar las fórmulas matemáticas
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);

    // Limpiar el campo de texto
    document.getElementById("pregunta").value = "";

    // Desplazar automáticamente el historial hacia abajo
    historial.scrollTop = historial.scrollHeight;
}