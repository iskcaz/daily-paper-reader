---
title: Improving Kinetic Prediction and Structural-Electronic Mechanistic Coherence in the Fenton Process via a Cross-Scale Machine-Learning Framework
authors: "Sheng Li, Ling Yuan, Yingying Chu, Chen Chen, Yujia Ma, Weiming Zhang, Jieshu Qian, Lu Lv, Bingcai Pan"
date: 2026-06-02
link: "https://doi.org/10.1021/acs.est.5c18754"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: 芬顿过程中污染物降解动力学受分子结构、电子性质与环境条件共同影响，传统线性或单尺度方法难以统一解释。该研究构建融合分子指纹与量子化学特征的跨尺度机器学习框架，用于预测污染物降解速率常数kobs。相比单尺度模型，融合模型在多种算法下表现出更高精度与稳健性，并重塑了特征重要性分布。研究进一步揭示电子反应性依赖分子结构表达，并通过外部实验验证模型对未知污染物和不同反应条件的泛化能力。
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.5c18754
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 芬顿动力学预测常受结构与电子机制割裂、解释矛盾及多尺度因素难整合的限制。
method: 融合分子指纹与量子化学特征，结合多种机器学习算法、降维可视化和偏依赖分析建模。
result: 融合模型较单尺度模型预测更准且更稳健，并识别出pH与污染物性质协同决定最优动力学区间。
conclusion: 该框架统一了结构—电子机制解释，为芬顿过程的动力学预测与工艺优化提供了可靠依据。
---

## Abstract
Accurately predicting and understanding contaminant degradation kinetics in advanced oxidation processes remains challenging due to the fragmented and even contradictory structure- and electronic-driven mechanistic interpretations, which traditional linear and isolated experimental methods fail to integrate across these multiscale drivers. This study developed a unified multiscale machine-learning framework that fused molecular fingerprints (MFs) and quantum chemical features (QCFs) of contaminants to predict the kobs of contaminant degradation in the Fenton process, aiming to link structural and electronic drivers. Compared with single-scale models, the fusion model achieved a higher predictive performance and robustness across all evaluated algorithms. More importantly, feature fusion reshaped the feature importance landscape, yielding a coherent structural–electronic mechanistic interpretation in which electronic reactivity is expressed in a structure-dependent manner rather than acting as an isolated molecular property. Interaction analyses (e.g., UMAP and t-SNE) further reveal the complementarity between MFs and QCFs by visualizing their distribution patterns. Partial dependence analyses reveal the synergistic interactions between key environmental factors (e.g., pH) and contaminant properties, defining optimal kinetic regimes for degradation kinetics. External validation experiments confirm the generalizability of the fusion model to unseen contaminants and varying reaction conditions. Overall, this proposed framework reconciles mechanistic understanding and provides a basis for rational optimization of the Fenton process.