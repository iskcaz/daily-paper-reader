---
title: Physics-Regularized Operator Learning for Hourly Mapping of Near-Surface Air Pollution under Sparse Observations
authors: "Jingkai Xue, Yizhi Zhu, Qihou Hu, Yu Ma, Zirui Xuan, Jun Zhang, Zhiguo Zhang, Peize Lin, Qihua Li, Cheng Liu"
date: 2026-08-19
link: "https://doi.org/10.1021/acs.estlett.6c00668"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est-letters", "query:EST Letters"]
score: 6.0
evidence: 来自环境期刊监控：EST Letters
tldr: "Abstract Hourly air-pollution fields are needed for exposure assessment and air-quality management; however, ground monitors are sparse, and satellite observations are intermittent。"
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.estlett.6c00668
journal: "Environmental Science & Technology Letters"
journal_label: EST Letters
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 研究动机：Data-driven models may reproduce station observations while leaving unmonitored regions poorly constrained。
method: "方法：To test this, we trained a neural operator to predict near-surface CO over Mainland China from emissions, meteorology, and terrain, using ground observations only for training。"
result: "主要结果：On the unseen year 2022, this constraint increased hourly station agreement from R = 0.57 to 0.64 and structural agreement with an assimilation-informed reanalysis from R = 0.55 to 0.74。"
conclusion: 结论意义：Transport regularization therefore reduces nonphysical extrapolation and enables more stable hourly pollution-field reconstruction without observations at prediction time。
---

## Abstract
Abstract Hourly air-pollution fields are needed for exposure assessment and air-quality management; however, ground monitors are sparse, and satellite observations are intermittent. Data-driven models may reproduce station observations while leaving unmonitored regions poorly constrained. This mismatch raises a central concern for observation-free hourly mapping: station-level skill may not imply a physically reliable pollution field. To test this, we trained a neural operator to predict near-surface CO over Mainland China from emissions, meteorology, and terrain, using ground observations only for training. Transport regularization was imposed through a full-grid advection-diffusion-reaction residual that balances emissions, transport, diffusion, and decay. On the unseen year 2022, this constraint increased hourly station agreement from R = 0.57 to 0.64 and structural agreement with an assimilation-informed reanalysis from R = 0.55 to 0.74. In a blind-region test, where local monitors were removed from training, R increased from 0.51 to 0.58. Transport regularization therefore reduces nonphysical extrapolation and enables more stable hourly pollution-field reconstruction without observations at prediction time.