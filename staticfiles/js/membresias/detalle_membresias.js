/**
 * ========================================
 * SCRIPT: GRÁFICO DE PROGRESO DE MEMBRESÍA
 * ========================================
 * Genera un gráfico circular (doughnut) con Chart.js
 * que muestra el progreso de consumo de una membresía
 */

document.addEventListener('DOMContentLoaded', function() {
    // 1. VERIFICAR QUE EL CANVAS EXISTA
    const canvas = document.getElementById('progressChart');
    if (!canvas) {
        console.error('❌ Canvas no encontrado');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('❌ No se pudo obtener el contexto 2D');
        return;
    }
    
    // 2. OBTENER PROGRESO DESDE EL ATRIBUTO data-progreso
    let progreso = parseFloat(canvas.getAttribute('data-progreso')) || 0;
    
    // Asegurar que esté entre 0 y 100
    progreso = Math.max(0, Math.min(100, progreso));
    
    const restante = 100 - progreso;
    
    console.log('📊 Progreso obtenido:', progreso);
    
    // 3. DETERMINAR COLOR BASADO EN EL PROGRESO
    let color;
    let colorTexto;
    
    if (progreso < 30) {
        color = '#047857';        // Verde oscuro (poca membresía consumida)
        colorTexto = '#047857';
    } else if (progreso < 70) {
        color = '#d97706';        // Amarillo/Naranja oscuro (mitad de membresía)
        colorTexto = '#d97706';
    } else if (progreso < 90) {
        color = '#b45309';        // Naranja oscuro (casi vencida)
        colorTexto = '#b45309';
    } else {
        color = '#b91c1c';        // Rojo oscuro (muy próxima a vencer)
        colorTexto = '#b91c1c';
    }
    
    // 4. CREAR EL GRÁFICO
    try {
        const chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [progreso, restante],
                    backgroundColor: [
                        color,         // Color dinámico según progreso
                        '#e9ecef'      // Gris claro para la parte restante
                    ],
                    borderWidth: 0,
                    borderRadius: 4,    
                    cutout: '70%',      // Grosor del anillo
                }]
            },
            options: {
                responsive: false,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 1500,
                    easing: 'easeInOutQuart'
                }
            }
        });
        
        // 5. ACTUALIZAR EL TEXTO CENTRAL
        const textElement = document.getElementById('chartCenterText');
        if (textElement) {
            textElement.style.color = colorTexto;
            textElement.textContent = `${progreso.toFixed(1)}%`;
        }
        
        console.log(' Gráfico cargado correctamente');
        console.log(` Progreso: ${progreso}%, Color: ${color}`);
        
    } catch (error) {
        console.error(' Error al crear el gráfico:', error);
        
        // Mostrar mensaje de error en el centro
        const textElement = document.getElementById('chartCenterText');
        if (textElement) {
            textElement.textContent = 'Error al cargar';
            textElement.style.color = '#dc3545';
            textElement.style.fontSize = '0.9rem';
        }
    }
});