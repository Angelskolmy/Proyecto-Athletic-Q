document.addEventListener('DOMContentLoaded', () => {
    const formFiltros = document.getElementById('formFiltrosUsuarios');
    const selectEstado = document.getElementById('filtroEstado');
    const selectRol = document.getElementById('filtroRol');
    const inputBuscar = document.getElementById('buscarUsuario');
    const btnLimpiar = document.getElementById('btnLimpiarFiltros');
    const exportForms = document.querySelectorAll('.form-export-usuarios');
    const filas = document.querySelectorAll('.usuario-row');

    let searchTimeout = null;

    const submitFiltros = () => {
        if (formFiltros) {
            formFiltros.submit();
        }
    };

    if (selectEstado) {
        selectEstado.addEventListener('change', submitFiltros);
    }

    if (selectRol) {
        selectRol.addEventListener('change', submitFiltros);
    }

    if (inputBuscar) {
        inputBuscar.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => submitFiltros(), 400);
        });
    }

    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', () => {
            if (selectEstado) selectEstado.value = '';
            if (selectRol) selectRol.value = '';
            if (inputBuscar) inputBuscar.value = '';
            submitFiltros();
        });
    }

    if (exportForms.length) {
        exportForms.forEach(form => {
            const hiddenField = form.querySelector('.visible-ids-field');
            form.addEventListener('submit', event => {
                const ids = Array.from(filas)
                    .map(fila => fila.dataset.userId)
                    .filter(Boolean);

                if (!ids.length) {
                    event.preventDefault();
                    alert('No hay usuarios para exportar.');
                    return;
                }

                hiddenField.value = ids.join(',');
            });
        });
    }
});
