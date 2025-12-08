/**
 * ========================================
 * SCRIPT: FILTRADO DE USUARIOS EN TIEMPO REAL
 * ========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    const inputBuscar = document.getElementById('buscarUsuario');
    const selectFiltro = document.getElementById('filtroUsuarios');
    const btnLimpiar = document.getElementById('btnLimpiarFiltros');
    const filas = document.querySelectorAll('.usuario-row');
    const countVisible = document.getElementById('countVisible');

    // Función para filtrar usuarios
    function filtrarUsuarios() {
        const busqueda = inputBuscar.value.toLowerCase().trim();
        const filtro = selectFiltro.value;
        let visibles = 0;

        filas.forEach(fila => {
            const nombre = fila.dataset.nombre || '';
            const cedula = fila.dataset.cedula || '';
            const correo = fila.dataset.correo || '';
            const estado = fila.dataset.estado || '';
            const grupos = fila.dataset.grupo || '';

            // Verificar búsqueda
            const coincideBusqueda = busqueda === '' || 
                nombre.includes(busqueda) || 
                cedula.includes(busqueda) || 
                correo.includes(busqueda);

            // Verificar filtro
            let coincideFiltro = true;
            if (filtro === 'active') {
                coincideFiltro = estado === 'active';
            } else if (filtro === 'inactive') {
                coincideFiltro = estado === 'inactive';
            } else if (filtro.startsWith('group_')) {
                coincideFiltro = grupos.includes(filtro);
            }

            // Mostrar u ocultar fila
            if (coincideBusqueda && coincideFiltro) {
                fila.style.display = '';
                visibles++;
            } else {
                fila.style.display = 'none';
            }
        });

        // Actualizar contador
        if (countVisible) {
            countVisible.textContent = visibles;
        }

        // Mostrar/ocultar botón limpiar
        if (btnLimpiar) {
            if (busqueda !== '' || filtro !== '') {
                btnLimpiar.classList.remove('d-none');
            } else {
                btnLimpiar.classList.add('d-none');
            }
        }

        // Mostrar mensaje si no hay resultados
        mostrarMensajeVacio(visibles);
    }

    // Mostrar mensaje cuando no hay resultados
    function mostrarMensajeVacio(visibles) {
        const tbody = document.getElementById('tablaUsuarios');
        const noResults = document.getElementById('noResults');

        if (visibles === 0 && filas.length > 0) {
            if (!noResults && tbody) {
                const tr = document.createElement('tr');
                tr.id = 'noResults';
                tr.innerHTML = `
                    <td colspan="10" class="text-center py-4">
                        <i class="bi bi-search fs-1 text-muted"></i>
                        <p class="text-muted mt-2">No se encontraron usuarios con los filtros aplicados</p>
                    </td>
                `;
                tbody.appendChild(tr);
            }
        } else {
            if (noResults) noResults.remove();
        }
    }

    // Eventos
    if (inputBuscar) {
        inputBuscar.addEventListener('input', filtrarUsuarios);
    }

    if (selectFiltro) {
        selectFiltro.addEventListener('change', filtrarUsuarios);
    }

    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', function() {
            inputBuscar.value = '';
            selectFiltro.value = '';
            filtrarUsuarios();
        });
    }
});