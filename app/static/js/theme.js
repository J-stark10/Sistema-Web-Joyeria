/**
 * theme.js — Joyería El Illimani
 * Maneja el toggle light/dark persistente en localStorage.
 * Se carga en el <head> para evitar flash de tema incorrecto.
 */

(function () {
  const STORAGE_KEY = 'illimani-theme';

  function getTheme() {
    return localStorage.getItem(STORAGE_KEY) || 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }

  function toggleTheme() {
    const current = getTheme();
    applyTheme(current === 'dark' ? 'light' : 'dark');
  }

  // Aplicar tema guardado inmediatamente (antes de pintar)
  applyTheme(getTheme());

  // Exponer función al HTML
  window.toggleTheme = toggleTheme;

  // Auto-cerrar flash messages después de 4 segundos
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.flash').forEach(function (el) {
      setTimeout(function () {
        el.style.transition = 'opacity 0.4s';
        el.style.opacity = '0';
        setTimeout(function () { el.remove(); }, 400);
      }, 4000);
    });

    // Botón cerrar manual
    document.querySelectorAll('.flash-close').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const flash = btn.closest('.flash');
        flash.style.transition = 'opacity 0.3s';
        flash.style.opacity = '0';
        setTimeout(function () { flash.remove(); }, 300);
      });
    });
  });
})();
