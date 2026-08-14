---
title: Autonomous inverse modeling of complex groundwater systems via a physics-integrated large language model multi-agent framework
authors: "Funing Ma, Junjun Chen, Zhenxue Dai, Fangfei Cai, Yingtao Hu"
date: 2026-07-01
link: "https://doi.org/10.1016/j.watres.2026.125886"
tags: ["query:environmental-science", "query:journal-watch", "query:core-journal", "query:water-research", "query:WR"]
score: 6.0
evidence: 来自环境期刊监控：WR
tldr: "Inverse modeling of groundwater flow and transport in subsurface systems is fundamentally restricted by the conceptual-numerical gap, where translating hydrogeological hypotheses into executable simulation codes remains。"
source: journal
selection_source: journal_website_data
doi: 10.1016/j.watres.2026.125886
journal: Water Research
journal_label: WR
open_pdf_status: no_open_pdf
open_pdf_note: No legal open PDF found; skip screenshots and figure extraction.
open_pdf_available: false
motivation: "研究动机：Inverse modeling of groundwater flow and transport in subsurface systems is fundamentally restricted by the conceptual-numerical gap, where translating hydrogeological hypotheses into executable simulation codes remains a labor-intensive process。"
method: "方法：We systematically validate the framework's robustness through three progressive tiers of hydrogeological complexity。"
result: "主要结果：Results demonstrate that the agents successfully bridge the conceptual-numerical gap: (1) In heterogeneous media, the system autonomously identified structural controls of non-convex geological features; (2) In kinetic experiments, it demonstrated robustness。"
conclusion: "结论意义：Hydro-Agent establishes a transparent, auditable, and physically constrained AI modeling framework。"
---

## Abstract
Inverse modeling of groundwater flow and transport in subsurface systems is fundamentally restricted by the conceptual-numerical gap, where translating hydrogeological hypotheses into executable simulation codes remains a labor-intensive process. While data-driven machine learning offers superior computational speed, it frequently violates mass conservation laws and lacks the interpretability required for regulatory decision-making. To resolve these operational bottlenecks, we propose Hydro-Agent, a physics-integrated multi-agent framework that leverages Large Language Models (LLMs) to govern rigorous process-based simulations via a "code-as-policy" paradigm. Unlike black-box predictors, the framework couples a reasoning agent (HydroCoder) with an execution agent (Executor) to autonomously generate, debug, and adaptively configure optimization strategies for standard solvers. We systematically validate the framework's robustness through three progressive tiers of hydrogeological complexity. Results demonstrate that the agents successfully bridge the conceptual-numerical gap: (1) In heterogeneous media, the system autonomously identified structural controls of non-convex geological features; (2) In kinetic experiments, it demonstrated robustness across multiple noise levels to achieve high-fidelity parameter retrieval under significant observational uncertainty; and (3) In the field-scale Aquia Aquifer, it navigated an 18-dimensional parameter space to reproduce complex chromatographic separation trends along a 96 km flow path while strictly enforcing mechanistic thermodynamic consistency. Systematic baseline comparisons confirm that Hydro-Agent maintains the numerical rigor of traditional direct-coupling approaches while significantly enhancing operational autonomy and ensuring geologically plausible outcomes. Hydro-Agent establishes a transparent, auditable, and physically constrained AI modeling framework. Ultimately, this abstraction of technical complexity into high-level intent broadens access for hydrogeologists who lack coding expertise, facilitating objective-driven modeling workflows that prioritize hydrogeological insights over computational implementation.