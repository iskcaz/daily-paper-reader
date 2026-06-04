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

function testInvalidJournalCleanupRebuildsMonthOptions() {
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

  assert.doesNotMatch(root.innerHTML, /<option value="JHM" selected>JHM<\/option>/);
  assert.match(root.innerHTML, /<option value="EST">EST<\/option>/);
  assert.match(root.innerHTML, /<option value="06">06<\/option>/);
  assert.match(root.innerHTML, /1 \/ 2/);
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
testInvalidJournalCleanupRebuildsMonthOptions();
Promise.resolve()
  .then(testQueryInputKeepsFocusAfterDebouncedRender)
  .then(testLoadRowsFromHistorySkipsBrokenMonthFiles)
  .then(() => {
    console.log('journal browser tests ok');
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
