import { dropFile, newFile, saveFiles, showFileNames, deleteFile } from "./javascript/manejo_ficheros.js";

class FileUploader extends HTMLElement {
    constructor() {
        super();
        this.files = [];
        this.server_URL_path = null;
        this.server_URL = null;
    }

    //Método con los atributos que se van a observar
    static get observedAttributes() {
        return ['server_url'];
    }

    //Método que se ejecuta cuando se modifica un atributo
    attributeChangedCallback(attributeName, oldValue, newValue) {
        if (attributeName === 'server_url' && newValue !== oldValue) {
            this.server_URL = newValue;
            this.server_URL_path = this.server_URL + "/upload";
        }
    }

    //Método para obtener el HTML del componente
    async obtenerHTMLComponente(htmlLinkElement = document.createElement('link')) {
        try {
            const moduleURL = new URL(import.meta.url);
            const htmlURL = new URL('file-uploader.html', moduleURL);
            const cssURL = new URL('file-uploader_style.css', moduleURL);
            this.innerHTML = await fetch(htmlURL).then(response => response.text());

            const linkElem = htmlLinkElement;
            linkElem.setAttribute('rel', 'stylesheet');
            linkElem.setAttribute('type', 'text/css');
            linkElem.setAttribute('href', cssURL);
            document.head.appendChild(linkElem);
        } catch (error) {
            console.error('Error al cargar el componente:', error);
            this.innerHTML = `<div class="error">Error al cargar el componente: ${error.message}</div>`;
        }
    }

    async connectedCallback() {
        // Cargar el HTML del componente
        await this.obtenerHTMLComponente();

        // Se obtienen los elementos del DOM
        const contenedor = this.querySelector("#contenedor");
        const btnSeleccionar = this.querySelector("#btnSeleccionar");
        const btnSubir = this.querySelector("#btnSubir");

        // Evento para seleccionar un archivo
        // Se selecciona un archivo cuando se hace click en el contenedor, simulando un click en el botón de selección de archivos
        contenedor.addEventListener("click", (event) => {
            //Actúa como un botón para seleccionar un archivo
            btnSeleccionar.click();
        });

        //Evento para seleccionar un archivo
        //Se selecciona un archivo cuando se hace click en el botón de selección
        btnSeleccionar.addEventListener("change", (event) => {
            //Selecciona un archivo
            this.files = newFile(event.target.files[0], this.files, contenedor);
        });

        //Evento para subir un archivo
        //Se sube un archivo cuando se arrastra y se suelta en el contenedor
        contenedor.addEventListener("drop", (event) => {
            this.files = dropFile(event, this.files, contenedor);
        });

        contenedor.addEventListener("dragover", (event) => {
            event.preventDefault();
        });

        //Evento para almacenar los archivos
        //Se almacenan los archivos en el servidor cuando se hace click en el botón de subir
        btnSubir.addEventListener("click", (event) => {
            // Se comprueba que los ficheros tengan una extensión válida
            const validExtensions = ['txt', 'docx', 'pdf']
            const invalidFiles = this.files.filter(file => {
                const fileExtension = file.name.split('.').pop();
                return !validExtensions.includes(fileExtension);
            });

            // Se muestra un mensaje de error con los archivos inválidos
            if (invalidFiles.length > 0) {
                alert(`Los siguientes archivos no se subirán porque no tienen una extensión válida: ${invalidFiles.map(f => f.name).join(', ')}`);
                // Se eliminan los archivos inválidos de la lista de archivos a subir
                invalidFiles.forEach(file => deleteFile(file.name, this.files, contenedor));
                showFileNames(this.files, contenedor);
            }

            // Subir los archivos
            if (this.files.length != 0) {
                saveFiles(this.files, this.server_URL_path, contenedor)
                    .then(newFileList => {
                        this.files = newFileList; // Reemplazamos la lista original con la lista de archivos que no se subieron correctamente
                    }
                );
            }
            else{
                alert("No hay archivos para subir");
            }
        });
    }
}

customElements.define('file-uploader', FileUploader);
