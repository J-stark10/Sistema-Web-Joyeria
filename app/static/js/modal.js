// =====================
// ESTADO GLOBAL
// =====================
let modalState = {
  confirmUrl: null
};

// =====================
// OPEN MODAL CONFIRM
// =====================
function openConfirmModal({ title, message, confirmUrl, type = "primary" }) {

  const modal = document.getElementById("global-modal");

  modalState.confirmUrl = confirmUrl;

  // TITLE
  document.getElementById("modal-title").innerText = title;

  // BODY
  document.getElementById("modal-body").innerHTML = `
    <p style="font-size:0.95rem;">
      ${message}
    </p>
  `;

  // BOTÓN
  const btn = document.getElementById("modal-confirm-btn");

  // limpiar estilos anteriores
  btn.classList.remove("btn-primary", "btn-danger", "btn-ghost");

  // 🔥 AQUÍ USAMOS TU SISTEMA REAL
  const finalType = type === "danger" ? "danger" : "primary";

  btn.classList.add("btn", `btn-${finalType}`);

  // texto dinámico más limpio
  btn.innerText =
    finalType === "danger"
      ? "Sí, confirmar"
      : "Confirmar";

  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

// =====================
// CONFIRM ACTION
// =====================
function handleConfirm() {

  if (!modalState.confirmUrl) return;

  const btn = document.getElementById("modal-confirm-btn");

  btn.classList.add("loading");
  btn.innerText = "Procesando...";

  window.location.href = modalState.confirmUrl;
}

// =====================
// CLOSE MODAL
// =====================
function closeModal() {

  const modal = document.getElementById("global-modal");

  modal.classList.add("hidden");

  document.body.style.overflow = "auto";

  modalState.confirmUrl = null;
}

// =====================
// EVENTS
// =====================

// click fuera
document.addEventListener("click", (e) => {
  const modal = document.getElementById("global-modal");
  if (e.target === modal) closeModal();
});

// ESC
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});