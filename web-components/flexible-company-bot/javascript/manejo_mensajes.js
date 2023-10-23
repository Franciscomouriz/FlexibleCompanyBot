import { agregarMensaje, agregarMensajeCarga, eliminarMensajeCarga } from './manejo_gui.js';

// Función para indicar que el bot está escribiendo
function indicarBotEscribiendo(conversacion) {
    try {
        agregarMensajeCarga(conversacion)
    }
    catch (error) {
        console.error('Error al indicar que el bot está escribiendo:', error);
        agregarMensaje(conversacion, 'No se pudo indicar que el bot está escribiendo.', 'error');
    }
}

// Función que elimina el mensaje de carga
function acabarBotEscribiendo(conversacion) {
    try {
        eliminarMensajeCarga(conversacion);
    }
    catch (error) {
        console.error('Error al eliminar mensaje de carga:', error);
        agregarMensaje(conversacion, 'No se pudo eliminar el mensaje de carga.', 'error');
    }
}

function respuestaBot(respuesta, conversacion) {
    try{
        console.log('Respuesta del bot:', respuesta);
        // Se elimina la animación de que el bot está escribiendo
        acabarBotEscribiendo(conversacion);
        // Se añade la respuesta del bot a la conversación
        agregarMensaje(conversacion, respuesta, "bot");
    }
    catch (error) {
        console.error('Error al obtener respuesta del bot:', error);
        agregarMensaje(conversacion, 'No se pudo obtener la respuesta del bot.', 'error');
    }
}
    

function enviarPreguntaBot(pregunta, conversacion) {
    let respuesta_texto = null;
    // Se añade la animación de que el bot está escribiendo
    indicarBotEscribiendo(conversacion);
    // Se envía la pregunta al bot
    const promesa = new Promise((resolve, reject) => {
        $.post({
            // Se envía una petición POST a la URL /search
            // Se envía la pregunta en el cuerpo de la petición
            url: "http://127.0.0.1:8000/search",
            data: JSON.stringify({ query: pregunta }),
            contentType: "application/json; charset=utf-8",
            success: function (respuesta) {
                // Se obtiene la respuesta del bot
                const key = Object.keys(respuesta);
                respuesta_texto = respuesta[key];
                // Se escribe la respuesta del bot en la conversación
                respuestaBot(respuesta_texto, conversacion)
                resolve();
            },
            error: function (error) {
                console.error('Error al enviar pregunta al bot:', error);
                reject(error);
            }
        });
    });

    return promesa.catch(error => {
        console.error('Error al enviar pregunta al bot:', error);
        acabarBotEscribiendo(conversacion);
        throw error;
    });
}

export { enviarPreguntaBot };
