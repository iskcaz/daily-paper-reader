---
title: Generalizable and Transferable Machine Learning Enables Accelerated Metal–Organic Framework Discovery in Gas Separations
authors: "Meiqi Yang, Jianhao Qian, Ruoyu Wang, Menachem Elimelech"
date: 2026-07-02
link: "https://doi.org/10.1021/acs.est.6c06775"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: "Gas separation is central to industrial processes that drive climate mitigation, clean energy, and sustainable technologies。"
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.6c06775
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 研究动机：Existing machine learning approaches have accelerated screening but often lack generalizability across diverse gas pairs and operating conditions。
method: "方法：Leveraging this dataset, LightGBM regressor (LGBMR) models are developed to achieve high predictive accuracy for gas uptakes ( R 2 = 0.93 and 0.92) and selectivity ( R 2 = 0.95) under strict robustness controls, including seed randomness and cross validation。"
result: 摘要未明确给出可抽取的主要结果；当前不应据此推断定量发现。
conclusion: "结论意义：This generalizable and interpretable framework enables scalable, data-driven discovery of advanced adsorbents for complex and evolving separation tasks。"
---

## Abstract
Gas separation is central to industrial processes that drive climate mitigation, clean energy, and sustainable technologies. Metal–organic frameworks (MOFs) offer remarkable tunability for adsorption-based separations, yet identifying optimal materials remains challenging due to their vast structural diversity, costly simulations, and the difficulty of achieving a full range of desired properties. Existing machine learning approaches have accelerated screening but often lack generalizability across diverse gas pairs and operating conditions. Herein, we present BiMix-Bench, a curated database comprising ∼125,900 MOFs and five binary gas mixtures. Leveraging this dataset, LightGBM regressor (LGBMR) models are developed to achieve high predictive accuracy for gas uptakes ( R 2 = 0.93 and 0.92) and selectivity ( R 2 = 0.95) under strict robustness controls, including seed randomness and cross validation. Using CO 2 /H 2 as a case study, we evaluate both zero-shot and few-shot transfer performance. While zero-shot predictions provide limited out-of-distribution accuracy, the pretrained LGBMR models can be efficiently adapted with a small number of new simulations ( N = 204) through transfer learning. This data-efficient adaptation enables the rapid identification of top-performing MOFs, which are subsequently validated through grand canonical Monte Carlo simulations. This generalizable and interpretable framework enables scalable, data-driven discovery of advanced adsorbents for complex and evolving separation tasks.