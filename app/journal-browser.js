window.DPRJournalBrowser = (function () {
  const stateByEl = new WeakMap();

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function norm(value) {
    return String(value == null ? '' : value).trim();
  }

  function parseDate(value) {
    const text = norm(value);
    if (!text) return null;
    const d = new Date(text);
    if (Number.isNaN(d.getTime())) return null;
    return d;
  }

  function yearOf(row) {
    const d = parseDate(row.published);
    return d ? String(d.getUTCFullYear()) : '';
  }

  function monthOf(row) {
    const d = parseDate(row.published);
    if (!d) return '';
    return String(d.getUTCMonth() + 1).padStart(2, '0');
  }

  function dateText(row) {
    const d = parseDate(row.published);
    if (!d) return '';
    return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}-${String(d.getUTCDate()).padStart(2, '0')}`;
  }

  function uniqueSorted(values, desc) {
    const out = Array.from(new Set(values.filter(Boolean)));
    out.sort();
    if (desc) out.reverse();
    return out;
  }

  function labelForPdf(row) {
    if (row.open_pdf_status === 'open_pdf' || row.open_pdf_available) {
      return '开放 PDF';
    }
    return '无开放 PDF';
  }

  function sourceLine(row) {
    const parts = [];
    if (row.journal_label || row.journal) parts.push(row.journal_label || row.journal);
    if (dateText(row)) parts.push(dateText(row));
    if (row.doi) parts.push(`DOI: ${row.doi}`);
    return parts.join(' · ');
  }

  function searchableText(row) {
    return [
      row.title,
      row.abstract,
      row.doi,
      row.journal,
      row.journal_label,
      row.openalex_concepts && row.openalex_concepts.join(' '),
      row.semantic_fields_of_study && row.semantic_fields_of_study.join(' '),
    ]
      .map(norm)
      .join(' ')
      .toLowerCase();
  }

  function filterRows(rows, filters) {
    const query = norm(filters.query).toLowerCase();
    return rows.filter((row) => {
      if (filters.year && yearOf(row) !== filters.year) return false;
      if (filters.month && monthOf(row) !== filters.month) return false;
      if (filters.journal && norm(row.journal_label || row.journal_key || row.journal) !== filters.journal) return false;
      if (filters.pdf === 'open' && !(row.open_pdf_status === 'open_pdf' || row.open_pdf_available)) return false;
      if (filters.pdf === 'missing' && (row.open_pdf_status === 'open_pdf' || row.open_pdf_available)) return false;
      if (query && !searchableText(row).includes(query)) return false;
      return true;
    });
  }

  function renderOptions(values, selected, allLabel) {
    return [`<option value="">${escapeHtml(allLabel)}</option>`]
      .concat(
        values.map((value) => {
          const active = value === selected ? ' selected' : '';
          return `<option value="${escapeHtml(value)}"${active}>${escapeHtml(value)}</option>`;
        }),
      )
      .join('');
  }

  function renderCard(row) {
    const title = norm(row.title) || '(Untitled)';
    const abstract = norm(row.abstract);
    const link = norm(row.abs_url || row.link || (row.doi ? `https://doi.org/${row.doi}` : ''));
    const pdf = norm(row.pdf_url);
    const concepts = Array.isArray(row.openalex_concepts) ? row.openalex_concepts.slice(0, 5) : [];
    return `
      <article class="dpr-journal-card">
        <div class="dpr-journal-card-head">
          <span class="dpr-journal-badge">${escapeHtml(row.journal_label || row.journal || 'Journal')}</span>
          <span class="dpr-journal-pdf ${pdf ? 'is-open' : 'is-missing'}">${escapeHtml(labelForPdf(row))}</span>
        </div>
        <h3 class="dpr-journal-title">${link ? `<a href="${escapeHtml(link)}" target="_blank" rel="noopener noreferrer">${escapeHtml(title)}</a>` : escapeHtml(title)}</h3>
        <div class="dpr-journal-meta">${escapeHtml(sourceLine(row))}</div>
        ${abstract ? `<p class="dpr-journal-abstract">${escapeHtml(abstract)}</p>` : '<p class="dpr-journal-abstract is-empty">暂无摘要；仍保留期刊记录用于追踪。</p>'}
        ${concepts.length ? `<div class="dpr-journal-tags">${concepts.map((x) => `<span>${escapeHtml(x)}</span>`).join('')}</div>` : ''}
        <div class="dpr-journal-actions">
          ${link ? `<a href="${escapeHtml(link)}" target="_blank" rel="noopener noreferrer">打开论文页</a>` : ''}
          ${pdf ? `<a href="${escapeHtml(pdf)}" target="_blank" rel="noopener noreferrer">打开开放 PDF</a>` : '<span>无开放 PDF，跳过截图/图表提取</span>'}
        </div>
      </article>
    `;
  }

  function render(root) {
    const state = stateByEl.get(root);
    if (!state) return;
    const rows = state.rows || [];
    const filters = state.filters || {};
    const journals = uniqueSorted(rows.map((row) => norm(row.journal_label || row.journal_key || row.journal)), false);
    const years = uniqueSorted(rows.map(yearOf), true);
    const months = uniqueSorted(rows.filter((row) => !filters.year || yearOf(row) === filters.year).map(monthOf), false);
    const filtered = filterRows(rows, filters);
    root.innerHTML = `
      <div class="dpr-journal-toolbar">
        <div class="dpr-journal-toolbar-row">
          <label>年份<select data-filter="year">${renderOptions(years, filters.year, '全部年份')}</select></label>
          <label>月份<select data-filter="month">${renderOptions(months, filters.month, '全部月份')}</select></label>
          <label>期刊<select data-filter="journal">${renderOptions(journals, filters.journal, '全部期刊')}</select></label>
          <label>PDF<select data-filter="pdf">
            <option value=""${!filters.pdf ? ' selected' : ''}>全部</option>
            <option value="open"${filters.pdf === 'open' ? ' selected' : ''}>有开放 PDF</option>
            <option value="missing"${filters.pdf === 'missing' ? ' selected' : ''}>无开放 PDF</option>
          </select></label>
        </div>
        <div class="dpr-journal-toolbar-row">
          <input data-filter="query" type="search" value="${escapeHtml(filters.query || '')}" placeholder="搜索标题、摘要、DOI、主题词">
          <button type="button" data-action="reset">重置</button>
        </div>
        <div class="dpr-journal-count">当前显示 ${filtered.length} / ${rows.length} 篇</div>
      </div>
      <div class="dpr-journal-list">
        ${filtered.length ? filtered.map(renderCard).join('') : '<div class="dpr-journal-empty">当前筛选条件下没有论文。</div>'}
      </div>
    `;
    bind(root);
  }

  function bind(root) {
    root.querySelectorAll('[data-filter]').forEach((el) => {
      el.addEventListener('change', () => {
        const state = stateByEl.get(root);
        if (!state) return;
        const key = el.getAttribute('data-filter');
        state.filters[key] = el.value;
        if (key === 'year') state.filters.month = '';
        render(root);
      });
      if (el.getAttribute('data-filter') === 'query') {
        el.addEventListener('input', () => {
          const state = stateByEl.get(root);
          if (!state) return;
          state.filters.query = el.value;
          render(root);
        });
      }
    });
    const reset = root.querySelector('[data-action="reset"]');
    if (reset) {
      reset.addEventListener('click', () => {
        const state = stateByEl.get(root);
        if (!state) return;
        state.filters = {};
        render(root);
      });
    }
  }

  async function initOne(root) {
    if (!root || stateByEl.has(root)) return;
    const source = root.getAttribute('data-source') || 'docs/journals/journal-papers.json';
    root.innerHTML = '<div class="dpr-journal-loading">正在加载环境期刊论文...</div>';
    try {
      const response = await fetch(source, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const rows = await response.json();
      stateByEl.set(root, {
        rows: Array.isArray(rows) ? rows : [],
        filters: {},
      });
      render(root);
    } catch (err) {
      root.innerHTML = `<div class="dpr-journal-error">环境期刊数据加载失败：${escapeHtml(err && err.message ? err.message : err)}</div>`;
    }
  }

  function init() {
    document.querySelectorAll('#dpr-journal-browser').forEach(initOne);
  }

  document.addEventListener('dpr-docsify-ready', () => {
    window.setTimeout(init, 0);
  });
  window.addEventListener('hashchange', () => {
    window.setTimeout(init, 80);
  });
  window.setTimeout(init, 0);

  return { init };
})();
