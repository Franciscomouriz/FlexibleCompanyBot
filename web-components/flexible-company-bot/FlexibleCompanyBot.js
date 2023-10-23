import {enviarMensajeUsuario, reiniciarConversacion} from './javascript/controlador.js';

class FlexibleCompanyBot extends HTMLElement {
    constructor() {
        super();
    }

    //Método para obtener el HTML del componente
    async obtenerHTMLComponente() {
        try {
            // Se obtienen las URLs con las ubicaciones de los archivos HTML y CSS
            const moduleURL = new URL(import.meta.url);
            const htmlURL = new URL('chatbot.html', moduleURL);
            const cssURL = new URL('chatbot_style.css', moduleURL);

            // Se obtiene el HTML del archivo HTML
            const html = await fetch(htmlURL).then(response => response.text());
            this.innerHTML = html;

            // Agregar dinámicamente el archivo CSS
            const linkElem = document.createElement('link');
            linkElem.setAttribute('rel', 'stylesheet');
            linkElem.setAttribute('type', 'text/css');
            linkElem.setAttribute('href', cssURL);
            document.head.appendChild(linkElem);
        }
        catch (error) {
            console.error('Error al cargar el componente:', error);
            this.innerHTML = `<div class="error">Error al cargar el componente: ${error.message}</div>`;
        }
    }
    

    async connectedCallback() {
        // Cargar el HTML del componente
        await this.obtenerHTMLComponente();
    
        // Añadir el nombre del bot
        $("#saludo").text(`Flexible Company Bot`);
    
        // Se obtienen los elementos del DOM
        const conversacion = $("#conversacion");
        const mensajeInput = $("#mensaje");
        const enviarBnt = $("#enviar");
        const resetBtn = $("#reset");
    
        // Evento para enviar el mensaje del usuario
        // Se envía el mensaje cuando se hace click en el botón de enviar
        enviarBnt.on("click", (event) => {
            try{
                event.preventDefault();
                event.stopPropagation();
                enviarMensajeUsuario(mensajeInput, conversacion, event);
                return false;
            }
            catch (error) {
                console.error('Error al enviar mensaje:', error);
                alert('No se pudo enviar el mensaje. Inténtalo de nuevo más tarde.');
            }
        });
    
        // Evento para enviar el mensaje del usuario
        // Se envía el mensaje cuando se presiona la tecla Enter
        mensajeInput.on("keydown", (event) => {
            try{
                if (event.key === "Enter") {
                    event.preventDefault();
                    event.stopPropagation();
                    enviarMensajeUsuario(mensajeInput, conversacion, event);
                    return false;
                }
            }
            catch (error) {
                console.error('Error al enviar mensaje:', error);
                alert('No se pudo enviar el mensaje. Inténtalo de nuevo más tarde.');
            }
        });
        
        // Evento para reiniciar la conversación
        // Se reinicia la conversación cuando se hace click en el botón de reiniciar
        resetBtn.on("click", () => {
            reiniciarConversacion(conversacion, mensajeInput);
        });
    }

}

//Declaración del componente
customElements.define('flexiblecompanybot-component', FlexibleCompanyBot);

