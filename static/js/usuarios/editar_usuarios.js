// SISTEMA DE EDICION DE USUARIOS CON VALIDACION

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // ENVIO DEL FORMULARIO DE EDICION
    
    // Obtener el formulario por su ID
    const form = document.getElementById('formEditarUsuario');
    
    // Si el formulario no existe, salir
    if (!form) {
        console.error('Formulario no encontrado');
        return;
    }
    
    // Agregar listener al evento submit (cuando se envía el formulario)
    form.addEventListener('submit', async function(e) {
        // Prevenir el envío tradicional del formulario (que recarga la página)
        e.preventDefault();
        
        try {
            // Crear un objeto FormData con todos los datos del formulario
            // Esto incluye archivos (como la imagen de perfil)
            const formData = new FormData(this);
            
            // Obtener el token CSRF de seguridad de Django
            // Este token es obligatorio para enviar formularios vía AJAX
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Obtener el ID del empleado desde la URL actual
            // Ejemplo: /Empleados/editar/5/ -> empleadoId = 5
            const urlParts = window.location.pathname.split('/');
            const empleadoId = urlParts[urlParts.length - 2];
            
            // Enviar los datos al servidor usando fetch (AJAX moderno)
            const response = await fetch(`/Empleados/editar/${empleadoId}/`, {
                method: 'POST',  // Método POST porque estamos actualizando datos
                headers: {
                    'X-CSRFToken': csrfToken  // Incluir el token de seguridad
                },
                body: formData  // Enviar todos los datos del formulario
            });

            // Convertir la respuesta del servidor a formato JSON
            const data = await response.json();
            
            // SI LA ACTUALIZACION FUE EXITOSA
            if (response.ok && data.success) {
                // Mostrar mensaje de éxito
                alert(data.message);
                
                // Si el servidor envió una URL de redirección
                if (data.redirect) {
                    // Redirigir a la lista de usuarios
                    window.location.href = data.redirect;
                }
            } else {
                // SI HUBO UN ERROR
                // Lanzar excepción con el mensaje del servidor
                throw new Error(data.message || 'Error al actualizar el usuario');
            }
        } catch (error) {
            // Capturar cualquier error y mostrarlo al usuario
            alert(error.message);
        }
    });
    
    
    // PREVISUALIZACION DE IMAGEN ANTES DE SUBIR
    
    // Obtener el input de tipo file (campo para subir imagen)
    const inputImagen = document.querySelector('input[type="file"][name="empleados_img"]');
    
    // Si existe el campo de imagen
    if (inputImagen) {
        // Agregar listener al evento change (cuando seleccionan un archivo)
        inputImagen.addEventListener('change', function(e) {
            // Obtener el archivo seleccionado
            const file = e.target.files[0];
            
            // Verificar que realmente hay un archivo
            if (file) {
                // Crear un objeto FileReader para leer el archivo
                const reader = new FileReader();
                
                // Definir qué hacer cuando el archivo se haya leído
                reader.onload = function(event) {
                    // Buscar si ya existe una imagen de previsualización
                    let imgPreview = document.getElementById('preview-img');
                    
                    // Si NO existe, crear el contenedor
                    if (!imgPreview) {
                        // Crear un div contenedor
                        const previewContainer = document.createElement('div');
                        previewContainer.className = 'preview-container';
                        previewContainer.innerHTML = `
                            <img id="preview-img" class="preview-image" alt="Vista previa">
                        `;
                        
                        // Insertar el contenedor ANTES del input de archivo
                        inputImagen.parentElement.insertBefore(previewContainer, inputImagen);
                        
                        // Obtener la referencia de la imagen recién creada
                        imgPreview = document.getElementById('preview-img');
                    }
                    
                    // Asignar la imagen leída al src de la etiqueta img
                    imgPreview.src = event.target.result;
                };
                
                // Leer el archivo como una URL de datos (base64)
                // Esto permite mostrar la imagen sin subirla al servidor todavía
                reader.readAsDataURL(file);
            }
        });
    }
    
    
    // VALIDACION DEL CAMPO DE CONTRASEÑA
    
    // Obtener los campos de contraseña
    const passwordInput = document.querySelector('input[type="password"][name="password"]');
    const confirmPasswordInput = document.querySelector('input[type="password"][name="password_confirm"]');
    
    // Si ambos campos existen
    if (passwordInput && confirmPasswordInput) {
        // Agregar listener al campo de confirmación
        confirmPasswordInput.addEventListener('blur', function() {
            // blur se ejecuta cuando el usuario sale del campo
            
            // Obtener los valores de ambos campos
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;
            
            // Si ambos tienen contenido Y NO coinciden
            if (password && confirmPassword && password !== confirmPassword) {
                // Marcar el campo como inválido
                confirmPasswordInput.classList.add('is-invalid');
                
                // Mostrar mensaje de error
                let errorMsg = confirmPasswordInput.nextElementSibling;
                if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                    errorMsg = document.createElement('div');
                    errorMsg.className = 'invalid-feedback';
                    errorMsg.textContent = 'Las contraseñas no coinciden';
                    confirmPasswordInput.parentElement.appendChild(errorMsg);
                }
            } else {
                // Si coinciden, quitar la marca de error
                confirmPasswordInput.classList.remove('is-invalid');
                const errorMsg = confirmPasswordInput.nextElementSibling;
                if (errorMsg && errorMsg.classList.contains('invalid-feedback')) {
                    errorMsg.remove();
                }
            }
        });
    }
});