/* =================================
    SISTEMA DE CREACIÓN DE USUARIOS
    CON REGISTRO DE HUELLA DACTILAR
   ================================ */

// ============================================
//  ENVIAR FORMULARIO DE CREACIÓN
// ============================================

// Escuchar el evento "submit" del formulario
document.getElementById('formCrearUsuario').addEventListener('submit', async function(e) {
    // Prevenir que el formulario se envíe de forma tradicional (recarga de página)
    e.preventDefault();
    
    try {
        // Crear un objeto FormData con todos los datos del formulario
        // (nombre, apellido, email, contraseña, etc.)
        const formData = new FormData(this);
        
        // Obtener el token CSRF de seguridad de Django
        // Este token es obligatorio para enviar formularios vía AJAX
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Enviar los datos al servidor usando fetch (AJAX moderno)
        const response = await fetch("/Empleados/crear/", {
            method: 'POST',  // Método POST porque estamos creando un registro
            headers: {
                'X-CSRFToken': csrfToken  // Incluir el token de seguridad
            },
            body: formData  // Enviar todos los datos del formulario
        });

        // Convertir la respuesta del servidor a formato JSON
        const data = await response.json();
        
        // ✅ SI LA CREACIÓN FUE EXITOSA
        if (response.ok && data.success) {
            
            // Si el servidor indica que debe registrar huella dactilar
            if (data.show_fingerprint_modal) {
                // Mostrar el modal para registrar la huella
                mostrarModalHuella(data.user_id);
            } else {
                // Si no requiere huella, mostrar mensaje y redirigir
                alert(data.message);
                
                // Si el servidor envió una URL de redirección
                if (data.redirect) {
                    window.location.href = data.redirect;  // Redirigir a la lista de usuarios
                }
            }
        } else {
            // ❌ SI HUBO UN ERROR
            throw new Error(data.message || 'Error al crear el usuario');
        }
    } catch (error) {
        // Mostrar el mensaje de error al usuario
        alert(error.message);
    }
});


// ============================================
// 🔐 VARIABLES GLOBALES PARA REGISTRO DE HUELLA
// ============================================

// Contador de intentos de lectura de huella (máximo 3)
let intentoActual = 1;

// ID del usuario que está registrando su huella
let userId = null;


// ============================================
// 👁️ MOSTRAR MODAL DE REGISTRO DE HUELLA
// ============================================

function mostrarModalHuella(user_id) {
    // Guardar el ID del usuario en la variable global
    userId = user_id;
    
    // Reiniciar el contador de intentos a 1
    intentoActual = 1;
    
    // Actualizar la barra de progreso y el texto del modal
    actualizarProgreso();
    
    // Crear una instancia del modal de Bootstrap
    const modal = new bootstrap.Modal(document.getElementById('modalRegistroHuella'));
    
    // Mostrar el modal al usuario
    modal.show();
}


// ============================================
// 📊 ACTUALIZAR BARRA DE PROGRESO
// ============================================

function actualizarProgreso() {
    // Actualizar el texto que muestra el número de intento (1 de 3, 2 de 3, etc.)
    document.getElementById('intentoActual').textContent = intentoActual;
    
    // Calcular el ancho de la barra de progreso
    // Intento 1 = 33.33%, Intento 2 = 66.66%, Intento 3 = 100%
    const porcentaje = (intentoActual * 33.33);
    document.getElementById('progresoHuella').style.width = porcentaje + '%';
    
    // Si es el tercer intento, cambiar el mensaje de instrucción
    if (intentoActual === 3) {
        document.getElementById('huellaInstruccion').textContent = 
            'Último intento - Coloca tu dedo firmemente';
    }
}


// ============================================
// 👆 REGISTRAR HUELLA DACTILAR
// ============================================

// Escuchar el clic en el botón "Leer Huella"
document.getElementById('btnLeerHuella').addEventListener('click', async function() {
    try {
        // 🔬 SIMULAR LECTURA DE HUELLA
        // En producción, aquí se conectaría con el lector de huellas real
        // Por ahora, generamos un código único simulado
        const huellaData = 'huella_simulada_' + Date.now();
        
        // Obtener el token CSRF para seguridad
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Enviar los datos de la huella al servidor
        const response = await fetch(`/Empleados/registrar-huella/${userId}/`, {
            method: 'POST',  // Enviar datos al servidor
            headers: {
                'X-CSRFToken': csrfToken,  // Token de seguridad
                'Content-Type': 'application/x-www-form-urlencoded'  // Formato de datos
            },
            body: new URLSearchParams({
                'huella_data': huellaData,  // Datos de la huella leída
                'attempt_number': intentoActual  // Número de intento (1, 2 o 3)
            })
        });

        // Convertir la respuesta a JSON
        const data = await response.json();
        
        // ✅ SI EL REGISTRO FUE EXITOSO
        if (response.ok && data.success) {
            
            // Si se completaron los 3 intentos exitosamente
            if (data.completed) {
                // Mostrar mensaje de éxito
                alert(data.message);
                
                // Cerrar el modal
                bootstrap.Modal.getInstance(document.getElementById('modalRegistroHuella')).hide();
                
                // Redirigir a la lista de usuarios
                window.location.href = '/Empleados/';
            } else {
                // Si aún faltan intentos
                alert(data.message);  // Mostrar mensaje (ej: "Intento 1 registrado")
                
                // Incrementar el contador de intentos
                intentoActual++;
                
                // Actualizar la barra de progreso
                actualizarProgreso();
            }
        } else {
            // ❌ SI HUBO UN ERROR
            alert('Error: ' + data.message);
        }
    } catch (error) {
        // Capturar errores de red o del servidor
        alert('Error al registrar huella: ' + error.message);
    }
});