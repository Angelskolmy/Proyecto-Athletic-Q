/* ================================
   SISTEMA DE EDICIÓN DE CATEGORÍAS
   CON VALIDACIÓN Y ENVÍO AJAX
   ================================ */

// ============================================
// ENVIAR FORMULARIO DE EDICIÓN DE CATEGORÍA
// ============================================

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // Obtener el formulario por su ID
    const form = document.getElementById('formEditarCategoria');
    
    // Si el formulario no existe, salir de la función
    if (!form) {
        console.error('❌ Formulario no encontrado');
        return;
    }
    
    // Guardar valores originales para detectar cambios
    const valoresOriginales = {
        nombre: form.querySelector('input[name="Nombre"]').value.trim(),
        estado: form.querySelector('select[name="Estado"]').value
    };
    
    // Agregar listener al evento submit (cuando se envía el formulario)
    form.addEventListener('submit', async function(e) {
        // Prevenir el envío tradicional del formulario (que recarga la página)
        e.preventDefault();
        
        try {
            // ============================================
            // 1. VALIDAR CAMPOS ANTES DE ENVIAR
            // ============================================
            
            // Obtener valores actuales del formulario
            const nombreInput = form.querySelector('input[name="Nombre"]');
            const estadoSelect = form.querySelector('select[name="Estado"]');
            
            const nombreActual = nombreInput.value.trim();
            const estadoActual = estadoSelect.value;
            
            // Validar que el nombre no esté vacío
            if (!nombreActual) {
                mostrarError('El nombre de la categoría es obligatorio');
                nombreInput.focus(); // Poner el cursor en el campo
                return; // Salir sin enviar
            }
            
            // Validar que tenga al menos 3 caracteres
            if (nombreActual.length < 3) {
                mostrarError('El nombre debe tener al menos 3 caracteres');
                nombreInput.focus();
                return;
            }
            
            // ============================================
            // 2. VERIFICAR SI HUBO CAMBIOS
            // ============================================
            
            const huboCambios = (
                nombreActual !== valoresOriginales.nombre ||
                estadoActual !== valoresOriginales.estado
            );
            
            // Si no hubo cambios, informar al usuario
            if (!huboCambios) {
                mostrarAdvertencia('No se detectaron cambios en la categoría');
                return; // Salir sin enviar
            }
            
            // ============================================
            // 3. CONFIRMAR ANTES DE ACTUALIZAR
            // ============================================
            
            // Mostrar cuadro de confirmación
            const confirmar = confirm('¿Está seguro de actualizar esta categoría?');
            
            // Si el usuario cancela, salir sin enviar
            if (!confirmar) {
                return;
            }
            
            // ============================================
            // 4. PREPARAR DATOS DEL FORMULARIO
            // ============================================
            
            // Crear un objeto FormData con todos los datos del formulario
            // Esto incluye todos los campos input, select, etc.
            const formData = new FormData(this);
            
            // Obtener el token CSRF de seguridad de Django
            // Este token es obligatorio para enviar formularios vía AJAX
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // ============================================
            // 5. DESHABILITAR BOTÓN DE ENVÍO (EVITAR DOBLE CLIC)
            // ============================================
            
            const btnSubmit = form.querySelector('button[type="submit"]');
            const textoBtnOriginal = btnSubmit.innerHTML;
            
            // Cambiar el texto y deshabilitar el botón
            btnSubmit.disabled = true;
            btnSubmit.innerHTML = '<i class="bi bi-hourglass-split"></i> Actualizando...';
            
            // ============================================
            // 6. ENVIAR DATOS AL SERVIDOR
            // ============================================
            
            // Obtener la URL actual (incluye el ID de la categoría)
            const urlActual = window.location.href;
            
            // Enviar los datos usando fetch (AJAX moderno)
            const response = await fetch(urlActual, {
                method: 'POST',  // Método POST porque estamos actualizando un registro
                headers: {
                    'X-CSRFToken': csrfToken  // Incluir el token de seguridad
                },
                body: formData  // Enviar todos los datos del formulario
            });

            // Convertir la respuesta del servidor a formato JSON
            const data = await response.json();
            
            // ============================================
            // 7. PROCESAR RESPUESTA DEL SERVIDOR
            // ============================================
            
            // ✅ SI LA ACTUALIZACIÓN FUE EXITOSA
            if (response.ok && data.success) {
                // Mostrar mensaje de éxito
                mostrarExito(data.message);
                
                // Actualizar los valores originales
                valoresOriginales.nombre = nombreActual;
                valoresOriginales.estado = estadoActual;
                
                // Esperar 1.5 segundos antes de redirigir
                setTimeout(() => {
                    // Si el servidor envió una URL de redirección
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                }, 1500);
            } else {
                // ❌ SI HUBO UN ERROR
                // Lanzar excepción con el mensaje del servidor
                throw new Error(data.message || 'Error al actualizar la categoría');
            }
            
        } catch (error) {
            // ============================================
            // 8. MANEJO DE ERRORES
            // ============================================
            
            // Capturar cualquier error y mostrarlo al usuario
            mostrarError(error.message);
            
            // Rehabilitar el botón de envío
            const btnSubmit = form.querySelector('button[type="submit"]');
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<i class="bi bi-check-circle"></i> Actualizar Categoría';
            
            // Log del error en consola para debugging
            console.error('❌ Error al actualizar categoría:', error);
        }
    });
    
    // ============================================
    // DETECTAR CAMBIOS EN TIEMPO REAL
    // ============================================
    
    // Listener para el campo nombre
    form.querySelector('input[name="Nombre"]').addEventListener('input', function() {
        // Resaltar visualmente si hay cambios
        if (this.value.trim() !== valoresOriginales.nombre) {
            this.classList.add('border-warning');
            this.classList.remove('border-success');
        } else {
            this.classList.remove('border-warning');
            this.classList.add('border-success');
        }
    });
    
    // Listener para el campo estado
    form.querySelector('select[name="Estado"]').addEventListener('change', function() {
        // Resaltar visualmente si hay cambios
        if (this.value !== valoresOriginales.estado) {
            this.classList.add('border-warning');
            this.classList.remove('border-success');
        } else {
            this.classList.remove('border-warning');
            this.classList.add('border-success');
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
    alert('❌ ' + mensaje);
}

/**
 * Muestra un mensaje de éxito al usuario
 * @param {string} mensaje - Texto del éxito a mostrar
 */
function mostrarExito(mensaje) {
    alert('✅ ' + mensaje);
}

/**
 * Muestra un mensaje de advertencia al usuario
 * @param {string} mensaje - Texto de la advertencia a mostrar
 */
function mostrarAdvertencia(mensaje) {
    alert('⚠️ ' + mensaje);
}