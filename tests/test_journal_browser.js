const assert = require('node:assert/strict');

global.window = global.window || {
  addEventListener() {},
};
global.window.addEventListener = global.window.addEventListener || function addEventListener() {};
global.window.setTimeout = global.setTimeout;
global.window.clearTimeout = global.clearTimeout;
global.document = global.document || {
  activeElement: null,
  addEventListener() {},
  querySelectorAll() {
    return [];
  },
};

require('../app/journal-browser.js');

const { loadRowsFromHistory, normalizeIndexMonths, renderForTest } = global.window.DPRJournalBrowser.__test;

function testNormalizeIndexMonthsKeepsOnlyValidYearMonths() {
  assert.deepEqual(
    normalizeIndexMonths([
      { month: '2025-06', count: 0 },
      '2026-01',
      { month: 'bad' },
      {},
      null,
    ]),
    ['2025-06', '2026-01'],
  );
}

function testRenderIncludesEmptyIndexedMonthOptions() {
  const root = {
    innerHTML: '',
    querySelectorAll() {
      return [];
    },
    querySelector() {
      return null;
    },
  };

  renderForTest(root, {
    rows: [],
    monthOptions: ['2025-06'],
    filters: { year: '2025' },
  });

  assert.match(root.innerHTML, /<option value="2025" selected>2025<\/option>/);
  assert.match(root.innerHTML, /<option value="06">06<\/option>/);
  assert.match(root.innerHTML, /0 \/ 0/);
}

function testJournalOptionsFollowCurrentMonthFilter() {
  const root = {
    innerHTML: '',
    querySelectorAll() {
      return [];
    },
    querySelector() {
      return null;
    },
  };

  renderForTest(root, {
    rows: [
      {
        id: 'may-paper',
        title: 'May paper',
        published: '2026-05-15',
        journal_label: 'EST Letters',
      },
      {
        id: 'june-paper',
        title: 'June paper',
        published: '2026-06-04',
        journal_label: 'EST',
      },
    ],
    monthOptions: ['2026-05', '2026-06'],
    filters: { year: '2026', month: '05' },
  });

  assert.match(root.innerHTML, /<option value="EST Letters">EST Letters<\/option>/);
  assert.doesNotMatch(root.innerHTML, /<option value="EST">EST<\/option>/);
  assert.match(root.innerHTML, /1 \/ 2/);
}

function testMonthOptionsFollowCurrentJournalFilter() {
  const root = {
    innerHTML: '',
    querySelectorAll() {
      return [];
    },
    querySelector() {
      return null;
    },
  };

  renderForTest(root, {
    rows: [
      {
        id: 'may-paper',
        title: 'May paper',
        published: '2026-05-15',
        journal_label: 'EST Letters',
      },
      {
        id: 'june-paper',
        title: 'June paper',
        published: '2026-06-04',
        journal_label: 'JHM',
      },
    ],
    monthOptions: ['2026-05', '2026-06'],
    filters: { year: '2026', journal: 'JHM' },
  });

  assert.match(root.innerHTML, /<option value="06">06<\/option>/);
  assert.doesNotMatch(root.innerHTML, /<option value="05">05<\/option>/);
  assert.match(root.innerHTML, /1 \/ 2/);
}

function testInvalidJournalSelectionIsPreservedAsNoMatch() {
  const root = {
    innerHTML: '',
    querySelectorAll() {
      return [];
    },
    querySelector() {
      return null;
    },
  };

  renderForTest(root, {
    rows: [
      {
        id: 'vegetable-paper',
        title: 'PFAS in vegetables',
        published: '2026-06-04',
        journal_label: 'EST',
      },
      {
        id: 'jhm-paper',
        title: 'PFAS in groundwater',
        published: '2026-06-02',
        journal_label: 'JHM',
      },
    ],
    monthOptions: ['2026-06'],
    filters: { journal: 'JHM', query: 'vegetables' },
  });

  assert.match(root.innerHTML, /<option value="JHM" selected>当前选择：JHM（无匹配）<\/option>/);
  assert.match(root.innerHTML, /<option value="EST">EST<\/option>/);
  assert.match(root.innerHTML, /0 \/ 2/);
  assert.match(root.innerHTML, /当前筛选条件下没有论文。/);
}

function testMonthSelectionIsPreservedWhenPdfFilterHasNoMatch() {
  const root = {
    innerHTML: '',
    querySelectorAll() {
      return [];
    },
    querySelector() {
      return null;
    },
  };

  renderForTest(root, {
    rows: [
      {
        id: 'may-paper',
        title: 'PFAS in coral',
        published: '2026-05-15',
        journal_label: 'EST Letters',
        open_pdf_available: false,
      },
      {
        id: 'june-paper',
        title: 'PFAS in Arctic animals',
        published: '2026-06-01',
        journal_label: 'JHM',
        pdf_url: 'https://example.org/article.pdf',
        open_pdf_available: true,
      },
    ],
    monthOptions: ['2026-05', '2026-06'],
    filters: { year: '2026', month: '05', pdf: 'open' },
  });

  assert.match(root.innerHTML, /<option value="05" selected>当前选择：05（无匹配）<\/option>/);
  assert.match(root.innerHTML, /<option value="06">06<\/option>/);
  assert.match(root.innerHTML, /0 \/ 2/);
  assert.match(root.innerHTML, /当前筛选条件下没有论文。/);
}

function testDoiLandingPageIsNotTreatedAsOpenPdf() {
  const root = {
    innerHTML: '',
    querySelectorAll() {
      return [];
    },
    querySelector() {
      return null;
    },
  };

  renderForTest(root, {
    rows: [
      {
        id: 'doi-page',
        title: 'PFAS DOI landing page',
        published: '2026-06-01',
        journal_label: 'JHM',
        pdf_url: 'https://doi.org/10.1016/j.jhazmat.2026.142173',
        open_pdf_available: true,
        open_pdf_status: 'open_pdf',
      },
    ],
    monthOptions: ['2026-06'],
    filters: { pdf: 'open' },
  });

  assert.match(root.innerHTML, /0 \/ 1/);
  assert.match(root.innerHTML, /当前筛选条件下没有论文。/);

  renderForTest(root, {
    rows: [
      {
        id: 'doi-page',
        title: 'PFAS DOI landing page',
        published: '2026-06-01',
        journal_label: 'JHM',
        pdf_url: 'https://doi.org/10.1016/j.jhazmat.2026.142173',
        open_pdf_available: true,
        open_pdf_status: 'open_pdf',
      },
    ],
    monthOptions: ['2026-06'],
    filters: { pdf: 'missing' },
  });

  assert.match(root.innerHTML, /1 \/ 1/);
  assert.match(root.innerHTML, /无开放 PDF，跳过截图\/图表提取/);
  assert.doesNotMatch(root.innerHTML, /打开开放 PDF/);
}

function testSearchMatchesAuthorNamesAndRendersAuthors() {
  const root = {
    innerHTML: '',
    querySelectorAll() {
      return [];
    },
    querySelector() {
      return null;
    },
  };

  renderForTest(root, {
    rows: [
      {
        id: 'jhm-paper',
        title: 'PFAS in Arctic food webs',
        published: '2026-06-01',
        journal_label: 'JHM',
        authors: [
          'Linyan Zhu',
          'Rossana Bossi',
          'Pedro N. Carvalho',
          'Jens Søndergaard',
          'Katrin Vorkamp',
        ],
      },
      {
        id: 'est-paper',
        title: 'PFAS in vegetables',
        published: '2026-06-04',
        journal_label: 'EST',
        authors: [
          { given: 'Beibei', family: 'Ye' },
        ],
      },
    ],
    monthOptions: ['2026-06'],
    filters: { query: 'Vorkamp' },
  });

  assert.match(root.innerHTML, /1 \/ 2/);
  assert.match(root.innerHTML, /PFAS in Arctic food webs/);
  assert.doesNotMatch(root.innerHTML, /PFAS in vegetables/);
  assert.match(root.innerHTML, /Linyan Zhu, Rossana Bossi, Pedro N\. Carvalho, Jens Søndergaard, Katrin Vorkamp/);
  assert.match(root.innerHTML, /placeholder="搜索标题、作者、摘要、DOI、主题词"/);
}

async function testQueryInputKeepsFocusAfterDebouncedRender() {
  const listeners = {};
  const query = {
    value: '',
    getAttribute(name) {
      return name === 'data-filter' ? 'query' : '';
    },
    addEventListener(type, handler) {
      listeners[type] = handler;
    },
    focus() {
      global.document.activeElement = query;
    },
    setSelectionRange(start, end) {
      query.selection = [start, end];
    },
  };
  const root = {
    innerHTML: '',
    querySelectorAll(selector) {
      return selector === '[data-filter]' ? [query] : [];
    },
    querySelector(selector) {
      return selector === 'input[data-filter="query"]' ? query : null;
    },
  };

  renderForTest(root, {
    rows: [
      {
        id: 'paper-1',
        title: 'PFAS transport',
        published: '2026-06-01',
        journal_label: 'EST',
      },
    ],
    monthOptions: [],
    filters: {},
  });

  query.value = 'PFAS';
  global.document.activeElement = null;
  listeners.input();
  await new Promise((resolve) => setTimeout(resolve, 230));

  assert.equal(query.value, 'PFAS');
  assert.equal(global.document.activeElement, query);
  assert.deepEqual(query.selection, [4, 4]);
  assert.match(root.innerHTML, /1 \/ 1/);
}

async function testQueryChangeDoesNotStealResetClick() {
  const listeners = {};
  const resetListeners = {};
  const query = {
    value: '',
    getAttribute(name) {
      return name === 'data-filter' ? 'query' : '';
    },
    addEventListener(type, handler) {
      listeners[type] = handler;
    },
    focus() {
      global.document.activeElement = query;
    },
    setSelectionRange(start, end) {
      query.selection = [start, end];
    },
  };
  const reset = {
    addEventListener(type, handler) {
      resetListeners[type] = handler;
    },
  };
  const root = {
    innerHTML: '',
    querySelectorAll(selector) {
      return selector === '[data-filter]' ? [query] : [];
    },
    querySelector(selector) {
      if (selector === 'input[data-filter="query"]') return query;
      if (selector === '[data-action="reset"]') return reset;
      return null;
    },
  };

  renderForTest(root, {
    rows: [
      {
        id: 'paper-1',
        title: 'PFAS in vegetables',
        published: '2026-06-01',
        journal_label: 'EST',
      },
      {
        id: 'paper-2',
        title: 'PFAS in groundwater',
        published: '2026-06-02',
        journal_label: 'JHM',
      },
    ],
    monthOptions: [],
    filters: {},
  });

  query.value = 'vegetables';
  listeners.input();
  listeners.change();
  resetListeners.click();
  await new Promise((resolve) => setTimeout(resolve, 230));

  assert.doesNotMatch(root.innerHTML, /value="vegetables"/);
  assert.match(root.innerHTML, /2 \/ 2/);
}

async function testLoadRowsFromHistorySkipsBrokenMonthFiles() {
  const originalFetch = global.fetch;
  global.fetch = async (url) => {
    if (url === 'index.json') {
      return {
        ok: true,
        json: async () => ({
          months: [
            { month: '2025-06', path: 'bad.json' },
            { month: '2025-07', path: 'good.json' },
          ],
        }),
      };
    }
    if (url === 'bad.json') {
      return { ok: false, status: 404, json: async () => [] };
    }
    if (url === 'good.json') {
      return {
        ok: true,
        json: async () => [
          { id: 'good', title: 'Good row', published: '2025-07-03' },
        ],
      };
    }
    throw new Error(`unexpected url ${url}`);
  };

  try {
    const loaded = await loadRowsFromHistory('index.json');
    assert.deepEqual(loaded.monthOptions, ['2025-06', '2025-07']);
    assert.equal(loaded.rows.length, 1);
    assert.equal(loaded.rows[0].id, 'good');
  } finally {
    global.fetch = originalFetch;
  }
}

testNormalizeIndexMonthsKeepsOnlyValidYearMonths();
testRenderIncludesEmptyIndexedMonthOptions();
testJournalOptionsFollowCurrentMonthFilter();
testMonthOptionsFollowCurrentJournalFilter();
testInvalidJournalSelectionIsPreservedAsNoMatch();
testMonthSelectionIsPreservedWhenPdfFilterHasNoMatch();
testDoiLandingPageIsNotTreatedAsOpenPdf();
testSearchMatchesAuthorNamesAndRendersAuthors();
Promise.resolve()
  .then(testQueryInputKeepsFocusAfterDebouncedRender)
  .then(testQueryChangeDoesNotStealResetClick)
  .then(testLoadRowsFromHistorySkipsBrokenMonthFiles)
  .then(() => {
    console.log('journal browser tests ok');
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
