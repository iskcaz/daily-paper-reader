---
title: Improving Kinetic Prediction and Structural-Electronic Mechanistic Coherence in the Fenton Process via a Cross-Scale Machine-Learning Framework
authors: "Sheng Li, Ling Yuan, Yingying Chu, Chen Chen, Yujia Ma, Weiming Zhang, Jieshu Qian, Lu Lv, Bingcai Pan"
date: 2026-06-02
link: "https://doi.org/10.1021/acs.est.5c18754"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: Fenton高级氧化过程中，污染物降解动力学受分子结构、电子性质与环境条件共同影响，但现有解释常彼此割裂，难以统一预测与机理认知。该研究构建跨尺度机器学习框架，融合分子指纹与量子化学特征预测降解速率常数kobs。相较单尺度模型，融合模型在多算法下表现更高精度与稳健性，并重塑特征重要性。结果表明电子反应性具有结构依赖表达，且与pH等条件存在协同作用，为Fenton过程优化提供统一机理基础。
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.5c18754
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: Fenton降解动力学受结构、电子与条件耦合驱动，传统线性或孤立实验难统一解释并稳定预测kobs。
method: 构建融合分子指纹与量子化学特征的跨尺度机器学习框架，并结合UMAP、t-SNE和偏依赖分析机制。
result: 融合模型在各类算法中均优于单尺度模型；外部验证显示其对未知污染物及不同反应条件具有良好泛化性。
conclusion: 结构与电子机制并非割裂关系，电子反应性以结构依赖方式发挥作用，可据此优化Fenton反应动力学。
---

## Abstract
Accurately predicting and understanding contaminant degradation kinetics in advanced oxidation processes remains challenging due to the fragmented and even contradictory structure- and electronic-driven mechanistic interpretations, which traditional linear and isolated experimental methods fail to integrate across these multiscale drivers. This study developed a unified multiscale machine-learning framework that fused molecular fingerprints (MFs) and quantum chemical features (QCFs) of contaminants to predict the kobs of contaminant degradation in the Fenton process, aiming to link structural and electronic drivers. Compared with single-scale models, the fusion model achieved a higher predictive performance and robustness across all evaluated algorithms. More importantly, feature fusion reshaped the feature importance landscape, yielding a coherent structural–electronic mechanistic interpretation in which electronic reactivity is expressed in a structure-dependent manner rather than acting as an isolated molecular property. Interaction analyses (e.g., UMAP and t-SNE) further reveal the complementarity between MFs and QCFs by visualizing their distribution patterns. Partial dependence analyses reveal the synergistic interactions between key environmental factors (e.g., pH) and contaminant properties, defining optimal kinetic regimes for degradation kinetics. External validation experiments confirm the generalizability of the fusion model to unseen contaminants and varying reaction conditions. Overall, this proposed framework reconciles mechanistic understanding and provides a basis for rational optimization of the Fenton process.