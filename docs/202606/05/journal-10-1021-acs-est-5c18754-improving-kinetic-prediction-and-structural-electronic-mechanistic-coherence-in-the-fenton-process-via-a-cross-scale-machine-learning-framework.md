---
title: Improving Kinetic Prediction and Structural-Electronic Mechanistic Coherence in the Fenton Process via a Cross-Scale Machine-Learning Framework
authors: "Sheng Li, Ling Yuan, Yingying Chu, Chen Chen, Yujia Ma, Weiming Zhang, Jieshu Qian, Lu Lv, Bingcai Pan"
date: 2026-06-02
link: "https://doi.org/10.1021/acs.est.5c18754"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: 针对芬顿过程中污染物降解动力学难预测、结构与电子机制解释割裂甚至矛盾的问题，研究构建了融合分子指纹与量子化学特征的跨尺度机器学习框架。该框架较单尺度模型在各类算法下都表现出更高的预测精度与稳健性，并通过特征重要性、UMAP/t-SNE和偏依赖分析揭示结构—电子协同作用。外部验证进一步证明模型可推广到未见污染物与不同反应条件，为芬顿过程机理统一理解与工艺优化提供了依据。
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.5c18754
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 传统线性或孤立实验难整合结构与电子多尺度驱动，导致芬顿降解动力学预测与机理解释不一致。
method: 融合污染物分子指纹和量子化学特征，构建跨尺度机器学习模型，并结合UMAP、t-SNE与偏依赖分析解释机制。
result: 融合模型在所有评估算法中均优于单尺度模型，且揭示电子反应性以结构依赖方式影响降解动力学。
conclusion: 该框架统一了结构—电子机制认知，并经外部实验验证具备泛化能力，可支撑芬顿过程的理性优化。
---

## Abstract
Accurately predicting and understanding contaminant degradation kinetics in advanced oxidation processes remains challenging due to the fragmented and even contradictory structure- and electronic-driven mechanistic interpretations, which traditional linear and isolated experimental methods fail to integrate across these multiscale drivers. This study developed a unified multiscale machine-learning framework that fused molecular fingerprints (MFs) and quantum chemical features (QCFs) of contaminants to predict the kobs of contaminant degradation in the Fenton process, aiming to link structural and electronic drivers. Compared with single-scale models, the fusion model achieved a higher predictive performance and robustness across all evaluated algorithms. More importantly, feature fusion reshaped the feature importance landscape, yielding a coherent structural–electronic mechanistic interpretation in which electronic reactivity is expressed in a structure-dependent manner rather than acting as an isolated molecular property. Interaction analyses (e.g., UMAP and t-SNE) further reveal the complementarity between MFs and QCFs by visualizing their distribution patterns. Partial dependence analyses reveal the synergistic interactions between key environmental factors (e.g., pH) and contaminant properties, defining optimal kinetic regimes for degradation kinetics. External validation experiments confirm the generalizability of the fusion model to unseen contaminants and varying reaction conditions. Overall, this proposed framework reconciles mechanistic understanding and provides a basis for rational optimization of the Fenton process.