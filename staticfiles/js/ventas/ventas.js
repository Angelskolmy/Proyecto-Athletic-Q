/* ================================
    SISTEMA DE CARRITO DE VENTAS
   ================================ */

// Inicializar carrito vacío
let carrito = [];

/**
 * Agregar producto al carrito
 * @param {number} id - ID del producto
 * @param {string} nombre - Nombre del producto
 * @param {number} precio - Precio del producto
 * @param {number} stock - Stock disponible del producto
 */
function agregar(id, nombre, precio, stock) {
  // Buscar si el producto ya existe en el carrito
  const existe = carrito.find(item => item.id === id);
  
  if (existe) {
    // 🔥 FIX: Leer stock REAL desde el DOM en lugar del stock guardado
    const stockBadge = document.querySelector(`#producto-${id} .badge-stock`);
    const stockDisponible = stockBadge ? parseInt(stockBadge.textContent) : stock;
    
    // Verificar si ya alcanzó el stock máximo
    if (existe.cantidad >= stockDisponible) {
      mostrarAlerta(`⚠️ Stock máximo: ${stockDisponible} unidades`, 'warning');
      return;
    }
    
    // Incrementar cantidad
    existe.cantidad++;
    // Actualizar stock guardado en memoria con el valor real
    existe.stock = stockDisponible;
  } else {
    // 🔥 FIX: Leer stock REAL desde el DOM al agregar por primera vez
    const stockBadge = document.querySelector(`#producto-${id} .badge-stock`);
    const stockDisponible = stockBadge ? parseInt(stockBadge.textContent) : stock;
    
    // Agregar nuevo producto al carrito
    carrito.push({ 
      id, 
      nombre, 
      precio, 
      cantidad: 1, 
      stock: stockDisponible // Usar el stock real del DOM
    });
  }
  
  // Actualizar la vista del carrito
  actualizar();
  
  // Mostrar mensaje de éxito
  mostrarAlerta(`✅ ${nombre} agregado al carrito`, 'success');
}

/**
 * Actualizar vista del carrito
 * Renderiza todos los productos en el carrito y calcula el total
 */
function actualizar() {
  // Obtener elementos del DOM
  const container = document.getElementById('carrito');
  const totalElement = document.getElementById('total');
  
  // Limpiar contenedor
  container.innerHTML = '';
  
  // Si el carrito está vacío, mostrar mensaje
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
  
  // Variables para HTML y total
  let html = '';
  let total = 0;
  
  // Recorrer cada producto en el carrito
  carrito.forEach(item => {
    // Calcular subtotal del producto
    const subtotal = item.precio * item.cantidad;
    total += subtotal;
    
    // Construir HTML del producto
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
  
  // Actualizar el DOM
  container.innerHTML = html;
  totalElement.textContent = `$${total.toLocaleString('es-CO')}`;
}

/**
 * Cambiar cantidad de un producto en el carrito
 * @param {number} id - ID del producto
 * @param {number} cambio - Cantidad a sumar o restar (ej: 1, -1)
 */
function cambiar(id, cambio) {
  // Buscar el producto en el carrito
  const item = carrito.find(i => i.id === id);
  if (!item) return;
  
  // Calcular nueva cantidad
  const nueva = item.cantidad + cambio;
  
  // Si la nueva cantidad es 0 o menos, eliminar del carrito
  if (nueva <= 0) {
    eliminar(id);
    return;
  }
  
  // 🔥 FIX: Leer stock REAL desde el DOM antes de validar
  const stockBadge = document.querySelector(`#producto-${id} .badge-stock`);
  const stockDisponible = stockBadge ? parseInt(stockBadge.textContent) : item.stock;
  
  // Validar que no exceda el stock disponible
  if (nueva > stockDisponible) {
    mostrarAlerta(`⚠️ Stock máximo: ${stockDisponible} unidades`, 'warning');
    return;
  }
  
  // Actualizar cantidad en el carrito
  item.cantidad = nueva;
  // Actualizar stock guardado en memoria con el valor real
  item.stock = stockDisponible;
  
  // Actualizar vista
  actualizar();
}

/**
 * Eliminar producto del carrito
 * @param {number} id - ID del producto a eliminar
 */
function eliminar(id) {
  // Buscar el producto
  const item = carrito.find(i => i.id === id);
  if (!item) return;
  
  // Eliminar del array
  carrito = carrito.filter(item => item.id !== id);
  
  // Actualizar vista
  actualizar();
  
  // Mostrar mensaje
  mostrarAlerta(`🗑️ ${item.nombre} eliminado del carrito`, 'info');
}

/**
 * Limpiar todo el carrito
 * Pide confirmación antes de vaciar
 */
function limpiar() {
  // Si ya está vacío, mostrar advertencia
  if (carrito.length === 0) {
    mostrarAlerta('ℹ️ El carrito ya está vacío', 'warning');
    return;
  }
  
  // Pedir confirmación
  if (confirm('¿Estás seguro de vaciar el carrito?')) {
    // Vaciar carrito
    carrito = [];
    
    // Actualizar vista
    actualizar();
    
    // Mostrar mensaje
    mostrarAlerta('🧹 Carrito vaciado', 'info');
  }
}

/**
 * Filtrar productos por búsqueda y categoría
 * Oculta/muestra productos según los filtros aplicados
 */
function filtrar() {
  // Obtener valores de los filtros
  const busqueda = document.getElementById('buscar').value.toLowerCase();
  const categoria = document.getElementById('filtro').value;
  
  // Recorrer todas las tarjetas de productos
  document.querySelectorAll('.producto-card').forEach(card => {
    // Obtener datos del producto
    const nombre = card.dataset.nombre.toLowerCase();
    const cat = card.dataset.categoria;
    
    // Verificar coincidencias
    const matchBusqueda = nombre.includes(busqueda);
    const matchCategoria = !categoria || cat === categoria;
    
    // Mostrar/ocultar según coincidencias
    card.style.display = (matchBusqueda && matchCategoria) ? 'block' : 'none';
  });
}

/**
 * Mostrar alertas/notificaciones temporales
 * @param {string} mensaje - Texto a mostrar
 * @param {string} tipo - Tipo de alerta: success, warning, danger, info
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
  
  // Agregar al body
  document.body.appendChild(alerta);
  
  // Auto-eliminar después de 3 segundos
  setTimeout(() => {
    alerta.classList.remove('show');
    setTimeout(() => alerta.remove(), 150);
  }, 3000);
}

/**
 * Validar formulario antes de enviar
 * @param {Event} event - Evento del formulario
 * @returns {boolean} - true si es válido, false si no
 */
function validarVenta(event) {
  // Validar que el carrito no esté vacío
  if (carrito.length === 0) {
    event.preventDefault();
    mostrarAlerta('⚠️ Debes agregar al menos un producto', 'warning');
    return false;
  }
  
  // Validar que se haya seleccionado un vendedor
  const empleadoId = document.querySelector('select[name="empleado_id"]').value;
  if (!empleadoId) {
    event.preventDefault();
    mostrarAlerta('⚠️ Debes seleccionar un vendedor', 'warning');
    return false;
  }
  
  // Validar que se haya seleccionado un método de pago
  const metodoPago = document.querySelector('select[name="metodo_pago"]').value;
  if (!metodoPago) {
    event.preventDefault();
    mostrarAlerta('⚠️ Debes seleccionar un método de pago', 'warning');
    return false;
  }
  
  // Todas las validaciones pasaron
  return true;
}

/**
 * Inicializar eventos al cargar la página
 * Se ejecuta cuando el DOM está completamente cargado
 */
document.addEventListener('DOMContentLoaded', function() {
  // Evento para el buscador de productos
  const buscarInput = document.getElementById('buscar');
  if (buscarInput) {
    buscarInput.addEventListener('input', filtrar);
  }
  
  // Evento para el filtro de categorías
  const filtroSelect = document.getElementById('filtro');
  if (filtroSelect) {
    filtroSelect.addEventListener('change', filtrar);
  }
  
  // Evento para validar el formulario al enviar
  const formVenta = document.getElementById('formVenta');
  if (formVenta) {
    formVenta.addEventListener('submit', validarVenta);
  }
  
  // Inicializar carrito vacío al cargar
  actualizar();
});