# 仓库级 Agent 规则

## 项目当前维护背景

- 这是用户 fork 后自用的 `daily-paper-reader` 仓库，远端 fork 通常为 `userfork https://github.com/iskcaz/daily-paper-reader.git`。
- 用户正在使用 GitHub Pages 站点：`https://iskcaz.github.io/daily-paper-reader/`。
- 当前已验证可用的稳定提交是 `63b114b`（`fix utf8 decoding for llm responses`）。如果后续改动导致网页或模型调用异常，优先对比或回退到这个提交。
- 用户希望使用的模型服务配置是：

```text
Base URL: https://jsyai.xinglian.work/v1
Model: gpt-5.4
```

- 不要把这个模型误判为不可用，也不要把问题简化成“只能换 DeepSeek”。这个 fork 已经改过前端和工作流，目标是支持上述 OpenAI-compatible 服务。
- 用户不熟悉 GitHub 和部署流程。回复时优先用中文、少术语、给明确下一步；不要要求用户提供或粘贴完整 API Key。

## 当前关键修复点

- 前端配置已经允许保存 `gpt-5.4` 和 `https://jsyai.xinglian.work/v1`。
- 浏览器端 CORS 测试失败不一定代表服务不可用，因为 GitHub Actions 的服务端请求仍可能可用。不要仅凭网页测试失败就否定模型。
- GitHub Actions 的智能查询生成已经加入服务端兜底，主要生成脚本为 `scripts/smart_query_generate.py`。
- `src/llm.py` 里必须按 UTF-8 读取模型 JSON 响应内容。此前供应商响应头编码不标准，`requests.response.json()` 可能把中文解成乱码。当前修复是优先用 `response.content.decode("utf-8-sig")` 再 `json.loads(...)`。
- 如果用户说“抽取后是乱码”，先检查生成文件本身，而不是只检查浏览器显示。重点看：
  - `docs/<日期>/`
  - `docs/README.md`
  - `docs/_sidebar.md`
  - `docs/<日期>/papers.meta.json`
  - `archive/<日期>/recommend/*.json`

## 自然科学文献源维护

- 用户的研究方向需要正式环境科学期刊，不应只依赖 arXiv / bioRxiv / 计算机会议源。
- 新增自然科学期刊监控清单为 `journal_watchlist.yaml`。首批重点期刊包括 EST、EST Letters、Water Research、Science of the Total Environment、Journal of Hazardous Materials。
- 自然科学来源抓取器为 `src/maintain/fetchers/fetch_journal_sources.py`：
  - Crossref：按期刊 ISSN 抓新论文，发现 EST / WR / STOTEN / JHM 等正式期刊文章。
  - OpenAlex：按 DOI 补主题、开放获取状态、来源信息。
  - Semantic Scholar：按 DOI 批量补摘要、引用量、开放 PDF 线索。
  - Unpaywall：按 DOI 专门寻找合法开放 PDF。
- 如果仍没有开放 PDF，保留论文卡片，但必须标记：

```text
open_pdf_status: no_open_pdf
open_pdf_available: false
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
```

- 目前 `.github/workflows/journal-sources-preview.yml` 是预览工作流，只产出 artifact，不修改网站内容。不要把它误认为已经接入主推荐流水线。
- 后续要真正进入网页推荐，需要再做 Supabase 表/RPC 或本地 raw 文件合并、DOI 去重、期刊权重排序与前端标签显示。

## 稳定版本和发布规则

- 这个项目对用户来说是一个已经部署的网站，不只是代码库。修改后如果用户期望网页生效，通常需要提交并推送到 `userfork main`。
- 推送用户 fork 的常用命令是：

```bash
git push userfork <当前分支>:main
```

- 推送前必须确认没有误提交 `secret.private`、真实 API Key、PAT 或其它私密信息。
- 推送后提示用户等待 GitHub Pages 自动部署，并使用带版本参数的地址强制刷新，例如：

```text
https://iskcaz.github.io/daily-paper-reader/?v=<说明>
```

- 如果网页仍旧不变，先让用户 `Ctrl + F5` 强刷，再检查 GitHub Actions / Pages 是否完成。

## 用户运行态文件规则

- 默认不要改动或提交以下文件，除非用户明确要求修复当前网页、生成结果或部署状态：
  - `config.yaml`
  - `docs/config.yaml`
  - `docs/README.md`
  - `docs/_sidebar.md`
  - `docs/<日期>/`
  - `docs/assets/`
  - `archive/`
  - `secret.private`
- 例外：如果用户明确反馈当前网页内容错误、乱码、生成结果错误，可以修复并提交 `docs/` 和 `archive/` 下对应日期的生成产物。提交前需要说明这是为了修复已发布页面。
- 永远不要提交 `secret.private`，也不要在回复中展示其中内容。

## 常用验证命令

- 修改模型配置或调用逻辑后，优先运行：

```bash
python -m unittest tests.test_llm_structured_output
node tests/test_subscriptions_smart_query.js
node tests/test_llm_config_utils.js
python -m py_compile scripts/smart_query_generate.py
```

- 修复乱码后，至少检查关键中文字段的 Unicode 码点，确认不是 `ä¸`、`æµ`、`è¯` 这类 mojibake 残留。
- 提交前运行：

```bash
git diff --check
git status --short --branch
```

## 提交共同作者规则

- 本仓库内由 Agent/Codex 创建、提交或推送的 commit，提交信息末尾必须追加以下共同作者 trailer：

```text
Co-Authored-By: lilmortyj <781113402@qq.com>
Co-Authored-By: xixi <3495302215@qq.com>
Co-Authored-By: wy <345619498@qq.com>
```

- 以上规则仅用于 Git commit message，不代表需要修改 `CITATION.cff`、`README.md` 或其它项目作者元数据。

## 合并主分支规则

- 将工作分支合并到 `main` / `origin/main` 前，必须先确认本次提交只包含可上游同步的代码、模板与测试改动，避免破坏用户通过 GitHub 网页 `Sync fork` 的既有使用习惯。
- 合并前必须执行并检查：

```bash
git diff --name-only origin/main..HEAD
git status --short
```

- 允许合并到主分支的典型路径：
  - `.github/workflows/`
  - `app/`
  - `scripts/`
  - `src/`
  - `sql/`
  - `tests/`
  - `requirements*.txt`
  - `.env.example`
  - `.gitignore`
  - `README.md`
  - `AGENTS.md`
- 默认不得合并以下用户运行态/每日生成产物路径，除非用户明确要求且已说明会影响 fork 用户的 `Sync fork` 风险：
  - `config.yaml`
  - `docs/config.yaml`
  - `docs/README.md`
  - `docs/_sidebar.md`
  - `docs/<日期>/`
  - `docs/assets/`
  - `archive/`
  - `secret.private`
- 若工作分支中混入了上述运行态产物，必须先从提交中剥离这些文件，只保留代码改动后再合并主分支。
- 推荐的主分支合并方式是快进合并：

```bash
git switch main
git merge --ff-only <work-branch>
git push origin main
```

- 若无法 `--ff-only`，必须先说明原因和冲突范围，不得直接创建包含用户运行态产物的 merge commit。
