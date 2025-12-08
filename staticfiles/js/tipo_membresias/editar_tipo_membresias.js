/**
 * ========================================
 * SCRIPT: PREVISUALIZACIÓN DE IMAGEN
 * ========================================
 * Permite previsualizar la imagen seleccionada
 * antes de enviar el formulario de edición
 */

document.addEventListener('DOMContentLoaded', function() {
    // Obtener el input de la imagen
    // Nota: El ID del input se genera dinámicamente por Django
    // Buscar el input con name="tipo_membresia_img"
    const inputImagen = document.querySelector('input[name="tipo_membresia_img"]');
    
    // Verificar que el input existe en la página
    if (!inputImagen) {
        console.warn('⚠️ Input de imagen no encontrado');
        return;
    }
    
    console.log('✅ Script de previsualización cargado correctamente');
    
    /**
     * Evento: change
     * Se activa cuando el usuario selecciona un archivo
     */
    inputImagen.addEventListener('change', function(e) {
        // Obtener el archivo seleccionado
        const file = e.target.files[0];
        
        // Validar que se haya seleccionado un archivo
        if (!file) {
            console.log('ℹ️ No se seleccionó ningún archivo');
            return;
        }
        
        console.log('📁 Archivo seleccionado:', file.name);
        
        // Validar que sea una imagen
        if (!file.type.match('image.*')) {
            alert('⚠️ Por favor selecciona un archivo de imagen válido');
            inputImagen.value = ''; // Limpiar el input
            return;
        }
        
        // Crear un FileReader para leer el archivo
        const reader = new FileReader();
        
        /**
         * Evento: onload del FileReader
         * Se ejecuta cuando se completa la lectura del archivo
         */
        reader.onload = function(event) {
            // Buscar si ya existe un contenedor de previsualización
            let previewContainer = document.getElementById('preview-container');
            
            // Si no existe, crear el contenedor
            if (!previewContainer) {
                previewContainer = document.createElement('div');
                previewContainer.id = 'preview-container';
                previewContainer.className = 'mt-3 text-center';
                previewContainer.innerHTML = `
                    <p class="text-muted mb-2">
                        <i class="bi bi-eye me-1"></i>Nueva imagen:
                    </p>
                    <img id="preview-img" class="rounded shadow-sm" 
                         style="max-height: 150px; object-fit: cover; border: 2px solid #dee2e6;">
                `;
                
                // Insertar el contenedor después del input
                inputImagen.parentElement.appendChild(previewContainer);
                
                console.log('✅ Contenedor de previsualización creado');
            }
            
            // Actualizar la imagen de previsualización
            const previewImg = document.getElementById('preview-img');
            if (previewImg) {
                previewImg.src = event.target.result;
                console.log('✅ Imagen de previsualización actualizada');
            }
        };
        
        /**
         * Evento: onerror del FileReader
         * Se ejecuta si hay un error al leer el archivo
         */
        reader.onerror = function() {
            console.error('❌ Error al leer el archivo');
            alert('❌ Hubo un error al cargar la imagen. Por favor intenta de nuevo.');
        };
        
        // Iniciar la lectura del archivo como Data URL (base64)
        reader.readAsDataURL(file);
    });
});