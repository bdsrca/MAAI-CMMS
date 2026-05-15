# Real-Life Chinese Industrial Examples for Multi-Agent CMMS/EAM

The examples below are not presented as deployments of this repository's architecture. They are public digitalization signals that reveal where future agentic CMMS/EAM systems can create value. The useful question is: **what kind of maintenance reasoning does each example force a platform to coordinate?**

![Chinese Industrial Exemplars for Agentic CMMS/EAM](../assets/china-industrial-exemplars.svg)

![Agentic EAM Fit Matrix](../assets/china-agentic-eam-fit-heatmap.svg)

## Example 1: Midea / MBT — AI-enabled chiller and compressor operations

**Public signal.** Midea Building Technologies has publicly described its Chongqing chiller factory as a full-process AI-empowered chiller lighthouse factory. Midea Industrial Technology also presents a broad smart-factory and industrial-technology footprint.

**CMMS/EAM lesson.** Chillers, compressors, pumps, valves, motors, and energy systems create a natural bridge between production assets, product service, energy optimization, and spare-parts planning. A future CMMS/EAM platform should not treat a chiller alarm as a simple ticket. It should ask: Is energy consumption changing? Is this a repeat event? Is the compressor under warranty? Are bearings, sensors, or filters available? Can the work be done without disrupting production?

**MAS workflow.**

1. Intake Agent normalizes the symptom: abnormal noise, energy increase, vibration hint.
2. Asset Agent checks criticality, service history, failure modes, and operating context.
3. Energy Agent compares consumption and load pattern.
4. Inventory Agent checks likely spares and lead times.
5. Policy Agent blocks auto-write if the asset is high criticality or if production downtime is required.
6. Human planner receives a review package with recommended inspection, parts, risk, and alternatives.

## Example 2: SANY Group — intelligent heavy-equipment manufacturing and field-service loops

**Public signal.** SANY describes No. 18 Factory as a 100,000-square-meter intelligent manufacturing pilot factory approved by China's Ministry of Industry and Information Technology.

**CMMS/EAM lesson.** Heavy equipment companies face two maintenance worlds at once: the factory assets that build machines and the deployed machines operating in the field. Agentic CMMS/EAM can connect factory quality, equipment telemetry, warranty, parts, dealer service, and customer downtime into a shared reasoning process.

**MAS workflow.** A Field Fleet Agent sees recurring hydraulic warnings from a machine family. A Reliability Agent checks whether similar factory or warranty issues exist. An MRO Agent checks component availability. A Vendor/Dealer Agent prepares service routing. A Policy Agent prevents customer-impacting commitments until a human service supervisor approves the plan.

## Example 3: State Grid — drone inspection to maintenance orchestration

**Public signal.** State Grid examples show drone-based grid inspection, AI defect recognition, and inspection-to-work-order dispatch. A Jiangsu State Grid example describes drones performing autonomous inspections and AI algorithms identifying defects and issuing handling orders to equipment-management units.

**CMMS/EAM lesson.** Drone inspection is not valuable only because it captures images. It becomes valuable when the platform can convert inspection findings into prioritized, safe, auditable maintenance action. Grid work also requires weather, access, outage risk, crew safety, asset criticality, and approval routing.

**MAS workflow.**

1. Inspection Agent classifies image evidence and confidence.
2. Grid Asset Agent checks line importance, failure history, and surrounding hazards.
3. Safety Agent checks live-line, weather, access, and personal-risk constraints.
4. Dispatch Agent proposes crew and time window.
5. Policy Agent routes approval or blocks automation.
6. Audit Agent stores image evidence, defect class, agent reasoning, and final disposition.

## Example 4: CRRC — rail fleet lifecycle intelligent O&M

**Public signal.** CRRC has described SmartCare intelligent O&M as integrating vehicle and ground data to provide lifecycle intelligent operation and maintenance services.

**CMMS/EAM lesson.** Rail is a strong test case because decisions are safety-critical, asset-rich, parts-heavy, and schedule-sensitive. A good agentic EAM system must combine vehicle telemetry, depot constraints, spare parts, safety standards, service contracts, and human approval.

**MAS workflow.** A Fleet Agent identifies a risk pattern across vehicles. A Safety Agent checks mandatory inspection rules. A Schedule Agent proposes a depot window. An Inventory Agent checks components. A Human Review Agent routes the package to the appropriate supervisor. Live changes to fleet availability should remain human-approved unless the action is low-risk and explicitly allowed.

## Example 5: Huawei — industrial digital infrastructure as the data layer

**Public signal.** Huawei's fully connected factory materials emphasize IT/OT convergence, Wi-Fi 7/UWB, unified communications for production devices, visualized OT networks, and direct device data transmission.

**CMMS/EAM lesson.** Agentic maintenance needs a trustworthy context layer before it needs fancy autonomy. Sensors, OT networks, historians, MES, CMMS, ERP, procurement, and documents must be connected under identity, segmentation, latency, security, and observability constraints.

**MAS workflow.** A Connectivity Agent validates whether machine data is fresh and complete. A Security Agent ensures tools do not cross OT boundaries. A Data Quality Agent labels unreliable signals. The maintenance agents use only trusted context.

## Example 6: Sinopec — smart-factory and process-plant maintenance

**Public signal.** Sinopec describes smart-factory construction based on the Sinopec Smart Cloud industrial Internet platform, with closed-loop production optimization.

**CMMS/EAM lesson.** Petrochemical and process industries are ideal for policy-aware maintenance. Shutdown work, permits, LOTO, hazardous areas, spare-parts staging, contractor coordination, and production loss all interact. This is where multi-agent reasoning can be extremely useful, but where write actions must be tightly governed.

**MAS workflow.** A Shutdown Agent creates a rough job package. A Permit Agent checks LOTO and hazardous-work requirements. An Inventory Agent verifies staging. A Risk Agent estimates operational impact. A Policy Agent enforces approval gates. A human turnaround planner remains accountable.

## Example 7: Haier COSMOPlat — industrial Internet platform and ecosystem orchestration

**Public signal.** Haier describes COSMOPlat as an industrial Internet platform that covers industrial platform construction, intelligent factory services, software/hardware integration, and energy-management businesses.

**CMMS/EAM lesson.** A multi-agent CMMS/EAM system improves when it has a common industrial data fabric. Platform examples such as COSMOPlat point toward cross-factory context, partner coordination, energy management, and shared learning loops.

**MAS workflow.** A Platform Agent resolves tenant/site context. An Energy Agent checks facility energy constraints. A Partner Agent checks service/vendor obligations. A Data Agent validates master data. The final review package explains which ecosystem signals were trusted and which were ignored.

## Example 8: Baowu / Baosteel — online inspection and heavy process reliability

**Public signal.** Baosteel presents BaoVision online surface inspection technology for high-speed production. Public summaries also describe Baowu's broader digital and intelligent transformation.

**CMMS/EAM lesson.** Steel production connects quality, process stability, equipment condition, safety, and energy consumption. An agentic maintenance platform can link online inspection defects to process equipment, recent maintenance, operator interventions, and reliability-improvement work.

**MAS workflow.** A Quality Agent detects a defect pattern. A Process Asset Agent checks mills, cooling, sensors, and prior work. A Reliability Agent proposes RCA. A Maintenance Agent drafts corrective work. A Cost Agent compares scrap risk, downtime risk, and maintenance cost.

## Cross-example design patterns

| Pattern | Why it matters | Agentic CMMS/EAM implication |
| --- | --- | --- |
| Inspection-to-work-order loop | Drones, machine vision, and AI defect recognition create more findings than humans can manually triage. | Need Inspection Agent + Asset Agent + Policy Agent + Dispatch Agent. |
| Asset-service-production loop | Manufacturers increasingly connect factory assets, shipped products, service, warranty, and spares. | Need Service Agent + MRO Agent + Reliability Agent. |
| Safety-critical approval loop | Grid, rail, petrochemical, and heavy industry cannot tolerate casual autonomous writes. | Human approval and deterministic policy gates are core architecture. |
| Data-platform dependency | MAS quality depends on clean asset hierarchy, fresh telemetry, and reliable identity/security boundaries. | Need Data Quality Agent + Security Agent + Integration Agent. |
| Continuous learning loop | Every repair outcome should improve future diagnosis, PM strategy, and spare-parts planning. | Need Audit Agent + Feedback Agent + Evaluation pipeline. |

## Sources

- Midea Building Technologies, AI-powered chiller lighthouse factory: <https://mbt.midea.com/global/news/ai-zero-carbon--the-world-s-first-fully-ai-powered-chiller-light>
- Midea Industrial Technology: <https://industry.midea.com/en>
- SANY Group, No. 18 Factory: <https://www.sanyglobal.com/video/145/>
- State Grid Jiangsu, drone inspection and AI defect recognition: <https://www.js.sgcc.com.cn/xwzx/jcdt/2025/287.shtml>
- State Grid / EPRI, AI data set for transmission-line drone inspection defects: <https://www.epri.sgcc.com.cn/html/chinasperi/gb/jyyw2/xyzx/20250515/856984202505151254000001.shtml>
- CRRC, SmartCare intelligent O&M: <https://www.crrcgc.cc/en/2024-09/27/article_2024092715480084389.html>
- Huawei Enterprise, fully connected smart factory: <https://e.huawei.com/en/industries/manufacturing/production-and-supply/fully-connected-smart-factory>
- Sinopec, smart factories and Sinopec Smart Cloud: <https://www.sinopecgroup.com/group/en/000/000/041/41714.shtml>
- Sinopec, digital production and smart-factory construction: <https://www.sinopecgroup.com/group/en/000/000/065/65832.shtml>
- Haier COSMOPlat: <https://www.haier.com/global/haier-ecosystem/cosmoplat/>
- COSMOPlat platform: <https://cosmoplat.com/en>
- Baosteel online surface inspection: <https://rd.baosteel.com/zypt//en/ability/see/abilityDetailsBSSF1/2/19b24dcfb0f747e581d919c6186a6880>
- English.gov.cn / Xinhua summary of Baowu digital and intelligent transformation: <https://english.www.gov.cn/news/202406/23/content_WS66782834c6d0868f4e8e8774.html>
