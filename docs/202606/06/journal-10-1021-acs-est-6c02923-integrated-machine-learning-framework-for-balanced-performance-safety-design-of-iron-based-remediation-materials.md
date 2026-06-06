---
title: Integrated Machine-Learning Framework for Balanced Performance-Safety Design of Iron-Based Remediation Materials
authors: "Qiqi Chen, Xinyue Wu, Wanyi Yu, Zhenjie Li, Jiang Xu, Kun Yang, Jie Hou, Daohui Lin"
date: 2026-06-04
link: "https://doi.org/10.1021/acs.est.6c02923"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: 铁基修复材料常通过表面包覆与晶格调控提升污染物去除能力，但反应性增强也可能带来更高生态毒性，性能与安全难以兼顾。该研究基于1007个文献案例，整合材料、污染物分子描述符及实验条件，利用AutoGluon构建二分类QSAR模型，同时预测修复表现与材料-污染物联合毒性方向。模型在两项任务上分别取得0.88和0.90的平衡准确率，并结合特征归因、动态加权排序与适用域过滤实现候选材料优选。该框架为铁基环境修复材料的前筛选与理性设计提供了可量化的性能-安全协同评估工具。
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.6c02923
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 高活性铁基修复材料虽能强化污染去除，但往往同步提升生物风险，缺少可同时量化性能与安全的评估工具。
method: 汇集1007个案例，输入材料与污染物描述符及实验条件，借助AutoGluon建立二分类QSAR并配合动态加权排序。
result: 修复性能与联合毒性方向预测的平衡准确率分别达0.88和0.90，且特征归因揭示异质性与生物属性的主导作用。
conclusion: 该研究提出兼顾排序与外推约束的前筛选框架，可支持铁基修复材料的性能-安全协同优化与理性应用。
---

## Abstract
Optimizing iron-based materials via surface coatings and lattice engineering has been a major research focus for environmental remediation, yet higher reactivity to contaminants often elevates risks to organisms. To address this trade-off, we develop an integrated machine-learning framework for the quantitative coassessment of performance and safety. The model was trained on a literature-derived data set of 1007 cases, encompassing 80 iron-based materials, 136 target pollutants, and 50 test organisms. Using AutoGluon, a binary QSAR model was constructed to screen reaction performance and predict the direction of material-pollutant joint toxicity. Inputting molecular descriptors of materials and pollutants alongside experimental conditions, this model achieved robust remediation performance and joint toxicity predictions with balanced accuracy of 0.88 and 0.90, respectively. Feature attribution analysis predicted that material heterogeneity was a key driver of performance, while organismal attributes primarily governed toxicity outcomes, highlighting niche-targeting material doping and hybrid nanobio remediation strategies. A dominance-aware dynamic weighting scheme that integrates calibrated probabilities with an upper-zone attenuation and low-zone penalty was introduced to rank material candidates, plus an applicability-domain filter to limit overconfident extrapolation. These findings support a practical prescreening framework that generates prioritized candidate materials to inform the rational application of iron-based remediation systems.