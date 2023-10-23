import { bloquearBotonEnviar, desbloquearBotonEnviar, agregarMensaje, limpiarEntrada, vaciarConversacion} from './manejo_gui.js';
import { enviarPreguntaBot } from './manejo_mensajes.js';

// Función para manejar el evento de enviar mensaje
function enviarMensajeUsuario(mensajeInput, conversacion, event) {
    try {
        const mensaje = $(mensajeInput).val().trim();
        if (mensaje !== '') {
            agregarMensaje(conversacion, mensaje, "usuario");
            limpiarEntrada(mensajeInput);
            bloquearBotonEnviar();
            enviarPreguntaBot(mensaje, conversacion).then(() => {
                console.log("Fin de enviar mensaje");
                desbloquearBotonEnviar();
            }).catch(error => {
                desbloquearBotonEnviar();
                console.error('Error al enviar mensaje al bot:', error);
                agregarMensaje(conversacion, 'No se pudo enviar el mensaje al bot. Inténtalo de nuevo más tarde.', 'error');
            });
        }
    }
    catch (error) {
        console.error('Error al enviar mensaje:', error);
        agregarMensaje(conversacion, 'No se pudo enviar el mensaje al bot. Inténtalo de nuevo más tarde.', 'error');
    }
    return false;
}



// Función para manejar el evento de reiniciar conversación
function reiniciarConversacion(conversacion, mensajeInput) {
    try {
        vaciarConversacion();
        limpiarEntrada(mensajeInput);
    }
    catch (error) {
        console.error('Error al reiniciar conversación:', error);
        agregarMensaje(conversacion, 'No se pudo reiniciar la conversación. Inténtalo de nuevo más tarde.', 'error');
    }
}

export { reiniciarConversacion, enviarMensajeUsuario };