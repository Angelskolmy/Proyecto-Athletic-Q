/**
 * Mostrar alertas de Django con SweetAlert2
 * Los mensajes se pasan desde el template como variable global
 */
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si existen mensajes de Django
    if (typeof djangoMessages !== 'undefined' && djangoMessages.length > 0) {
        djangoMessages.forEach(function(msg) {
            let icon, title;
            
            switch(msg.tags) {
                case 'success':
                    icon = 'success';
                    title = '¡Éxito!';
                    break;
                case 'error':
                    icon = 'error';
                    title = '¡Error!';
                    break;
                case 'warning':
                    icon = 'warning';
                    title = '¡Atención!';
                    break;
                case 'info':
                    icon = 'info';
                    title = 'Información';
                    break;
                default:
                    icon = 'info';
                    title = 'Aviso';
            }
            
            Swal.fire({
                icon: icon,
                title: title,
                text: msg.message,
                confirmButtonColor: '#8B0000',
                timer: 3000,
                timerProgressBar: true
            });
        });
    }
});

/**
 * Confirmar acción genérica
 */
function confirmarAccion(url, titulo, texto, textoBoton = 'Confirmar') {
    Swal.fire({
        title: titulo,
        text: texto,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#8B0000',
        cancelButtonColor: '#6c757d',
        confirmButtonText: textoBoton,
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
    });
}