// Función que bloquea el botón de enviar mensaje
function bloquearBotonEnviar(){
    // Se encuentra el botón con la clase CSS enviarActivado
    document.getElementById("enviar").disabled = true;
    document.getElementById("enviar").classList.add("enviarDesactivado");
}

// Función que desbloquea el botón de enviar mensaje
function desbloquearBotonEnviar(){
    document.getElementById("enviar").disabled = false;
    document.getElementById("enviar").classList.remove("enviarDesactivado");
}

// Función para agregar un nuevo mensaje a la conversación
// tipoMensaje puede ser usuario, bot o error
// mensaje es opcional
function agregarMensaje(conversacion, mensaje, tipoMensaje) {
    const $mensajeElement = $('<div>').addClass('mensaje-container');
    switch (tipoMensaje) {
        case 'usuario':
            $mensajeElement.append($('<span>').addClass('mensaje-usuario').text(mensaje));
            break;
        case 'bot':
            $mensajeElement.append($('<span>').addClass('mensaje-bot').text(mensaje));
            break;
        case 'error':
            $mensajeElement.append($('<span>').addClass('mensaje-error').text(mensaje));
            break;
        default:
            console.error('Tipo de mensaje no reconocido:', tipoMensaje);
            return;
    }
    $(conversacion).append($mensajeElement);
}

// Función para agregar mensaje de carga
function agregarMensajeCarga(conversacion) {
    // Se crea un mensaje con una rueda de carga
    const $mensajeElement = $('<div>').addClass('mensaje-container');
    $mensajeElement.append($('<div>').addClass('loader'));
    $(conversacion).append($mensajeElement);
}

// Función para eliminar mensaje de carga
function eliminarMensajeCarga(conversacion) {
    $(conversacion).find('.loader').parent().remove();
}

// Función para limpiar la entrada del usuario
function limpiarEntrada(mensajeInput) {
    $(mensajeInput).val('');
}

// Función para vaciar la conversacion
function vaciarConversacion(conversacion) {
    $(conversacion).empty();
}

export { bloquearBotonEnviar, desbloquearBotonEnviar, agregarMensaje, limpiarEntrada, agregarMensajeCarga, eliminarMensajeCarga, vaciarConversacion };