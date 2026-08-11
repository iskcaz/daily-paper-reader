---
title: "Critical elements for groundwater contamination source identification (GCSI) in sparse/discontinuous data scenarios: Physical constraints and spatiotemporal information"
authors: "Yuanbo Ge, Weihong Zhang, Wenxi Lu, Jun Dong"
date: 2026-08-01
link: "https://doi.org/10.1016/j.watres.2026.126080"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:water-research", "query:WR"]
score: 6.0
evidence: 来自环境期刊监控：WR
tldr: "Operating enterprises have complex, concealed engineering facilities, and in the event of leakage incidents, pollutants are released, accumulate, and migrate in groundwater。"
source: journal
selection_source: journal_website_data
doi: 10.1016/j.watres.2026.126080
journal: Water Research
journal_label: WR
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: "研究动机：Operating enterprises have complex, concealed engineering facilities, and in the event of leakage incidents, pollutants are released, accumulate, and migrate in groundwater。"
method: "方法：To evaluate the efficiency and accuracy of Pi-STT, three indirect numerical inversion methods, integrating the ResNets surrogate model with the Goat Optimization Algorithm (GOA), Differential Evolution Adaptive Metropolis (DREAM), and Ensemble Kalman Filter。"
result: 主要结果：Results indicate that Pi-STT achieved the lowest mean relative errors and the shortest computational times for both the hypothetical case and the real operating enterprise。
conclusion: "结论意义：This work established a novel deep learning-based direct inversion method, the Physics-informed Spatiotemporal Transformer (Pi-STT), which effectively integrates spatiotemporal information from monitoring data and embeds physical constraints into the loss。"
---

## Abstract
Operating enterprises have complex, concealed engineering facilities, and in the event of leakage incidents, pollutants are released, accumulate, and migrate in groundwater. Groundwater contamination source identification (GCSI) is difficult due to the insufficient number of monitoring wells. Conventional indirect numerical inversion methods, such as simulation-optimization (SO), simulation-stochastic statistics (SSS), and simulation-filtering (SF), suffer from reduced accuracy due to the sparsity and high nonlinearity of monitoring data. This work established a novel deep learning-based direct inversion method, the Physics-informed Spatiotemporal Transformer (Pi-STT), which effectively integrates spatiotemporal information from monitoring data and embeds physical constraints into the loss function. To evaluate the efficiency and accuracy of Pi-STT, three indirect numerical inversion methods, integrating the ResNets surrogate model with the Goat Optimization Algorithm (GOA), Differential Evolution Adaptive Metropolis (DREAM), and Ensemble Kalman Filter (EnKF) algorithms, were developed based on the SO, SSS, and SF frameworks. Results indicate that Pi-STT achieved the lowest mean relative errors and the shortest computational times for both the hypothetical case and the real operating enterprise. Noise sensitivity and sparsity analyses performed separately for the steady-flow and transient-flow hypothetical cases demonstrate that Pi-STT maintains excellent robustness, with relative errors remaining below 10 % even under increased noise levels and shortened temporal observation periods. Pi-STT incorporates the critical elements for GCSI in sparse and discontinuous data scenarios, namely physical constraints and spatiotemporal information. This approach holds significant importance for efficiently and accurately identifying groundwater contamination sources in operating enterprises, demonstrating strong potential for practical application.