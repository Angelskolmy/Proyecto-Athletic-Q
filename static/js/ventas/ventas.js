/* ================================
    SISTEMA DE CARRITO DE VENTAS
   ================================ */

// Inicializar carrito vacío
let carrito = [];

/**
 * Agregar producto al carrito
 */
function agregar(id, nombre, precio, stock) {
  const existe = carrito.find(item => item.id === id);
  
  if (existe) {
    if (existe.cantidad >= stock) {
      mostrarAlerta(` Stock insuficiente para ${nombre}`, 'warning');
      return;
    }
    existe.cantidad++;
  } else {
    carrito.push({ id, nombre, precio, cantidad: 1, stock });
  }
  
  actualizar();
  mostrarAlerta(` ${nombre} agregado al carrito`, 'success');
}

/**
 * Actualizar vista del carrito
 */
function actualizar() {
  const container = document.getElementById('carrito');
  const totalElement = document.getElementById('total');
  
  container.innerHTML = '';
  
  if (carrito.length === 0) {
    container.innerHTML = `
      <div class="text-center text-muted carrito-vacio">
        <i class="bi bi-cart-x"></i>
        <p class="mt-3 mb-0">El carrito está vacío</p>
        <small>Selecciona productos para agregar</small>
      </div>
    `;
    totalElement.textContent = '$0';
    return;
  }
  
  let html = '';
  let total = 0;
  
  carrito.forEach(item => {
    const subtotal = item.precio * item.cantidad;
    total += subtotal;
    
    html += `
      <div class="border rounded p-3 mb-2 carrito-item">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <strong class="text-truncate me-2" style="font-size: 0.95rem;">${item.nombre}</strong>
          <button type="button" class="btn btn-sm btn-danger" onclick="eliminar(${item.id})" title="Eliminar">
            <i class="bi bi-trash"></i>
          </button>
        </div>
        <div class="d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center gap-2">
            <button type="button" class="btn btn-sm btn-outline-secondary btn-cantidad" onclick="cambiar(${item.id}, -1)">
              <i class="bi bi-dash"></i>
            </button>
            <span class="cantidad-display">${item.cantidad}</span>
            <button type="button" class="btn btn-sm btn-outline-secondary btn-cantidad" onclick="cambiar(${item.id}, 1)">
              <i class="bi bi-plus"></i>
            </button>
          </div>
          <div class="text-end">
            <div class="text-muted small">$${item.precio.toLocaleString('es-CO')} c/u</div>
            <strong class="text-success">$${subtotal.toLocaleString('es-CO')}</strong>
          </div>
        </div>
        <input type="hidden" name="producto_id[]" value="${item.id}">
        <input type="hidden" name="cantidad[]" value="${item.cantidad}">
      </div>
    `;
  });
  
  container.innerHTML = html;
  totalElement.textContent = `$${total.toLocaleString('es-CO')}`;
}

/**
 * Cambiar cantidad de un producto
 */
function cambiar(id, cambio) {
  const item = carrito.find(i => i.id === id);
  if (!item) return;
  
  const nueva = item.cantidad + cambio;
  
  if (nueva <= 0) {
    eliminar(id);
    return;
  }
  
  if (nueva > item.stock) {
    mostrarAlerta(` Stock máximo: ${item.stock} unidades`, 'warning');
    return;
  }
  
  item.cantidad = nueva;
  actualizar();
}

/**
 * Eliminar producto del carrito
 */
function eliminar(id) {
  const item = carrito.find(i => i.id === id);
  if (!item) return;
  
  carrito = carrito.filter(item => item.id !== id);
  actualizar();
  mostrarAlerta(` ${item.nombre} eliminado del carrito`, 'info');
}

/**
 * Limpiar todo el carrito
 */
function limpiar() {
  if (carrito.length === 0) {
    mostrarAlerta(' El carrito ya está vacío', 'warning');
    return;
  }
  
  if (confirm('¿Estás seguro de vaciar el carrito?')) {
    carrito = [];
    actualizar();
    mostrarAlerta(' Carrito vaciado', 'info');
  }
}

/**
 * Filtrar productos por búsqueda y categoría
 */
function filtrar() {
  const busqueda = document.getElementById('buscar').value.toLowerCase();
  const categoria = document.getElementById('filtro').value;
  
  document.querySelectorAll('.producto-card').forEach(card => {
    const nombre = card.dataset.nombre.toLowerCase();
    const cat = card.dataset.categoria;
    
    const matchBusqueda = nombre.includes(busqueda);
    const matchCategoria = !categoria || cat === categoria;
    
    card.style.display = (matchBusqueda && matchCategoria) ? 'block' : 'none';
  });
}

/**
 * Mostrar alertas/notificaciones
 */
function mostrarAlerta(mensaje, tipo = 'info') {
  // Crear elemento de alerta
  const alerta = document.createElement('div');
  alerta.className = `alert alert-${tipo} alert-dismissible fade show position-fixed`;
  alerta.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
  alerta.innerHTML = `
    ${mensaje}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
  
  document.body.appendChild(alerta);
  
  // Auto-eliminar después de 3 segundos
  setTimeout(() => {
    alerta.classList.remove('show');
    setTimeout(() => alerta.remove(), 150);
  }, 3000);
}

/**
 * Validar formulario antes de enviar
 */
function validarVenta(event) {
  if (carrito.length === 0) {
    event.preventDefault();
    mostrarAlerta('⚠️ Debes agregar al menos un producto', 'warning');
    return false;
  }
  
  const empleadoId = document.querySelector('select[name="empleado_id"]').value;
  if (!empleadoId) {
    event.preventDefault();
    mostrarAlerta('⚠️ Debes seleccionar un vendedor', 'warning');
    return false;
  }
  
  const metodoPago = document.querySelector('select[name="metodo_pago"]').value;
  if (!metodoPago) {
    event.preventDefault();
    mostrarAlerta('⚠️ Debes seleccionar un método de pago', 'warning');
    return false;
  }
  
  return true;
}

// Inicializar eventos al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  // Filtros
  const buscarInput = document.getElementById('buscar');
  const filtroSelect = document.getElementById('filtro');
  
  if (buscarInput) {
    buscarInput.addEventListener('input', filtrar);
  }
  
  if (filtroSelect) {
    filtroSelect.addEventListener('change', filtrar);
  }
  
  // Validación del formulario
  const formVenta = document.getElementById('formVenta');
  if (formVenta) {
    formVenta.addEventListener('submit', validarVenta);
  }
  
  // Inicializar carrito vacío
  actualizar();
});