/**
 * ========================================
 * SCRIPT: FILTRADO DE USUARIOS EN TIEMPO REAL
 * ========================================
 */

document.addEventListener('DOMContentLoaded', function() {
    const inputBuscar = document.getElementById('buscarUsuario');
    const selectEstado = document.getElementById('filtroEstado');
    const selectRol = document.getElementById('filtroRol');
    const btnLimpiar = document.getElementById('btnLimpiarFiltros');
    const filas = document.querySelectorAll('.usuario-row');
    const countVisible = document.getElementById('countVisible');
    const exportForms = document.querySelectorAll('.form-export-usuarios');

    // Función para filtrar usuarios
    function filtrarUsuarios() {
        const busqueda = inputBuscar.value.toLowerCase().trim();
        const filtroEstado = selectEstado ? selectEstado.value : '';
        const filtroRol = selectRol ? selectRol.value : '';
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
            if (filtroEstado === 'active') {
                coincideFiltro = estado === 'active';
            } else if (filtroEstado === 'inactive') {
                coincideFiltro = estado === 'inactive';
            }

            if (coincideFiltro && filtroRol) {
                coincideFiltro = grupos.includes(filtroRol);
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
            if (busqueda !== '' || filtroEstado !== '' || filtroRol !== '') {
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
    if (selectEstado) {
        selectEstado.addEventListener('change', () => {
            localStorage.setItem('usuariosFiltroEstado', selectEstado.value);
            filtrarUsuarios();
        });
    }

    if (selectRol) {
        selectRol.addEventListener('change', () => {
            localStorage.setItem('usuariosFiltroRol', selectRol.value);
            filtrarUsuarios();
        });
    }

    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', function() {
            inputBuscar.value = '';
            if (selectEstado) {
                selectEstado.value = '';
                localStorage.removeItem('usuariosFiltroEstado');
            }
            if (selectRol) {
                selectRol.value = '';
                localStorage.removeItem('usuariosFiltroRol');
            }
            localStorage.removeItem('usuariosBusqueda');
            filtrarUsuarios();
        });
    }

    if (inputBuscar) {
        const storedSearch = localStorage.getItem('usuariosBusqueda');
        if (storedSearch) {
            inputBuscar.value = storedSearch;
        }
        inputBuscar.addEventListener('input', () => {
            localStorage.setItem('usuariosBusqueda', inputBuscar.value.toLowerCase());
            filtrarUsuarios();
        });
    }

    if (selectEstado) {
        const storedState = localStorage.getItem('usuariosFiltroEstado');
        if (storedState) {
            selectEstado.value = storedState;
        }
    }

    if (selectRol) {
        const storedRole = localStorage.getItem('usuariosFiltroRol');
        if (storedRole) {
            selectRol.value = storedRole;
        }
    }

    if (exportForms.length) {
        exportForms.forEach(form => {
            const hiddenField = form.querySelector('.visible-ids-field');
            form.addEventListener('submit', function(event) {
                const ids = Array.from(filas)
                    .filter(fila => fila.style.display !== 'none')
                    .map(fila => fila.dataset.userId)
                    .filter(Boolean);

                if (ids.length === 0) {
                    event.preventDefault();
                    alert('No hay usuarios visibles para exportar.');
                    return;
                }

                hiddenField.value = ids.join(',');
            });
        });
    }

    filtrarUsuarios();
});
