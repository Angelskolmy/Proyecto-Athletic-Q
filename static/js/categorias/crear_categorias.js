/* ================================
   SISTEMA DE CREACIÓN DE CATEGORÍAS
   CON VALIDACIÓN Y ENVÍO AJAX
   ================================ */

// ============================================
// ENVIAR FORMULARIO DE CREACIÓN DE CATEGORÍA
// ============================================

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // Obtener el formulario por su ID
    const form = document.getElementById('formCrearCategoria');
    
    // Si el formulario no existe, salir de la función
    if (!form) {
        console.error('❌ Formulario no encontrado');
        return;
    }
    
    // Agregar listener al evento submit (cuando se envía el formulario)
    form.addEventListener('submit', async function(e) {
        // Prevenir el envío tradicional del formulario (que recarga la página)
        e.preventDefault();
        
        try {
            // ============================================
            // 1. VALIDAR CAMPOS ANTES DE ENVIAR
            // ============================================
            
            // Obtener el campo de nombre de la categoría
            const nombreInput = form.querySelector('input[name="Nombre"]');
            const nombre = nombreInput.value.trim();
            
            // Validar que el nombre no esté vacío
            if (!nombre) {
                mostrarError('El nombre de la categoría es obligatorio');
                nombreInput.focus(); // Poner el cursor en el campo
                return; // Salir sin enviar
            }
            
            // Validar que tenga al menos 3 caracteres
            if (nombre.length < 3) {
                mostrarError('El nombre debe tener al menos 3 caracteres');
                nombreInput.focus();
                return;
            }
            
            // ============================================
            // 2. PREPARAR DATOS DEL FORMULARIO
            // ============================================
            
            // Crear un objeto FormData con todos los datos del formulario
            // Esto incluye todos los campos input, select, etc.
            const formData = new FormData(this);
            
            // Obtener el token CSRF de seguridad de Django
            // Este token es obligatorio para enviar formularios vía AJAX
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // ============================================
            // 3. DESHABILITAR BOTÓN DE ENVÍO (EVITAR DOBLE CLIC)
            // ============================================
            
            const btnSubmit = form.querySelector('button[type="submit"]');
            const textoBtnOriginal = btnSubmit.innerHTML;
            
            // Cambiar el texto y deshabilitar el botón
            btnSubmit.disabled = true;
            btnSubmit.innerHTML = '<i class="bi bi-hourglass-split"></i> Guardando...';
            
            // ============================================
            // 4. ENVIAR DATOS AL SERVIDOR
            // ============================================
            
            // Enviar los datos usando fetch (AJAX moderno)
            const response = await fetch("/Categorias/crear/", {
                method: 'POST',  // Método POST porque estamos creando un registro
                headers: {
                    'X-CSRFToken': csrfToken  // Incluir el token de seguridad
                },
                body: formData  // Enviar todos los datos del formulario
            });

            // Convertir la respuesta del servidor a formato JSON
            const data = await response.json();
            
            // ============================================
            // 5. PROCESAR RESPUESTA DEL SERVIDOR
            // ============================================
            
            // SI LA CREACIÓN FUE EXITOSA
            if (response.ok && data.success) {
                // Mostrar mensaje de éxito
                mostrarExito(data.message);
                
                // Esperar 1 segundo antes de redirigir
                setTimeout(() => {
                    // Si el servidor envió una URL de redirección
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                }, 1000);
            } else {
                // ❌ SI HUBO UN ERROR
                // Lanzar excepción con el mensaje del servidor
                throw new Error(data.message || 'Error al crear la categoría');
            }
            
        } catch (error) {
            // ============================================
            // 6. MANEJO DE ERRORES
            // ============================================
            
            // Capturar cualquier error y mostrarlo al usuario
            mostrarError(error.message);
            
            // Rehabilitar el botón de envío
            const btnSubmit = form.querySelector('button[type="submit"]');
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<i class="bi bi-check-circle"></i> Guardar Categoría';
            
            // Log del error en consola para debugging
            console.error('❌ Error al crear categoría:', error);
        }
    });
});


// ============================================
// FUNCIONES AUXILIARES PARA MOSTRAR MENSAJES
// ============================================

/**
 * Muestra un mensaje de error al usuario
 * @param {string} mensaje - Texto del error a mostrar
 */
function mostrarError(mensaje) {
    // Opción 1: Usar alert (simple pero funcional)
    alert('❌ ' + mensaje);
    
    // Opción 2: Crear un toast personalizado (más profesional)
    // Descomentar si prefieres este estilo:
    /*
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-bg-danger border-0 position-fixed bottom-0 end-0 m-3';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-x-circle-fill me-2"></i>${mensaje}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    setTimeout(() => toast.remove(), 5000);
    */
}

/**
 * Muestra un mensaje de éxito al usuario
 * @param {string} mensaje - Texto del éxito a mostrar
 */
function mostrarExito(mensaje) {
    // Opción 1: Usar alert
    alert('✅ ' + mensaje);
    
    // Opción 2: Toast personalizado (descomentar si prefieres):
    /*
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-bg-success border-0 position-fixed bottom-0 end-0 m-3';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-check-circle-fill me-2"></i>${mensaje}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    */
}