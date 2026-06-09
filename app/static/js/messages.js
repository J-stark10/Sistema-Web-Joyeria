function initMessages(autoHide = true, delay = 4000) {
  const messages = document.querySelectorAll(".msg");

  messages.forEach(msg => {
    const closeBtn = msg.querySelector(".msg-close");
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
