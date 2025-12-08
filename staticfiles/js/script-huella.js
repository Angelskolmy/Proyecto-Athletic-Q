/**
 * Simula el proceso de captura de huella 3 veces seguidas
 * @param {string} inputId - ID del input donde se guardará el código
 * @param {string} inputGroupId - ID del grupo de input a ocultar
 * @param {string} animationId - ID del contenedor de animación
 */
function iniciarCapturaHuella(inputId, inputGroupId, animationId) {
  const inputGroup = document.getElementById(inputGroupId);
  const animation = document.getElementById(animationId);
  const input = document.getElementById(inputId);
  const mensaje = document.getElementById("mensajeHuella");

  inputGroup.style.display = "none";
  animation.style.display = "flex";

  let capturas = 0;
  const totalCapturas = 3;
  let huellas = [];

  function simularCaptura() {
    capturas++;
    mensaje.textContent = `Capturando huella (${capturas}/${totalCapturas})...`;

    // Mostrar animación durante 1.8 segundos
    setTimeout(() => {
      // Simula una "huella" con código aleatorio (pero con leve variación)
      const codigo = "FP-" + Math.random().toString(36).substr(2, 5).toUpperCase();
      huellas.push(codigo);

      if (capturas < totalCapturas) {
        mensaje.textContent = `Retire el dedo...`;
        setTimeout(() => {
          mensaje.textContent = `Coloque nuevamente su dedo (${capturas + 1}/${totalCapturas})`;
          simularCaptura();
        }, 1000);
      } else {
        // Comparar si las 3 huellas coinciden (simulación)
        const coincide = huellas.every((v) => v === huellas[0]);

        if (coincide) {
          const codigoHuella = huellas[0];
          input.value = codigoHuella;

          animation.innerHTML = `
            <div class="huella-success">
              <i class="bi bi-check-circle-fill"></i>
              <div>
                <h5 class="mb-0">¡Huella verificada exitosamente!</h5>
                <p class="mb-0 text-muted small">Código: ${codigoHuella}</p>
              </div>
            </div>
          `;
        } else {
          animation.innerHTML = `
            <div class="huella-success" style="background:#f8d7da; border-color:#dc3545;">
              <i class="bi bi-x-circle-fill" style="color:#dc3545;"></i>
              <div>
                <h5 class="mb-0">Error en verificación</h5>
                <p class="mb-0 text-muted small">Las huellas no coinciden, intente nuevamente.</p>
              </div>
            </div>
          `;
        }

        // Volver al estado inicial tras unos segundos
        setTimeout(() => {
          animation.style.display = "none";
          inputGroup.style.display = "block";
        }, 2500);
      }
    }, 1800);
  }

  simularCaptura();
}

/**
 * Simula la recaptura de huella (3 pasos) para el modal de editar usuario
 * @param {string} inputId - ID del input donde se guardará el código
 * @param {string} inputGroupId - ID del grupo de input a ocultar
 * @param {string} animationId - ID del contenedor de animación
 */
function iniciarRecapturaHuella(inputId, inputGroupId, animationId) {
  const inputGroup = document.getElementById(inputGroupId);
  const animation = document.getElementById(animationId);
  const input = document.getElementById(inputId);
  const mensaje = document.getElementById("editMensajeHuella");

  inputGroup.style.display = "none";
  animation.style.display = "flex";

  let capturas = 0;
  const totalCapturas = 3;
  let huellas = [];

  function simularCaptura() {
    capturas++;
    mensaje.textContent = `Capturando huella (${capturas}/${totalCapturas})...`;

    setTimeout(() => {
      // Simula un código aleatorio de huella
      const codigo = "FP-" + Math.random().toString(36).substr(2, 5).toUpperCase();
      huellas.push(codigo);

      if (capturas < totalCapturas) {
        mensaje.textContent = `Retire el dedo...`;
        setTimeout(() => {
          mensaje.textContent = `Coloque nuevamente su dedo (${capturas + 1}/${totalCapturas})`;
          simularCaptura();
        }, 1000);
      } else {
        // Verificar coincidencia (simulada)
        const coincide = huellas.every((v) => v === huellas[0]);

        if (coincide) {
          const codigoHuella = huellas[0];
          input.value = codigoHuella;

          animation.innerHTML = `
            <div class="huella-success" style="border-color:#0d6efd; background:#d1e7ff;">
              <i class="bi bi-check-circle-fill text-primary"></i>
              <div>
                <h5 class="mb-0 text-primary">¡Huella verificada exitosamente!</h5>
                <p class="mb-0 text-muted small">Código: ${codigoHuella}</p>
              </div>
            </div>
          `;
        } else {
          animation.innerHTML = `
            <div class="huella-success" style="background:#f8d7da; border-color:#dc3545;">
              <i class="bi bi-x-circle-fill" style="color:#dc3545;"></i>
              <div>
                <h5 class="mb-0">Error en verificación</h5>
                <p class="mb-0 text-muted small">Las huellas no coinciden, intente nuevamente.</p>
              </div>
            </div>
          `;
        }

        setTimeout(() => {
          animation.style.display = "none";
          inputGroup.style.display = "block";
        }, 2500);
      }
    }, 1800);
  }

  simularCaptura();
}

