---
title: Modelling biological and resource fluxes in fluvial meta-ecosystems
title_zh: 河流元生态系统中生物与资源通量的建模
authors: "Talluto, L., del Campo, R., Estevez, E., Fuss, T., Thuile Bistarelli, L., Martini, J., Singer, G. A."
date: 2026-06-04
pdf: "https://www.biorxiv.org/content/10.1101/2024.01.12.575367v3.full.pdf"
tags: ["query:coastal-pfas"]
score: 7.0
evidence: 河流网络通量建模可支撑陆源入海路径分析
tldr: 河流网络中水流会同时搬运营养、能量与生物个体，使相连生态系统强耦合，但现有模型很少把资源流与生物流显式联结。本文提出一个用于河流meta-ecosystem的模型及配套R包，把资源浓度视为生态位维度，驱动定殖与灭绝，并让生物消耗资源后再随水文过程向下游传输。通过数值实验与示例代码，作者展示了该框架可预测河网中资源与生物分布及整体功能，为研究生物多样性—生态系统功能关系提供工具。
source: biorxiv
selection_source: fresh_fetch
open_pdf_available: false
motivation: 河流生态系统受水流连接显著，跨生态系统的资源与生物流会共同影响群落组装与功能，但统一刻画二者耦合的模型不足。
method: 构建河流meta-ecosystem模型与R包，将资源浓度作为生态位维度影响定殖和灭绝，并加入生物对资源的消耗及下游输送反馈。
result: 通过in silico数值实验与示例分析，模型展示了对河网中资源和生物空间分布，以及meta-ecosystem功能的预测能力。
conclusion: 该框架把资源流与生物流显式耦合，为分析河流网络中的群落动态、生态系统功能及多样性—功能关系提供了可用工具。
---

## 摘要
元生态系统理论预测，生态系统之间能量、营养物质和生物体的跨生态系统流动，会对局地群落组装和生态系统功能产生重要影响。该理论的发展也有望增进我们对生物多样性与生态系统功能关系的理解。元生态系统理论尤其适用于河流研究，因为水流会在相互连通的生态系统之间形成强烈的空间相互关系。然而，目前仍缺乏同时处理资源与生物体流动并明确将二者联系起来的模型。我们提出了一个关于资源与生物体跨生态系统流动的模型及其配套的 R 软件包，可用于预测它们在河流网络中的分布，以及元生态系统功能。该模型纳入了这两个关键组成部分之间的反馈：资源浓度构成生物体的生态位维度，从而改变网络中不同位置的定殖与灭绝动态；同时，生物体也会消耗资源，进而改变向下游输送的资源浓度。为展示该模型的能力，我们给出了一个计算机模拟实验及其分析，并提供了示例代码。

## Abstract
Meta-ecosystem theory predicts that cross-ecosystem flows of energy, nutrients, and organisms have important implications for local community assembly and ecosystem functioning. Developments in the theory also have the potential to enhance our understanding of biodiversity-ecosystem functioning relationships. Meta-ecosystem theory is particularly well-suited to the study of rivers, because water flow forces strong spatial interrelationships among connected ecosystems. However, models that address flows of both resources and organisms and explicitly link both are lacking. We present a model and associated R-package for cross-ecosystem flows of both resources and organisms that can be used to predict their distribution in river networks, as well as meta-ecosystem functioning. The model incorporates feedbacks between these two crucial components---resource concentrations represent niche dimensions for organisms, modifying the colonisation and extinction dynamics and different locations in the network, and organisms also consume resources, thereby modifying the concentrations that are transported downstream. To illustrate the capabilities of the model, we present an in silico experiment and analysis, as well as providing sample code.