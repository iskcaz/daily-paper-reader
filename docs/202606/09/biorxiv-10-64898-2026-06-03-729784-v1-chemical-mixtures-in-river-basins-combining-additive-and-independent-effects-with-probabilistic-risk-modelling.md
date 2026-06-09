---
title: "Chemical Mixtures in River Basins: Combining Additive and Independent Effects with Probabilistic Risk Modelling"
title_zh: 河流流域中的化学混合物：结合加和效应与独立效应的概率风险建模
authors: "Moe, S. J., Madsen, A. L., Mentzel, S., Viaene, K. P. J., Vlaeminck, K., Grung, M., Martins, S. E., Subelj, G., Welch, S. A., Verdonck, F."
date: 2026-06-07
pdf: "https://www.biorxiv.org/content/10.64898/2026.06.03.729784v1.full.pdf"
tags: ["query:coastal-pfas"]
score: 6.0
evidence: 流域污染物风险建模与上游输送背景相关
tldr: 河流流域中的化学混合物会产生“鸡尾酒效应”，而传统单物质评估难以反映真实生态风险。本文提出一个多层概率风险框架，在贝叶斯网络中先为单一物质计算风险商分布，再在同作用组内用浓度加和、组间用独立作用进行联合表征。作者以比利时流域15种农药和ENCORE暴露模拟开展验证，发现CA结果略高于IA，组合式CA+IA给出更均衡的风险估计，并可识别关键风险驱动物质。
source: biorxiv
selection_source: fresh_fetch
open_pdf_available: false
motivation: 流域中多种化学物共存会带来混合毒性，需用概率化方法替代传统单物质、确定性风险表征。
method: 构建面向对象贝叶斯网络：先算单物质风险商分布，组内按CA求和，组间按IA做联合超阈概率。
result: 在比利时流域15种农药试验中，各情景结果与文献一致；CA风险略高于IA，CA+IA介于两者之间。
conclusion: 该方法为流域混合物风险提供可操作的概率框架，并可借助敏感性分析支持化学物优先排序与管理。
---

## 摘要
水生生态系统中的化学混合物及其潜在的鸡尾酒效应，已被公认为全球河流流域面临的一种威胁。概率风险方法在环境风险评估中正变得越来越常见，并为混合物风险表征等方法学挑战提供了新的机遇。浓度加和（CA）概念通常用于较低层级的风险评估（例如风险商之和），作为一种务实且具有保护性的办法。然而，另一种独立作用（IA）概念也可以方便地纳入概率风险计算（例如阈值超标的联合概率）。我们开发了一个多层次概率模型，用于整合这两个概念，并将其表述为一个面向对象的贝叶斯网络（BN）。首先，对单个物质计算概率风险商（RQ），即环境浓度的概率分布与环境阈值的比值。接着，在物质组内应用CA概念，对RQ分布进行求和。最后，在不同物质组之间应用IA概念，假定其作用方式彼此独立，通过联合概率计算（“OR”表达式）来组合RQ分布。预测暴露浓度来自ENCORE归趋模型，这是一种基于过程的模型，用于模拟欧洲各地河流流域中的化学物质。本文展示了一项试点研究，聚焦于部分物质（15种农药）和部分河流流域（比利时境内），以作为概念验证。该试点研究的目的是通过在多层次BN中结合CA与IA概念，展示一种新的混合物风险表征概率方法。结果在不同情景之间以及与文献结果相比均表现出一致性，其中基于CA的风险表征略高于基于IA的风险表征。基于CA+IA的组合风险代表了一种合理的折中。对BN进行敏感性分析能够有效识别驱动风险的关键物质及物质组的排序，从而为化学物质优先级划分和风险管理提供支持。

## Abstract
Chemical mixtures and potential cocktail effects in aquatic ecosystems are recognised as a threat for river basins world-wide. Probabilistic risk approaches are becoming more common in environmental risk assessment, and offer new opportunities for metodological challenges such as of mixture risk characterisation. The Concentration Addition (CA) concept is commonly used in lower-tier risk assessment (e.g., sum of risk quotients), as a pragmatic and protective method. However, the alternative Independent Action (IA) concept can easily be implemented in probabilistic risk calculation (e.g., joint probability of threshold exceedances). We have developed a multi-level probabilistic model for integrating these two concepts, formulated as an object-oriented Bayesian network (BN). First, probabilistic risk quotients (RQ) are calculated for individual substances, as probability distributions of environmental concentrations divided by a threshold environmental value. Next, the CA concept is applied within groups of substances by summing the RQ distributions. Finally, the IA concept is applied across the different substance groups, assuming independent modes of action, to combine RQ distributions by joint probability calculation ("OR" expressions). Predicted exposure concentrations were obtained from the ENCORE fate model, a process-based model for simulation of chemicals in river basins across Europe. Here we present a pilot study focusing on a subset of the substances (15 pesticides) and river basins (in Belgium), as a proof-of-concept. The purpose of this pilot study was to demonstrate a novel probabilistic approach to mixture risk characterisation, by combining the CA and IA concepts in a multi-level BN. The results were consistent across scenarios as well as with literature, with CA-based risk characterisations being slightly higher the IA-based. The combined CA+IA-based risk represents a reasonable compromise. Sensitivity analysis of the BN can provide an effective ranking of the risk-driving substances and groups, to support chemical prioritisation and risk managment.