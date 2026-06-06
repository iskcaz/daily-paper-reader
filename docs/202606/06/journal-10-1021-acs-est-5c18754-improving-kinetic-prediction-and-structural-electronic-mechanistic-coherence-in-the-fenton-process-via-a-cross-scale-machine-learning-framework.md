---
title: Improving Kinetic Prediction and Structural-Electronic Mechanistic Coherence in the Fenton Process via a Cross-Scale Machine-Learning Framework
authors: "Sheng Li, Ling Yuan, Yingying Chu, Chen Chen, Yujia Ma, Weiming Zhang, Jieshu Qian, Lu Lv, Bingcai Pan"
date: 2026-06-02
link: "https://doi.org/10.1021/acs.est.5c18754"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: 针对芬顿过程污染物降解动力学难以准确预测、且结构驱动与电子驱动机理解释割裂甚至矛盾的问题，研究构建了融合分子指纹与量子化学特征的跨尺度机器学习框架。该框架统一表征污染物结构与电子反应性，并结合UMAP、t-SNE及偏依赖分析揭示特征互补与环境因子协同作用。相比单尺度模型，融合模型在各类算法下均表现出更高精度与鲁棒性，且外部验证证明其可推广到未知污染物和变化工况。研究因此在提升kobs预测能力的同时，给出了更一致的结构—电子机理解释，为芬顿工艺优化提供依据。
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.5c18754
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: 芬顿降解动力学受结构、电子与环境多因素耦合影响，传统线性或单尺度方法难统一预测与机理解释。
method: 融合污染物分子指纹与量子化学特征，构建跨尺度机器学习模型，并用降维和偏依赖分析解释特征交互。
result: 融合模型较单尺度模型在所有算法中预测kobs更准确稳健，且外部实验验证了对新污染物和工况的泛化性。
conclusion: 电子反应性并非孤立属性，而是以结构依赖方式发挥作用；该框架统一机理认知并支撑芬顿过程优化。
---

## Abstract
Accurately predicting and understanding contaminant degradation kinetics in advanced oxidation processes remains challenging due to the fragmented and even contradictory structure- and electronic-driven mechanistic interpretations, which traditional linear and isolated experimental methods fail to integrate across these multiscale drivers. This study developed a unified multiscale machine-learning framework that fused molecular fingerprints (MFs) and quantum chemical features (QCFs) of contaminants to predict the kobs of contaminant degradation in the Fenton process, aiming to link structural and electronic drivers. Compared with single-scale models, the fusion model achieved a higher predictive performance and robustness across all evaluated algorithms. More importantly, feature fusion reshaped the feature importance landscape, yielding a coherent structural–electronic mechanistic interpretation in which electronic reactivity is expressed in a structure-dependent manner rather than acting as an isolated molecular property. Interaction analyses (e.g., UMAP and t-SNE) further reveal the complementarity between MFs and QCFs by visualizing their distribution patterns. Partial dependence analyses reveal the synergistic interactions between key environmental factors (e.g., pH) and contaminant properties, defining optimal kinetic regimes for degradation kinetics. External validation experiments confirm the generalizability of the fusion model to unseen contaminants and varying reaction conditions. Overall, this proposed framework reconciles mechanistic understanding and provides a basis for rational optimization of the Fenton process.