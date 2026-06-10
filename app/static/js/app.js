/* ============================================================
   Joyería El Illimani — App JS
   ============================================================ */

/* ── Tema ── */
(function () {
  const saved = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeIcons(saved);
})();

function updateThemeIcons(theme) {
  const sun  = document.getElementById('icon-sun');
  const moon = document.getElementById('icon-moon');
  if (!sun || !moon) return;
  if (theme === 'dark') {
    sun.style.display  = 'none';
    moon.style.display = 'block';
  } else {
    sun.style.display  = 'block';
    moon.style.display = 'none';
  }
}

function toggleTheme() {
  const html    = document.documentElement;
  const current = html.getAttribute('data-theme') || 'dark';
  const next    = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateThemeIcons(next);
}

/* ── Sidebar ── */
let sidebarCollapsed = localStorage.getItem('sidebar') === 'collapsed';

(function () {
  if (sidebarCollapsed) {
    document.getElementById('app')?.classList.add('sidebar-collapsed');
  }
})();

function toggleSidebar() {
  const app = document.getElementById('app');
  if (!app) return;

  sidebarCollapsed = !sidebarCollapsed;
  app.classList.toggle('sidebar-collapsed', sidebarCollapsed);
  localStorage.setItem('sidebar', sidebarCollapsed ? 'collapsed' : 'expanded');

  // Cerrar submenús al colapsar
  if (sidebarCollapsed) {
    document.querySelectorAll('[id^="submenu-"]').forEach(function (sub) {
      sub.style.maxHeight = '0';
    });
    document.querySelectorAll('.submenu-chevron').forEach(function (ch) {
      ch.style.transform = 'rotate(0deg)';
    });
  }
}

function openSidebar() {
  document.getElementById('sidebar')?.classList.add('open');
  document.getElementById('sidebar-overlay').style.display = 'block';
}

function closeSidebar() {
  document.getElementById('sidebar')?.classList.remove('open');
  document.getElementById('sidebar-overlay').style.display = 'none';
}

/* ── Dropdown usuario ── */
let userMenuOpen = false;

function toggleUserMenu() {
  userMenuOpen = !userMenuOpen;
  const dropdown = document.getElementById('user-dropdown');
  const chevron  = document.getElementById('user-chevron');
  if (!dropdown) return;
  dropdown.classList.toggle('open', userMenuOpen);
  if (chevron) {
    chevron.style.transform = userMenuOpen ? 'rotate(180deg)' : 'rotate(0deg)';
  }
}

// Cerrar al hacer clic fuera
document.addEventListener('click', function (e) {
  const wrapper = document.getElementById('user-menu-wrapper');
  if (wrapper && !wrapper.contains(e.target) && userMenuOpen) {
    userMenuOpen = false;
    document.getElementById('user-dropdown')?.classList.remove('open');
    const chevron = document.getElementById('user-chevron');
    if (chevron) chevron.style.transform = 'rotate(0deg)';
  }
});

/* ── Auto-dismiss flash alerts ── */
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      el.style.transition = 'opacity 0.4s ease, max-height 0.4s ease';
      el.style.opacity = '0';
      el.style.maxHeight = '0';
      el.style.overflow = 'hidden';
      setTimeout(function () { el.remove(); }, 400);
    });
  }, 4500);
});

/* ── Búsqueda global (Cmd/Ctrl+K) ── */
document.addEventListener('keydown', function (e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    const input = document.querySelector('.search-bar input');
    input?.focus();
  }
});

/* ── Confirm delete helper ── */
function confirmDelete(form, message) {
  if (confirm(message || '¿Seguro que deseas eliminar este registro?')) {
    form.submit();
  }
}


function toggleSubmenu(id, btn) {
  if (sidebarCollapsed) {
    toggleSidebar(); // expande el sidebar primero
    // pequeño delay para que la animación termine antes de abrir el submenú
    setTimeout(function () {
      openSubmenu(id, btn);
    }, 250);
    return;
  }

  const submenu = document.getElementById(id);
  const chevron = btn.querySelector('.submenu-chevron');
  const isOpen  = submenu.style.maxHeight !== '0px' && submenu.style.maxHeight !== '';

  if (isOpen) {
    submenu.style.maxHeight = '0';
    chevron && chevron.style.setProperty('transform', 'rotate(0deg)');
  } else {
    openSubmenu(id, btn);
  }
}

function openSubmenu(id, btn) {
  const submenu = document.getElementById(id);
  const chevron = btn.querySelector('.submenu-chevron');
  submenu.style.maxHeight = submenu.scrollHeight + 'px';
  chevron && chevron.style.setProperty('transform', 'rotate(180deg)');
}