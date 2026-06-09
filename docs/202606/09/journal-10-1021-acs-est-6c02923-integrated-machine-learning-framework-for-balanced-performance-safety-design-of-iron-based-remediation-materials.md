---
title: Integrated Machine-Learning Framework for Balanced Performance-Safety Design of Iron-Based Remediation Materials
authors: "Qiqi Chen, Xinyue Wu, Wanyi Yu, Zhenjie Li, Jiang Xu, Kun Yang, Jie Hou, Daohui Lin"
date: 2026-06-04
link: "https://doi.org/10.1021/acs.est.6c02923"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: 铁基修复材料常通过表面包覆和晶格调控提升污染物去除能力，但反应性增强往往伴随更高生态毒性，性能与安全难以兼顾。本文基于1007个文献案例，整合材料、污染物分子描述符与实验条件，利用AutoGluon建立二分类QSAR模型，同时预测修复表现与材料-污染物联合毒性方向。模型在两项任务上分别取得0.88和0.90的平衡准确率，并结合特征归因、动态加权排序与适用域过滤，实现候选材料的风险感知预筛选。该框架为铁基环境修复材料的理性设计和优先级推荐提供了可操作工具。
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.6c02923
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 铁基材料虽能高效去除污染物，但性能提升常增加生物风险，亟需统一量化评估性能与安全。
method: 基于1007个案例，用AutoGluon构建二分类QSAR，输入材料与污染物描述符及条件，联合预测性能和毒性。
result: 修复性能与联合毒性预测的平衡准确率分别达0.88和0.90；性能受材料异质性主导，毒性更多由生物属性决定。
conclusion: 研究提出含动态加权排序和适用域过滤的预筛选框架，可支持铁基修复材料的平衡设计与优先应用。
---

## Abstract
Optimizing iron-based materials via surface coatings and lattice engineering has been a major research focus for environmental remediation, yet higher reactivity to contaminants often elevates risks to organisms. To address this trade-off, we develop an integrated machine-learning framework for the quantitative coassessment of performance and safety. The model was trained on a literature-derived data set of 1007 cases, encompassing 80 iron-based materials, 136 target pollutants, and 50 test organisms. Using AutoGluon, a binary QSAR model was constructed to screen reaction performance and predict the direction of material-pollutant joint toxicity. Inputting molecular descriptors of materials and pollutants alongside experimental conditions, this model achieved robust remediation performance and joint toxicity predictions with balanced accuracy of 0.88 and 0.90, respectively. Feature attribution analysis predicted that material heterogeneity was a key driver of performance, while organismal attributes primarily governed toxicity outcomes, highlighting niche-targeting material doping and hybrid nanobio remediation strategies. A dominance-aware dynamic weighting scheme that integrates calibrated probabilities with an upper-zone attenuation and low-zone penalty was introduced to rank material candidates, plus an applicability-domain filter to limit overconfident extrapolation. These findings support a practical prescreening framework that generates prioritized candidate materials to inform the rational application of iron-based remediation systems.