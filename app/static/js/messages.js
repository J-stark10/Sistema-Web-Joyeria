function initMessages(autoHide = true, delay = 4000) {
  const messages = document.querySelectorAll(".flash");

  messages.forEach(msg => {

    const closeBtn = msg.querySelector(".flash-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        msg.remove();
      });
    }

    if (autoHide) {
      setTimeout(() => {
        msg.style.opacity = "0";
        msg.style.transform = "translateX(20px)";
        setTimeout(() => msg.remove(), 300);
      }, delay);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initMessages();
});
