---
title: Improving Kinetic Prediction and Structural-Electronic Mechanistic Coherence in the Fenton Process via a Cross-Scale Machine-Learning Framework
authors: "Sheng Li, Ling Yuan, Yingying Chu, Chen Chen, Yujia Ma, Weiming Zhang, Jieshu Qian, Lu Lv, Bingcai Pan"
date: 2026-06-02
link: "https://doi.org/10.1021/acs.est.5c18754"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: 芬顿过程中过污染物降解动力学常受结构因素与电子因素解释割裂、预测不稳所限制。该研究构建融合分子指纹与量子化学特征的跨尺度机器学习框架，用于预测污染物降解表观速率常数kobs。融合模型在多类算法下均优于单尺度模型，并通过特征重要性、UMAP/t-SNE及偏依赖分析揭示结构—电子协同机制。外部实验进一步验证其对未知污染物和不同反应条件的泛化能力，为芬顿工艺机理统一与优化提供依据。
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.5c18754
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 传统线性和割裂式实验难整合污染物结构、电子性质与环境条件对芬顿降解动力学的共同作用。
method: 融合分子指纹与量子化学特征，构建跨尺度机器学习模型，并结合UMAP、t-SNE和偏依赖分析解释机制。
result: 融合模型较单尺度模型在各算法中预测更准且更稳，并揭示pH与污染物性质存在显著协同作用。
conclusion: 电子反应性并非孤立属性，而是以结构依赖方式发挥作用，该框架统一机理认知并支持芬顿过程优化。
---

## Abstract
Accurately predicting and understanding contaminant degradation kinetics in advanced oxidation processes remains challenging due to the fragmented and even contradictory structure- and electronic-driven mechanistic interpretations, which traditional linear and isolated experimental methods fail to integrate across these multiscale drivers. This study developed a unified multiscale machine-learning framework that fused molecular fingerprints (MFs) and quantum chemical features (QCFs) of contaminants to predict the kobs of contaminant degradation in the Fenton process, aiming to link structural and electronic drivers. Compared with single-scale models, the fusion model achieved a higher predictive performance and robustness across all evaluated algorithms. More importantly, feature fusion reshaped the feature importance landscape, yielding a coherent structural–electronic mechanistic interpretation in which electronic reactivity is expressed in a structure-dependent manner rather than acting as an isolated molecular property. Interaction analyses (e.g., UMAP and t-SNE) further reveal the complementarity between MFs and QCFs by visualizing their distribution patterns. Partial dependence analyses reveal the synergistic interactions between key environmental factors (e.g., pH) and contaminant properties, defining optimal kinetic regimes for degradation kinetics. External validation experiments confirm the generalizability of the fusion model to unseen contaminants and varying reaction conditions. Overall, this proposed framework reconciles mechanistic understanding and provides a basis for rational optimization of the Fenton process.