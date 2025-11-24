/* ================================
   SISTEMA DE EDICIÓN DE VENTAS
   CON VALIDACIÓN DE CAMBIOS
   ================================ */

// Variable global que almacena los productos en el carrito
// Se inicializa con los datos que Django envía desde el servidor
let carrito = [];

// ============================================
// INICIALIZACIÓN AL CARGAR LA PÁGINA
// ============================================

// Este código se ejecuta cuando el DOM está completamente cargado
document.addEventListener('DOMContentLoaded', function() {
  
  // Cargar el carrito inicial con los productos de la venta existente
  // La variable carrito_inicial viene del template HTML ({{ carrito_inicial|safe }})
  if (typeof carrito_inicial !== 'undefined') {
    carrito = carrito_inicial;
  }
  
  // Actualizar la vista del carrito con los productos ya existentes
  actualizar();
  
  // Agregar validación al formulario antes de enviar
  const formVenta = document.getElementById('formVenta');
  if (formVenta) {
    formVenta.addEventListener('submit', function(e) {
      // Obtener el texto de las observaciones (motivo de edición)
      const observaciones = document.querySelector('textarea[name="observaciones"]').value.trim();
      
      // Validar que el motivo tenga al menos 10 caracteres
      if (observaciones.length < 10) {
        e.preventDefault(); // Detener el envío del formulario
        alert(' Debe escribir un motivo detallado (mínimo 10 caracteres) para editar esta venta.');
        return false;
      }
      
      // Confirmar antes de guardar los cambios
      if (!confirm('¿Está seguro de guardar estos cambios? Esta acción quedará registrada en el sistema.')) {
        e.preventDefault(); // Cancelar si el usuario no confirma
        return false;
      }
    });
  }
});


// ============================================
// AGREGAR PRODUCTO AL CARRITO
// ============================================

/**
 * Agrega un producto al carrito o incrementa su cantidad si ya existe
 * @param {number} id - ID del producto
 * @param {string} nombre - Nombre del producto
 * @param {number} precio - Precio unitario del producto
 * @param {number} stock - Stock disponible del producto
 */
function agregar(id, nombre, precio, stock) {
  // Buscar si el producto ya está en el carrito
  const existe = carrito.find(item => item.id === id);
  
  if (existe) {
    // Si el producto ya está en el carrito
    
    // Verificar que no se exceda el stock disponible
    if (existe.cantidad >= stock) {
      alert(` Stock insuficiente para ${nombre}`);
      return; // Salir sin agregar más unidades
    }
    
    // Incrementar la cantidad en 1
    existe.cantidad++;
  } else {
    // Si el producto NO está en el carrito, agregarlo
    carrito.push({ 
      id: id, 
      nombre: nombre, 
      precio: precio, 
      cantidad: 1, 
      stock: stock 
    });
  }
  
  // Actualizar la vista del carrito con los nuevos datos
  actualizar();
}


// ============================================
// ACTUALIZAR VISTA DEL CARRITO
// ============================================

/**
 * Actualiza el HTML del carrito y el total de la venta
 * Esta función se ejecuta cada vez que se modifica el carrito
 */
function actualizar() {
  // Obtener el contenedor donde se mostrarán los productos
  const container = document.getElementById('carrito');
  
  // Obtener el elemento donde se muestra el total
  const totalElement = document.getElementById('total');
  
  // Limpiar el contenido anterior
  container.innerHTML = '';
  
  // Si el carrito está vacío, mostrar mensaje
  if (carrito.length === 0) {
    container.innerHTML = `
      <div class="text-center text-muted py-4 carrito-vacio">
        <i class="bi bi-cart-x display-4"></i>
        <p class="mt-2">Carrito vacío</p>
      </div>
    `;
    totalElement.textContent = '$0'; // Total en cero
    return; // Salir de la función
  }
  
  // Construir el HTML de cada producto en el carrito
  let html = '';
  let total = 0; // Inicializar el total
  
  // Recorrer cada producto del carrito
  carrito.forEach(item => {
    // Calcular el subtotal del producto (precio × cantidad)
    const subtotal = item.precio * item.cantidad;
    
    // Sumar al total general
    total += subtotal;
    
    // Construir el HTML de este producto
    html += `
      <div class="border rounded p-2 mb-2 bg-light carrito-item">
        <!-- Nombre del producto y botón eliminar -->
        <div class="d-flex justify-content-between align-items-center mb-2">
          <strong class="text-truncate me-2" style="font-size: 0.95rem;">${item.nombre}</strong>
          <button type="button" class="btn btn-sm btn-danger" onclick="eliminar(${item.id})" title="Eliminar">
            <i class="bi bi-trash"></i>
          </button>
        </div>
        
        <!-- Controles de cantidad y precio -->
        <div class="d-flex justify-content-between align-items-center">
          <!-- Botones de cantidad -->
          <div class="d-flex align-items-center gap-2">
            <button type="button" class="btn btn-sm btn-outline-secondary btn-cantidad" onclick="cambiar(${item.id}, -1)">
              <i class="bi bi-dash"></i>
            </button>
            <span class="cantidad-display">${item.cantidad}</span>
            <button type="button" class="btn btn-sm btn-outline-secondary btn-cantidad" onclick="cambiar(${item.id}, 1)">
              <i class="bi bi-plus"></i>
            </button>
          </div>
          
          <!-- Precio unitario y subtotal -->
          <div class="text-end">
            <div class="text-muted small">$${item.precio.toLocaleString('es-CO')} c/u</div>
            <strong class="text-success">$${subtotal.toLocaleString('es-CO')}</strong>
          </div>
        </div>
        
        <!-- Campos ocultos para enviar al servidor -->
        <input type="hidden" name="producto_id[]" value="${item.id}">
        <input type="hidden" name="cantidad[]" value="${item.cantidad}">
      </div>
    `;
  });
  
  // Insertar el HTML generado en el contenedor
  container.innerHTML = html;
  
  // Actualizar el total con formato de moneda colombiana
  totalElement.textContent = `$${total.toLocaleString('es-CO')}`;
}


// ============================================
// CAMBIAR CANTIDAD DE UN PRODUCTO
// ============================================

/**
 * Incrementa o decrementa la cantidad de un producto
 * @param {number} id - ID del producto
 * @param {number} cambio - +1 para incrementar, -1 para decrementar
 */
function cambiar(id, cambio) {
  // Buscar el producto en el carrito
  const item = carrito.find(i => i.id === id);
  
  // Si no se encuentra, salir
  if (!item) return;
  
  // Calcular la nueva cantidad
  const nueva = item.cantidad + cambio;
  
  // Si la nueva cantidad es 0 o menor, eliminar el producto
  if (nueva <= 0) {
    eliminar(id);
    return;
  }
  
  // Verificar que no se exceda el stock
  if (nueva > item.stock) {
    alert(` Stock máximo: ${item.stock} unidades`);
    return; // No permitir cantidades mayores al stock
  }
  
  // Actualizar la cantidad del producto
  item.cantidad = nueva;
  
  // Actualizar la vista
  actualizar();
}


// ============================================
// ELIMINAR PRODUCTO DEL CARRITO
// ============================================

/**
 * Elimina un producto del carrito después de confirmar
 * @param {number} id - ID del producto a eliminar
 */
function eliminar(id) {
  // Filtrar el carrito para remover el producto con ese ID
  carrito = carrito.filter(item => item.id !== id);
    
    // Actualizar la vista
    actualizar();
  
}


// ============================================
// LIMPIAR TODO EL CARRITO
// ============================================

/**
 * Vacía completamente el carrito después de confirmar
 */
function limpiar() {
  // Verificar que el carrito no esté vacío
  if (carrito.length > 0) {
    // Confirmar antes de vaciar
    if (confirm(' ¿Vaciar completamente el carrito?')) {
      // Vaciar el array del carrito
      carrito = [];
      
      // Actualizar la vista
      actualizar();
    }
  }
}


// ============================================
// FILTRAR PRODUCTOS
// ============================================

/**
 * Filtra los productos mostrados según búsqueda y categoría
 * Esta función se ejecuta cuando el usuario escribe en el buscador
 * o cambia el selector de categoría
 */
function filtrar() {
  // Obtener el texto de búsqueda y convertirlo a minúsculas
  const busqueda = document.getElementById('buscar').value.toLowerCase();
  
  // Obtener la categoría seleccionada
  const categoria = document.getElementById('filtro').value;
  
  // Recorrer todas las tarjetas de productos
  document.querySelectorAll('.producto-card').forEach(card => {
    // Obtener los atributos data-nombre y data-categoria
    const nombre = card.dataset.nombre;
    const cat = card.dataset.categoria;
    
    // Verificar si el producto coincide con los filtros
    const matchNombre = nombre.includes(busqueda);
    const matchCategoria = !categoria || cat === categoria;
    
    // Mostrar u ocultar según coincidencia
    if (matchNombre && matchCategoria) {
      card.classList.remove('d-none'); // Mostrar
    } else {
      card.classList.add('d-none'); // Ocultar
    }
  });
}


// ============================================
// INICIALIZAR FILTROS
// ============================================

// Conectar el campo de búsqueda al filtro
const buscarInput = document.getElementById('buscar');
if (buscarInput) {
  buscarInput.addEventListener('input', filtrar);
}

// Conectar el selector de categoría al filtro
const filtroSelect = document.getElementById('filtro');
if (filtroSelect) {
  filtroSelect.addEventListener('change', filtrar);
}