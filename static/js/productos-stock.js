// ============================================
// SISTEMA DE EDICIÓN DE STOCK DE PRODUCTOS
// ============================================

// ----- 1. OBTENER TOKEN DE SEGURIDAD -----
// Django necesita un "token" especial para aceptar cambios
// Este código busca ese token en las cookies del navegador
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Guardar el token en una variable para usarlo después
const csrftoken = getCookie('csrftoken');


// ----- 2. ACTIVAR MODO EDICIÓN -----
// Cuando el usuario hace clic en el stock, esto se ejecuta
function editarStock(productoId) {
    // Ocultar el número que se ve normalmente
    document.getElementById(`stock-display-${productoId}`).classList.add('d-none');
    
    // Mostrar el campo donde puede escribir
    document.getElementById(`stock-edit-${productoId}`).classList.remove('d-none');
    
    // Poner el cursor en el campo y seleccionar el número
    const input = document.getElementById(`stock-input-${productoId}`);
    input.focus();
    input.select();
}


// ----- 3. CANCELAR EDICIÓN -----
// Si el usuario presiona el botón X o presiona Escape
function cancelarStock(productoId) {
    // Mostrar de nuevo el número normal
    document.getElementById(`stock-display-${productoId}`).classList.remove('d-none');
    
    // Ocultar el campo de edición
    document.getElementById(`stock-edit-${productoId}`).classList.add('d-none');
    
    // Restaurar el número original (por si lo cambió)
    const displayElement = document.getElementById(`stock-display-${productoId}`);
    const valorOriginal = displayElement.textContent.trim().split('\n')[0].trim();
    document.getElementById(`stock-input-${productoId}`).value = valorOriginal;
}


// ----- 4. GUARDAR EL NUEVO STOCK -----
// Cuando el usuario presiona el botón ✓ o Enter
async function guardarStock(productoId) {
    const nuevoStock = document.getElementById(`stock-input-${productoId}`).value;
    
    // Validar que sea un número válido
    if (nuevoStock === '' || nuevoStock < 0) {
        mostrarToast('El stock debe ser un número positivo', 'danger');
        return;
    }
    
    try {
        // Enviar el nuevo stock al servidor (Django)
        const response = await fetch(`/ActualizarStock/${productoId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken  // Token de seguridad
            },
            body: `stock=${nuevoStock}`  // Enviar: stock=25
        });
        
        // Obtener la respuesta del servidor
        const data = await response.json();
        
        // Si todo salió bien
        if (data.success) {
            actualizarDisplayStock(productoId, data.nuevo_stock);  // Actualizar el número en pantalla
            cancelarStock(productoId);  // Volver al modo normal
            animarFilaActualizada(productoId);  // Hacer un efecto visual
            mostrarToast(data.message, 'success');  // Mostrar mensaje de éxito
        } else {
            mostrarToast(data.message || 'Error al actualizar', 'danger');
        }
    } catch (error) {
        mostrarToast('Error de conexión', 'danger');
    }
}


// ----- 5. ACTUALIZAR EL NÚMERO EN PANTALLA -----
// Cambia el badge con el nuevo stock y el color correcto
function actualizarDisplayStock(productoId, stockValue) {
    const displayElement = document.getElementById(`stock-display-${productoId}`);
    
    // Elegir el color según la cantidad
    let colorClase = 'text-bg-success';  // Verde si hay más de 10
    if (stockValue <= 0) {
        colorClase = 'text-bg-danger';  // Rojo si no hay stock
    } else if (stockValue <= 10) {
        colorClase = 'text-bg-warning';  // Amarillo si hay poco
    }
    
    // Cambiar el HTML del badge
    displayElement.className = `stock-display badge ${colorClase}`;
    displayElement.innerHTML = `${stockValue} <i class="bi bi-pencil-fill ms-1" style="font-size: 0.7rem;"></i>`;
    displayElement.style.cursor = 'pointer';
}


// ----- 6. ANIMACIÓN DE ÉXITO -----
// Hace que la fila se ponga verde brevemente
function animarFilaActualizada(productoId) {
    const fila = document.getElementById(`producto-${productoId}`);
    fila.classList.add('stock-updated');  // Agregar clase de animación
    setTimeout(() => {
        fila.classList.remove('stock-updated');  // Quitar después de 0.6 segundos
    }, 600);
}


// ----- 7. MOSTRAR MENSAJES (TOAST) -----
// Muestra una notificación en la esquina inferior derecha
function mostrarToast(mensaje, tipo = 'success') {
    const toastElement = document.getElementById('stockToast');
    const toastBody = document.getElementById('stockToastBody');
    
    // Cambiar el color según el tipo (success = verde, danger = rojo)
    toastElement.classList.remove('bg-success', 'bg-danger');
    toastElement.classList.add(`bg-${tipo}`);
    
    // Poner el texto del mensaje
    toastBody.textContent = mensaje;
    
    // Mostrar el toast por 3 segundos
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    toast.show();
}


// ----- 8. HACER FUNCIONES ACCESIBLES -----
// Permitir que el HTML pueda usar estas funciones con onclick
window.editarStock = editarStock;
window.cancelarStock = cancelarStock;
window.guardarStock = guardarStock;