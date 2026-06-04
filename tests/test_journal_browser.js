const assert = require('node:assert/strict');

global.window = global.window || {
  addEventListener() {},
  setTimeout() {},
};
global.window.addEventListener = global.window.addEventListener || function addEventListener() {};
global.window.setTimeout = global.window.setTimeout || function setTimeoutStub() {};
global.document = global.document || {
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
testLoadRowsFromHistorySkipsBrokenMonthFiles()
  .then(() => {
    console.log('journal browser tests ok');
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
