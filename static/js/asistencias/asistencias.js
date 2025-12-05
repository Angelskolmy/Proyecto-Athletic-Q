/**
 * ========================================
 * SCRIPT: FILTROS EN TIEMPO REAL - ASISTENCIAS
 * ========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    const inputBuscar = document.getElementById('buscarNombre');
    const selectTipo = document.getElementById('filtroTipo');
    const formFiltros = document.getElementById('formFiltros');
    
    let debounceTimer;

    /**
     * Enviar formulario con debounce para el buscador
     * Espera 400ms después de que el usuario deje de escribir
     */
    function enviarConDebounce() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            formFiltros.submit();
        }, 400);
    }

    /**
     * Enviar formulario inmediatamente (para selects)
     */
    function enviarInmediato() {
        formFiltros.submit();
    }

    // ========================================
    // EVENTOS
    // ========================================

    // Buscador por nombre - con debounce
    if (inputBuscar) {
        inputBuscar.addEventListener('input', enviarConDebounce);
        
        // Enviar al presionar Enter
        inputBuscar.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                clearTimeout(debounceTimer);
                formFiltros.submit();
            }
        });
    }

    // Filtro por tipo/rol - cambio inmediato
    if (selectTipo) {
        selectTipo.addEventListener('change', enviarInmediato);
    }

    // ========================================
    // LAS FECHAS NO SE ENVÍAN AUTOMÁTICAMENTE
    // Solo se envían al hacer clic en el botón "Filtrar"
    // ========================================

    // ========================================
    // MANTENER FOCUS EN EL INPUT DESPUÉS DE SUBMIT
    // ========================================
    
    // Si hay texto en el buscador, mantener el foco
    if (inputBuscar && inputBuscar.value.length > 0) {
        inputBuscar.focus();
        // Mover cursor al final del texto
        inputBuscar.setSelectionRange(inputBuscar.value.length, inputBuscar.value.length);
    }
});