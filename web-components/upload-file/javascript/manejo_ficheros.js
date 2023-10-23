// Función que muestra los ficheros seleccionados
// Muestra los nombres de los ficheros seleccionados con un icono
function showFileNames(contenedor, fileList) {
    // Recorre fileList y muestra los nombres de los archivos con su icono
    const fileNames = fileList.map(file => {
        let fileName = file.name;
        // Si el nombre del archivo es muy largo, se muestra solo los primeros 10 caracteres
        if (fileName.length > 10) {
            fileName = fileName.substring(0, 10) + "...";
        }
        return `<div class='file-icon-with-name'>
                    <img src='/web-components/upload-file/images/file.png' alt='icono de archivo' class='file-icon'/>
                    <div class='file-name'>${fileName}</div>
                </div>`;
    });
    contenedor.innerHTML = fileNames.join('');
}

// Función que guarda un nuevo fichero en la lista de ficheros
function newFile(file, fileList, contenedor) {
    fileList.push(file);
    showFileNames(contenedor, fileList);
    return fileList;
}

// Función que elimina un fichero de la lista de ficheros
function deleteFile(fileName, fileList, contenedor) {
    //Elimina un archivo de la lista de archivos
    const index = fileList.findIndex(file => file.name === fileName);
    fileList.splice(index, 1);
    showFileNames(contenedor, fileList);
    return fileList;
}

// Función que se ejecuta cuando se suelta un archivo en el contenedor
function dropFile(event, fileList, contenedor) {
    event.preventDefault();
    if (event.dataTransfer.items) {
        for (let i = 0; i < event.dataTransfer.items.length; i++) {
            if (event.dataTransfer.items[i].kind === 'file') {
                let file = event.dataTransfer.items[i].getAsFile();
                fileList = newFile(file, fileList, contenedor);
            }
        }
    } else {
        for (let i = 0; i < ev.dataTransfer.files.length; i++) {
            fileList = newFile(event.dataTransfer.files[i], fileList, contenedor);
        }
    }

    return fileList;
}

// Función que guarda los ficheros en el servidor
function saveFiles(fileList, serverURLPath, contenedor){
    const filesNotUploaded = [...fileList]; // Copiamos la lista original de archivos

    // Usamos reduce para encadenar las promesas
    // Se sube un archivo, y cuando se sube correctamente, se sube el siguiente
    const uploadChain = fileList.reduce((prevPromise, file, index) => {
        return prevPromise.then(() => {
            // Se hace la petición PUT para subir el archivo
            const fileName = file.name;
            const uploadPath = `${serverURLPath}/${fileName}`;
            const options = {
                method: 'PUT',
                body: file,
            };

            return fetch(uploadPath, options)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Error al subir el archivo ${fileName}: ${response.statusText}`);
                    } else {
                        const notUploadedIndex = filesNotUploaded.findIndex(f => f.name === file.name);
                        if (notUploadedIndex !== -1) {
                            filesNotUploaded.splice(notUploadedIndex, 1); // Eliminamos el archivo de la lista si se subió correctamente
                        }
                        fileList = deleteFile(fileName, fileList, contenedor); // Eliminamos el archivo de fileList
                    }
                });
        });
    }, Promise.resolve()); // Iniciamos con una promesa resuelta para iniciar la cadena

    return uploadChain
        .then(() => {
            // Cuando se suben todos los archivos, envía la petición al bot para que los procese
            processFiles();
            return filesNotUploaded; // Devolvemos la lista de archivos que no se subieron correctamente
        })
        .catch(error => {
            console.error('Error al almacenar los ficheros', error);
            alert('No se pudieron subir los ficheros. Inténtalo de nuevo más tarde.');
            throw error;
        });
}

// Función que envía la petición al bot para que procese los archivos
function processFiles(){
    const promesa = new Promise((resolve, reject) => {
        $.post({
            // Se envía una petición POST al bot
            url: "http://127.0.0.1:8000/process-data",
            success: function (respuesta) {
                const mensaje = respuesta.message;
                console.log('Respuesta del servidor:', mensaje);
                resolve();
            },
            error: function (error) {
                console.error('Error al enviar la petición al servidor:', error);
                reject(error);
            }
        });
    });

    return promesa.catch(error => {
        console.error('Error al enviar la petición al servidor:', error);
        alert('No se pudo procesar los ficheros. Inténtalo de nuevo más tarde.');
        throw error;
    });
}




export { dropFile, newFile, saveFiles, showFileNames, deleteFile };
