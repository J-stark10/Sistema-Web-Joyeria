class Paginator {
  constructor({ tableId, paginatorId, pageSize = 10, totalItems = null }) {
    this.table       = document.getElementById(tableId);
    this.wrapper     = document.getElementById(paginatorId);
    this.pageSize    = pageSize;
    this.currentPage = 1;
    this.totalItems  = totalItems;

    this._filteredRows = [];
    this._preFilterCount = 0;

    if (!this.table || !this.wrapper) return;

    this.render();
  }

  get totalPages() {
    return Math.max(1, Math.ceil(this._preFilterCount / this.pageSize));
  }

  refresh(opts) {
    if (opts && opts.totalItems !== undefined) {
      this.totalItems = opts.totalItems;
    }

    const allRows = [...this.table.querySelectorAll('tbody tr[data-page-row]')];
    this._filteredRows = allRows.filter(r => r.style.display !== 'none');
    this._preFilterCount = this.totalItems !== null ? this.totalItems : this._filteredRows.length;

    if (this.currentPage > this.totalPages) {
      this.currentPage = this.totalPages;
    }

    this._applyPage();
    this._renderControls();
  }

  render() {
    this._markRows();

    const allRows = [...this.table.querySelectorAll('tbody tr[data-page-row]')];
    this._filteredRows = allRows.filter(r => r.style.display !== 'none');
    this._preFilterCount = this.totalItems !== null ? this.totalItems : this._filteredRows.length;

    this.currentPage = 1;
    this._applyPage();
    this._renderControls();
  }

  _applyPage() {
    const start = (this.currentPage - 1) * this.pageSize;
    const end   = Math.min(start + this.pageSize, this._filteredRows.length);

    this._filteredRows.forEach((row, idx) => {
      row.style.display = (idx >= start && idx < end) ? '' : 'none';
    });
  }

  _goTo(page) {
    if (page < 1 || page > this.totalPages) return;
    this.currentPage = page;
    this._applyPage();
    this._renderControls();
  }

  _markRows() {
    this.table.querySelectorAll('tbody tr').forEach(row => {
      const hasData = [...row.attributes].some(
        a => a.name.startsWith('data-') && a.name !== 'data-page-row'
      );
      if (hasData) row.setAttribute('data-page-row', '');
    });
  }

  _renderControls() {
    if (!this.wrapper) return;

    const current = this.currentPage;
    const total   = this.totalPages;
    const count   = this._preFilterCount;

    if (count === 0 || total === 0) {
      this.wrapper.innerHTML = '';
      return;
    }

    const from = (current - 1) * this.pageSize + 1;
    const to   = Math.min(current * this.pageSize, count);

    const info = document.createElement('span');
    info.className = 'pg-info';
    info.textContent = `Mostrando del ${from} al ${to} de ${count} resultados`;

    const nav = document.createElement('div');
    nav.className = 'pg-nav';

    const btnPrev = this._btn(
      `<svg xmlns="http://www.w3.org/2000/svg" class="pg-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>`,
      () => this._goTo(current - 1),
      current === 1,
      'Página anterior'
    );

    const btnNext = this._btn(
      `<svg xmlns="http://www.w3.org/2000/svg" class="pg-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>`,
      () => this._goTo(current + 1),
      current === total,
      'Página siguiente'
    );

    nav.appendChild(btnPrev);

    const visiblePages = this._getVisiblePages(current, total);
    visiblePages.forEach(p => {
      if (p === '…') {
        const span = document.createElement('span');
        span.className = 'pg-ellipsis';
        span.textContent = '…';
        span.setAttribute('aria-hidden', 'true');
        nav.appendChild(span);
        return;
      }
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = p === current ? 'pg-btn pg-btn-active' : 'pg-btn';
      btn.textContent = String(p);
      if (p === current) {
        btn.setAttribute('aria-current', 'page');
      }
      btn.addEventListener('click', () => this._goTo(p));
      nav.appendChild(btn);
    });

    nav.appendChild(btnNext);

    this.wrapper.innerHTML = '';
    this.wrapper.appendChild(info);
    this.wrapper.appendChild(nav);
  }

  _btn(html, onClick, disabled, ariaLabel) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'pg-btn';
    btn.innerHTML = html;
    btn.disabled = disabled;
    btn.setAttribute('aria-label', ariaLabel);
    if (disabled) btn.setAttribute('aria-disabled', 'true');
    if (!disabled) btn.addEventListener('click', onClick);
    return btn;
  }

  _getVisiblePages(current, total) {
    if (total <= 7) {
      return Array.from({ length: total }, (_, i) => i + 1);
    }

    if (current <= 3) {
      const pages = [1, 2, 3, 4, 5];
      pages.push('…', total);
      return pages;
    }

    if (current >= total - 2) {
      const pages = [1, '…'];
      for (let i = total - 4; i <= total; i++) pages.push(i);
      return pages;
    }

    return [1, '…', current - 1, current, current + 1, '…', total];
  }
}
