---
title: Integrated Machine-Learning Framework for Balanced Performance-Safety Design of Iron-Based Remediation Materials
authors: "Qiqi Chen, Xinyue Wu, Wanyi Yu, Zhenjie Li, Jiang Xu, Kun Yang, Jie Hou, Daohui Lin"
date: 2026-06-04
link: "https://doi.org/10.1021/acs.est.6c02923"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: 铁基修复材料常通过表面包覆与晶格调控提升污染物去除能力，但反应性增强往往伴随更高生态毒性，形成性能与安全难以兼顾的设计难题。本文基于1007个文献案例构建集成机器学习框架，联合输入材料、污染物分子描述符及实验条件，分别预测修复表现与材料-污染物联合毒性方向。模型对两项任务的平衡准确率分别达到0.88和0.90，并结合特征归因、动态加权排序和适用域过滤实现候选材料优选。该框架为铁基环境修复材料的理性预筛选与平衡设计提供了可操作工具。
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.6c02923
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 铁基材料虽能高效修复污染物，但活性提升常带来更高生物风险，亟需统一评估性能与安全的定量工具。
method: 汇集1007个案例，用AutoGluon构建二分类QSAR模型，联合预测修复效果与联合毒性，并引入动态加权排序和适用域过滤。
result: 模型在修复性能和联合毒性方向预测上平衡准确率分别为0.88和0.90；特征归因显示材料异质性主导性能，生物属性更影响毒性。
conclusion: 该研究提出兼顾效果与安全的铁基材料预筛选框架，可用于优先推荐候选材料并指导掺杂设计与纳米生物协同修复应用。
---

## Abstract
Optimizing iron-based materials via surface coatings and lattice engineering has been a major research focus for environmental remediation, yet higher reactivity to contaminants often elevates risks to organisms. To address this trade-off, we develop an integrated machine-learning framework for the quantitative coassessment of performance and safety. The model was trained on a literature-derived data set of 1007 cases, encompassing 80 iron-based materials, 136 target pollutants, and 50 test organisms. Using AutoGluon, a binary QSAR model was constructed to screen reaction performance and predict the direction of material-pollutant joint toxicity. Inputting molecular descriptors of materials and pollutants alongside experimental conditions, this model achieved robust remediation performance and joint toxicity predictions with balanced accuracy of 0.88 and 0.90, respectively. Feature attribution analysis predicted that material heterogeneity was a key driver of performance, while organismal attributes primarily governed toxicity outcomes, highlighting niche-targeting material doping and hybrid nanobio remediation strategies. A dominance-aware dynamic weighting scheme that integrates calibrated probabilities with an upper-zone attenuation and low-zone penalty was introduced to rank material candidates, plus an applicability-domain filter to limit overconfident extrapolation. These findings support a practical prescreening framework that generates prioritized candidate materials to inform the rational application of iron-based remediation systems.