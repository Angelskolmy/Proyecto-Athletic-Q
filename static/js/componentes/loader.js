/**
 * ========================================
 * SCRIPT: SPINNER DE CARGA GLOBAL
 * ========================================
 * Muestra un spinner mientras la página carga,
 * al navegar entre páginas y al enviar formularios.
 */

(function() {
    'use strict';

    const loader = document.getElementById('page-loader');
    
    if (!loader) {
        console.warn('⚠️ Elemento #page-loader no encontrado');
        return;
    }

    /**
     * Ocultar el spinner
     */
    function hideLoader() {
        loader.classList.add('hidden');
    }

    /**
     * Mostrar el spinner
     */
    function showLoader() {
        loader.classList.remove('hidden');
    }

    /**
     * Verificar si un enlace debe activar el spinner
     * @param {HTMLElement} link - Elemento <a>
     * @returns {boolean}
     */
    function shouldShowLoader(link) {
        if (!link || !link.getAttribute('href')) return false;
        
        const href = link.getAttribute('href');
        
        // Ignorar estos casos:
        if (href.startsWith('#')) return false;                    // Anchors
        if (href.startsWith('javascript:')) return false;          // JavaScript
        if (link.hasAttribute('data-bs-toggle')) return false;     // Modales Bootstrap
        if (link.getAttribute('target') === '_blank') return false; // Nueva pestaña
        if (link.classList.contains('no-loader')) return false;    // Clase para ignorar
        
        return true;
    }

    // ========================================
    // EVENTOS
    // ========================================

    // 1. Ocultar spinner cuando el DOM esté listo
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(hideLoader, 200);
    });

    // 2. Mostrar spinner al hacer clic en enlaces de navegación
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href]');
        
        if (shouldShowLoader(link)) {
            showLoader();
        }
    });

    // 3. Mostrar spinner al enviar formularios POST
    document.addEventListener('submit', function(e) {
        const form = e.target;
        
        // Solo para formularios POST (no para filtros GET)
        if (form.method.toLowerCase() === 'post') {
            // Ignorar formularios con clase especial
            if (!form.classList.contains('no-loader')) {
                showLoader();
            }
        }
    });

    // 4. Ocultar spinner si el usuario vuelve atrás (bfcache)
    window.addEventListener('pageshow', function(e) {
        if (e.persisted) {
            hideLoader();
        }
    });

    // 5. Ocultar si hay error de carga
    window.addEventListener('error', function() {
        hideLoader();
    });
    
    document.addEventListener('DOMContentLoaded', function() {
    const pageLoader = document.getElementById('page-loader');
    
    // Ocultar loader cuando termina de cargar la página
    window.addEventListener('load', function() {
        if (pageLoader) {
        pageLoader.style.display = 'none';
        }
    });
    
    // Detectar descargas de archivos
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href*="/exportar/"], a[href*="/descargar/"]');
        if (link && pageLoader) {
        // Ocultar después de 500ms
        setTimeout(() => {
            pageLoader.style.display = 'none';
        }, 500);
        }
    });
    
    // Detectar cuando la página es visible nuevamente (volver del navegador)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && pageLoader) {
        pageLoader.style.display = 'none';
        }
    });
    });


    // ========================================
    // API PÚBLICA (opcional)
    // ========================================
    
    window.PageLoader = {
        show: showLoader,
        hide: hideLoader
    };

})();