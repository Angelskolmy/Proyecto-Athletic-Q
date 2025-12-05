/**
 * ========================================
 * SCRIPT: FILTROS EN TIEMPO REAL - HISTORIAL VENTAS
 * ========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    const inputBuscar = document.getElementById('buscarVenta');
    const selectMetodo = document.getElementById('filtroMetodo');
    const inputFecha = document.getElementById('filtroFecha');
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
     * Enviar formulario inmediatamente (para selects y fechas)
     */
    function enviarInmediato() {
        formFiltros.submit();
    }

    // ========================================
    // EVENTOS
    // ========================================

    // Buscador - con debounce
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

    // Filtro por método de pago - cambio inmediato
    if (selectMetodo) {
        selectMetodo.addEventListener('change', enviarInmediato);
    }

    // Filtro por fecha - cambio inmediato
    if (inputFecha) {
        inputFecha.addEventListener('change', enviarInmediato);
    }

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