---
title: Qualitative and Quantitative Prediction of Blood–Brain Barrier Permeability of Chemicals via an SE(3)-Transformer-Based Model with LLM-Assisted Explanation
authors: "Lilai Shen, Ziyu Chen, Weiwei Huan, Yizhou Huang, Peirong Wu, Hou Guo, Chunlong Zhang, Shulin Zhuang"
date: 2026-08-04
link: "https://doi.org/10.1021/acs.est.6c06459"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:est", "query:EST"]
score: 6.0
evidence: 来自环境期刊监控：EST
tldr: "Abstract The blood–brain barrier (BBB) regulates the entry of chemicals into the central nervous system, and contaminants with high permeability can accumulate in the brain, posing neurotoxicity risks。"
source: journal
selection_source: journal_website_data
doi: 10.1021/acs.est.6c06459
journal: "Environmental Science & Technology"
journal_label: EST
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: "研究动机：Given the urgent need for high-throughput neurotoxicity assessment, this study proposes a multifeature fusion framework for identifying and quantifying the BBB permeability to neurotoxic chemicals。"
method: "方法：Its predictive performance was validated using a BBB bioassay (11 chemicals) and an external data set (2023 chemicals), in which the model achieved 94.42% AUC。"
result: 主要结果：Substructure mask explanation analysis revealed CCS as an influential feature that correlated well with BBB permeability to chemicals (R2 = 0.84)。
conclusion: 摘要未明确展开结论意义；后续应结合全文再判断应用价值。
---

## Abstract
Abstract The blood–brain barrier (BBB) regulates the entry of chemicals into the central nervous system, and contaminants with high permeability can accumulate in the brain, posing neurotoxicity risks. Given the urgent need for high-throughput neurotoxicity assessment, this study proposes a multifeature fusion framework for identifying and quantifying the BBB permeability to neurotoxic chemicals. BBBProfiler leverages an SE(3)-Transformer to encode the three-dimensional molecular geometry and a deep neural network to encode collision cross-section (CCS) and fingerprint, followed by adaptive integration of modality representations through gating weights. Under the scaffold-split evaluation, BBBProfiler achieves high performance with an area under the receiver operating characteristic curve (AUC) of 93.72% and a recall of 89.19% for classification, and a coefficient of determination (R2) of 0.72 for regression. Its predictive performance was validated using a BBB bioassay (11 chemicals) and an external data set (2023 chemicals), in which the model achieved 94.42% AUC. Substructure mask explanation analysis revealed CCS as an influential feature that correlated well with BBB permeability to chemicals (R2 = 0.84). Model predictions were supplemented with natural-language explanations generated from a large language model. BBBProfiler is deployed on a publicly accessible platform (https://www.ai4environ.cn/BBBProfiler) to facilitate the development of new approach methodologies for neurotoxicity evaluation.