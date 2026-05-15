# China, Made in China 2025, and the Road to Agentic EAM

This note extends the paper with a China-specific view. The official policy name is **Made in China 2025**. In product and industry conversations it is often reframed as the move from conventional manufacturing to intelligent manufacturing: from manufacturing capacity to intelligent manufacturing capability. This document uses that framing as an interpretation, not as a replacement for the official policy title.

![Made in China 2025 as a Launchpad for Agentic EAM](../assets/made-in-china-2025-agentic-eam-roadmap.svg)

## 1. Why China is a serious proving ground for multi-agent CMMS/EAM

China is relevant to agentic CMMS/EAM for a practical reason: the country combines large installed industrial assets, rapid industrial digitalization, policy pressure for intelligent manufacturing, and many safety-critical operating environments. These conditions produce exactly the kind of messy, cross-functional maintenance decisions that a multi-agent system is designed to handle.

A future CMMS/EAM platform is not just a work-order database. In high-scale industrial settings it becomes a control plane for many signals and decisions: machine alarms, operator reports, drone inspections, spare parts, shutdown windows, energy constraints, regulatory rules, permits, vendor obligations, and human approvals. A single AI assistant may summarize this context, but a multi-agent architecture can decompose it, cross-check it, debate it, and keep the decision auditable.

## 2. What Made in China 2025 contributes to the platform thesis

The State Council issued the **Made in China 2025** notice in 2015 as a manufacturing-power action program. Public government summaries describe it as the first ten-year action program for implementing a manufacturing-power strategy. The policy emphasized innovation, integration of informatization and industrialization, industrial foundations, quality and brands, green manufacturing, service-oriented manufacturing, and internationalization.

For this paper, the most relevant parts are not the slogans. They are the structural priorities that push factories and asset operators toward connected, data-rich, safety-aware operations:

| Made in China 2025 element | Why it matters for CMMS/EAM |
| --- | --- |
| Intelligent manufacturing and IT/OT integration | More connected assets generate more maintenance signals, but also more data-governance and cybersecurity burden. |
| High-end CNC and robotics | Robotic cells, machine tools, and automated production lines need condition monitoring, calibration, tooling, and safety checks. |
| Advanced rail transit equipment | Rail fleets require safety-critical maintenance, lifecycle service, strict audit, and explainable decision support. |
| Power equipment | Grid assets need inspection, defect recognition, outage planning, emergency response, and policy-gated field work. |
| Energy-saving and new-energy vehicles | Battery, charging, power electronics, and production-line assets create new reliability and warranty loops. |
| New materials and process industries | Quality, process stability, and heavy-asset reliability become linked; maintenance decisions affect product quality and energy use. |

The official priority sectors listed in public summaries include next-generation information technology, high-end CNC machine tools and robotics, aerospace equipment, marine engineering equipment and high-tech ships, advanced rail transit equipment, energy-saving and new-energy vehicles, power equipment, agricultural machinery, new materials, and biomedicine/high-performance medical devices.

## 3. The CMMS/EAM interpretation: from digitized maintenance to agentic operations

A useful way to understand the platform evolution is:

1. **Digitized CMMS**: work orders, PMs, assets, spares, inventory, reporting.
2. **Integrated EAM**: mobile work execution, IoT integration, condition monitoring, reliability analysis, procurement/ERP/MES links.
3. **Intelligent EAM**: predictive maintenance, root-cause analysis, risk-based workflows, policy-aware approval, guided planning.
4. **Agentic EAM**: specialized agents collaborate across maintenance, production, energy, safety, inventory, finance, and vendors; bounded automation only happens when policy allows it.

The shift to agentic EAM does **not** mean removing people from maintenance decisions. It means giving planners and engineers a better review package: the system gathers evidence, checks policies, exposes conflicts, estimates risk, proposes options, and shows exactly what it is not allowed to do.

## 4. How the China examples map to multi-agent roles

| Sector signal | Example maintenance problem | Useful agent roles |
| --- | --- | --- |
| AI-enabled chiller and compressor manufacturing | A compressor shows abnormal noise and rising energy consumption. | Intake Agent, Asset Agent, Energy Agent, Inventory Agent, Service Agent, Policy Agent |
| Heavy equipment and connected machines | Field equipment reports fault codes while the factory has similar quality events. | Fleet Agent, Warranty Agent, Reliability Agent, MRO Agent, Vendor Agent |
| Grid drone inspection | AI recognizes a line defect or external hazard and needs a risk-ranked work order. | Inspection Agent, Grid Asset Agent, Safety Agent, Dispatch Agent, Policy Agent |
| Rail fleet O&M | Train data and depot history suggest a safety-critical intervention. | Fleet Agent, Safety Agent, Schedule Agent, Parts Agent, Human Review Agent |
| Petrochemical smart plant | Shutdown work requires permits, LOTO, parts, labor windows, and risk control. | Process Asset Agent, Permit Agent, Shutdown Agent, Inventory Agent, Risk Agent |
| Industrial Internet platform | Factories, partners, energy, and users need a shared data fabric. | Data Quality Agent, Platform Agent, Partner Agent, Energy Agent, Security Agent |

The common pattern is cross-functional reasoning. Maintenance is no longer an isolated department event. It touches production, quality, energy, service, safety, and capital planning.

## 5. What a future experimental CMMS product should do with this insight

A future CMMS/EAM platform inspired by this experimental concept should use China-style industrial cases as stress tests:

- **Can the platform explain why a work order is recommended?**
- **Can it say which agent checked asset risk, which agent checked inventory, and which agent blocked automation?**
- **Can it handle safety-critical assets without pretending the AI has authority it does not have?**
- **Can it connect inspection findings, telemetry, manuals, maintenance history, and spare-parts constraints into one planner-ready package?**
- **Can it learn from the final repair outcome without silently changing maintenance strategy?**

The practical north star is not full autonomy on day one. It is **high-trust decision compression**: reducing a planner's time to understand, verify, and approve the next action.

## 6. Governance boundary

This document uses public information to build product-design analogies. It does not claim that any named Chinese company operates the exact multi-agent CMMS/EAM architecture proposed in this repository. The architecture is a forward-looking reference model. The real examples show why the problem is important and why the data environment is becoming ready.

## Sources

- State Council of the People's Republic of China, **Notice on Issuing Made in China 2025**: <https://www.gov.cn/zhengce/content/2015-05/19/content_9784.htm>
- Ministry of Finance summary of State Council Made in China 2025 announcement: <https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/201505/t20150519_1233749.htm>
- MIIT Made in China 2025 topic page: <https://www.miit.gov.cn/ztzl/lszt/zgzz2025/index.html>
- MIIT media link on priority sectors and intelligent manufacturing: <https://www.miit.gov.cn/ztzl/lszt/zgzz2025/mtlj/art/2020/art_59d47f4319394d66b491522f44a6ad9f.html>


