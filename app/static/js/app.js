/* =========================
   THEME : DARK - LIGTH
========================= */

function toggleTheme() {
  const html    = document.documentElement;
  const current = html.getAttribute('data-theme') || 'dark';
  const next    = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateThemeIcons(next);
}

/* =========================
   ESTADO GLOBAL
========================= */

let sidebarCollapsed = localStorage.getItem('sidebar') === 'collapsed';
let userMenuOpen = false;

/* =========================
   INIT
========================= */

document.addEventListener('DOMContentLoaded', function () {

    const app = document.getElementById('app');

    // aplicar sidebar estado inicial
    if (sidebarCollapsed) {
        app?.classList.add('sidebar-collapsed');
    }

    // restaurar submenús
    document.querySelectorAll('[id^="submenu-"]').forEach(submenu => {

        const btn = document.querySelector(`[onclick*="${submenu.id}"]`);
        const chevron = btn?.querySelector('.submenu-chevron');

        if (sidebarCollapsed) {
            submenu.style.maxHeight = '0';
            if (chevron) chevron.style.transform = 'rotate(0deg)';
            return;
        }

        const state = localStorage.getItem(submenu.id);

        if (state === 'open') {
            submenu.style.maxHeight = submenu.scrollHeight + 'px';
            if (chevron) chevron.style.transform = 'rotate(180deg)';
        } else {
            submenu.style.maxHeight = '0';
            if (chevron) chevron.style.transform = 'rotate(0deg)';
        }
    });
});


/* =========================
   SIDEBAR
========================= */

function toggleSidebar() {

    const app = document.getElementById('app');
    if (!app) return;

    sidebarCollapsed = !sidebarCollapsed;

    app.classList.toggle('sidebar-collapsed', sidebarCollapsed);

    localStorage.setItem(
        'sidebar',
        sidebarCollapsed ? 'collapsed' : 'expanded'
    );

    // cerrar submenús si colapsa
    if (sidebarCollapsed) {

        document.querySelectorAll('[id^="submenu-"]').forEach(sub => {
            sub.style.maxHeight = '0';
        });

        document.querySelectorAll('.submenu-chevron').forEach(ch => {
            ch.style.transform = 'rotate(0deg)';
        });
    }
}


/* =========================
   SUBMENU (IMPORTANTE FIX)
========================= */

function toggleSubmenu(id, btn) {

    const app = document.getElementById('app');
    const submenu = document.getElementById(id);
    const chevron = btn.querySelector('.submenu-chevron');

    if (!submenu) return;

    // si sidebar está colapsado → primero abrirlo
    if (app?.classList.contains('sidebar-collapsed')) {
        toggleSidebar();
    }

    const isOpen = submenu.style.maxHeight &&
                   submenu.style.maxHeight !== '0px';

    if (isOpen) {
        submenu.style.maxHeight = '0';
        if (chevron) chevron.style.transform = 'rotate(0deg)';
        localStorage.setItem(id, 'closed');
    } else {
        submenu.style.maxHeight = submenu.scrollHeight + 'px';
        if (chevron) chevron.style.transform = 'rotate(180deg)';
        localStorage.setItem(id, 'open');
    }
}


/* =========================
   USER MENU
========================= */

function toggleUserMenu() {

    userMenuOpen = !userMenuOpen;

    const dropdown = document.getElementById('user-dropdown');
    const chevron = document.getElementById('user-chevron');

    dropdown?.classList.toggle('open', userMenuOpen);

    if (chevron) {
        chevron.style.transform =
            userMenuOpen ? 'rotate(180deg)' : 'rotate(0deg)';
    }
}

document.addEventListener('click', function (e) {

    const wrapper = document.getElementById('user-menu-wrapper');

    if (wrapper && !wrapper.contains(e.target) && userMenuOpen) {

        userMenuOpen = false;

        document.getElementById('user-dropdown')
            ?.classList.remove('open');

        document.getElementById('user-chevron')
            ?.style.setProperty('transform', 'rotate(0deg)');
    }
});