---
title: Integrated Machine-Learning Framework for Balanced Performance-Safety Design of Iron-Based Remediation Materials
authors: "Qiqi Chen, Xinyue Wu, Wanyi Yu, Zhenjie Li, Jiang Xu, Kun Yang, Jie Hou, Daohui Lin"
date: 2026-06-04
link: "https://doi.org/10.1021/acs.est.6c02923"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: "Optimizing iron-based materials via surface coatings and lattice engineering has been a major research focus for environmental remediation, yet higher reactivity to contaminants often elevates risks to organisms。"
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.6c02923
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: "研究动机：The model was trained on a literature-derived data set of 1007 cases, encompassing 80 iron-based materials, 136 target pollutants, and 50 test organisms。"
method: "方法：Using AutoGluon, a binary QSAR model was constructed to screen reaction performance and predict the direction of material-pollutant joint toxicity。"
result: 摘要未明确给出可抽取的主要结果；当前不应据此推断定量发现。
conclusion: 结论意义：These findings support a practical prescreening framework that generates prioritized candidate materials to inform the rational application of iron-based remediation systems。
---

## Abstract
Optimizing iron-based materials via surface coatings and lattice engineering has been a major research focus for environmental remediation, yet higher reactivity to contaminants often elevates risks to organisms. To address this trade-off, we develop an integrated machine-learning framework for the quantitative coassessment of performance and safety. The model was trained on a literature-derived data set of 1007 cases, encompassing 80 iron-based materials, 136 target pollutants, and 50 test organisms. Using AutoGluon, a binary QSAR model was constructed to screen reaction performance and predict the direction of material-pollutant joint toxicity. Inputting molecular descriptors of materials and pollutants alongside experimental conditions, this model achieved robust remediation performance and joint toxicity predictions with balanced accuracy of 0.88 and 0.90, respectively. Feature attribution analysis predicted that material heterogeneity was a key driver of performance, while organismal attributes primarily governed toxicity outcomes, highlighting niche-targeting material doping and hybrid nanobio remediation strategies. A dominance-aware dynamic weighting scheme that integrates calibrated probabilities with an upper-zone attenuation and low-zone penalty was introduced to rank material candidates, plus an applicability-domain filter to limit overconfident extrapolation. These findings support a practical prescreening framework that generates prioritized candidate materials to inform the rational application of iron-based remediation systems.