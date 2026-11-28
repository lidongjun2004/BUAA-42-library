# 一、Prompt说明

| 组号：学号-姓名 | 互评打分（满分40） |
| --- | --- |
| G28: 22371014-卢裕轩 | 40 |
| G28: | |

> 我们首先自己翻译了一个初版，然后利用大语言模型进行逐段落优化。每个段落用到的prompt均使用下述模版。

```text
请按照英文学术论文的语言规范润色下面这段英文，要求语气正式、用词准确学术、关联词恰当自然，给出旧的版本和修改后版本的对比，并说明每一处修改的理由：
......（待优化的段落）
```

## 二、优化记录（按论文结构依次进行优化）

## Abstract

### 🔹润色后版本（Revised Version）

> ## Abstract
>
> This study tackles the NP-hard problem of dynamic coordination in ultra-large-scale remote sensing satellite constellations through **SRFS-Transformer**, an integrated algorithm–system–hardware architecture. We present: (1) a Transformer-based planning model utilizing spatiotemporal attention mechanisms to fuse multidimensional constraints and construct a differentiable task representation space; (2) a ROS2-based distributed flight system (SRFS) that achieves microsecond-level scheduling via DDS middleware and heterogeneous multi-core processing; and (3) a digital twin verification framework leveraging Basilisk simulations coupled with Unity3D visualization. Experimental results demonstrate a **23.7× speedup in policy generation** and **1.8 ms per-step inference latency** for a 100-satellite constellation. This work offers a scalable and practical solution for autonomous mega-constellation operations with both military and commercial applications.
>
> **Keywords:** Transformer, SRFS, constellation planning, heterogeneous computing, NP-hard problems

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/表达 | 修改后 | 理由 |
| --- | --- | --- | --- |
| 语态统一 | “This study addresses NP-hard dynamic coordination challenges” | “This study tackles the NP-hard problem of dynamic coordination” | 语气更简洁、直接 |
| 标点规范 | “Transformer-based planning model employing spatiotemporal attention mechanisms” | “Transformer-based planning model utilizing spatiotemporal attention mechanisms” | “utilize”更书面化 |
| 结构调整 | 列表中“establishing a differentiable task representation space” | “construct a differentiable task representation space” | 动词统一，简洁 |
| 细节补充 | “ROS2-based distributed flight system (SRFS) achieving microsecond-level scheduling via DDS middleware and heterogeneous multi-core processing” | “ROS2-based distributed flight system (SRFS) that achieves microsecond-level scheduling via DDS middleware and heterogeneous multi-core processing” | 更完整的从句结构 |
| 精确用词 | “digital twin verification framework using Basilisk simulations and Unity3D visualization” | “digital twin verification framework leveraging Basilisk simulations coupled with Unity3D visualization” | “leveraging”语义更精准，强调结合 |
| 数字表达 | “Experiments demonstrate 23.7× faster policy generation and 1.8 ms per-step latency at 100-satellite scale” | “Experimental results demonstrate a 23.7× speedup in policy generation and 1.8 ms per-step inference latency for a 100-satellite constellation” | 表达更规范清晰 |
| 语义完整 | “This work provides a scalable solution for autonomous mega-constellation operations with dual military and commercial applicability” | “This work offers a scalable and practical solution for autonomous mega-constellation operations with both military and commercial applications” | 更符合学术语境，语义更通顺 |

## Introduction

### 🔹润色后版本（Revised Version）

## Introduction

### 1.1 Strategic Context

As global demand for Earth observation expands exponentially, remote sensing satellite constellations have entered an era of ultra-large-scale deployment. Leading systems, such as the US-based Planet Labs’ “Flock” constellation, operate over 200 micro- and nanosatellites to achieve global daily revisit capabilities. Concurrently, China’s “Nuwa Constellation” has completed its first-phase deployment of 138 satellites, enabling real-time transmission of sub-meter resolution data. However, as constellation sizes exceed 100 satellites, traditional mission management systems confront fundamental technical bottlenecks. Being a classic NP-hard problem, the solution space for constellation planning grows exponentially with the number of satellites.

Simultaneously, remote sensing systems are undergoing dual technological transitions. Regarding observation targets, missions evolve from point targets (instantaneous field-of-view coverage) to complex regional targets requiring multi-pass image stitching. From the platform perspective, traditional single-axis side-slipping Earth observation satellites (EOS) are being supplanted by three-axis agile Earth observation satellites (AEOS). This shift transforms the planning problem from single-satellite scheduling to dynamic, collaborative multi-satellite coordination. The NP-hard nature of this challenge critically constrains the efficiency of constellations comprising hundreds of satellites. Achieving minute-level responsiveness and inter-satellite autonomy under dynamic resource constraints has become a central challenge in optimizing constellation performance.

Within this strategic context, the Satellite Mission Management System (SMMS)—the “nerve center” of in-orbit satellite operations—plays a pivotal role in overcoming large-scale constellation limitations. Traditional SMMS architectures, constrained by centralized control and rigid scheduling strategies, reveal critical shortcomings in large-scale scenarios: (1) Coupled heterogeneous resource constraints—including attitude adjustments, onboard storage, and energy—impose multidimensional trade-offs; (2) Insufficient real-time responsiveness—emergency tasks, such as disaster monitoring, suffer unacceptable delays; (3) Scalability bottlenecks—mixed-integer programming approaches experience super-linear growth in computation time beyond 50 satellites. Although reinforcement learning methods show potential, their effectiveness in sparse-reward environments and modeling complex physical constraints remains limited.

To address these challenges, this study proposes the SRFS-Transformer collaborative planning framework, achieving breakthroughs through multi-level innovations:

We construct a dynamic planning architecture based on a Transformer neural network employing multi-head attention mechanisms. The encoder processes variable-length task sequences and captures spatiotemporal correlations across multiple targets via self-attention layers. The decoder ingests satellite state data, establishing a coupled mapping between task demands and satellite resource constraints within cross-attention layers, ultimately outputting a satellite control command matrix. Through differentiable modeling, this architecture integrates agile satellite dynamics and energy constraints directly into the attention weight calculations, enabling efficient control strategy generation.

To support onboard deployment of the Transformer model, we developed the ROS2-based SRFS (Space Ranger Flight Software) real-time flight software system [3]. The software adopts a distributed-node design, dedicating nodes to task planning (Transformer inference engine), fault-tolerance management, inter-satellite communication, and other functions. Microsecond-level message transmission is achieved via the DDS (Data Distribution Service) communication protocol. At the hardware level, a heterogeneous multi-core processor operates in a novel hot-redundancy mode: the primary core is exclusively reserved for Transformer model inference, while secondary cores run the SRFS operating system and synchronize system state via shared memory. This integrated system delivers three key performance breakthroughs:

1. **High Real-Time Performance**: Leveraging the ROS2 publish–subscribe framework, task scheduling latency remains stably within the hundred-microsecond range, meeting millisecond-level response requirements for attitude control commands.
2. **High Reliability**: A triple fault-tolerance mechanism—including heartbeat monitoring, cyclic node restarts, and a node-maintenance routine—ensures service continuity even amid single-node failures.
3. **Parallel Command Execution**: ROS2 Action interfaces enable concurrent processing of multi-satellite command streams, ensuring scalable, real-time operations across the constellation.

Together, these achievements establish an “algorithm–system–hardware” integrated technical paradigm for autonomous large-scale constellation control, advancing our nation’s aerospace information systems toward an intelligent, next-generation architecture.

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/表达 | 修改后 | 理由 |
| --- | --- | --- | --- |
| 语句通顺 | “As global demand for Earth observation grows exponentially” | “As global demand for Earth observation expands exponentially” | “expands”更贴切增长语境 |
| 术语统一 | “micro-nano satellites” | “micro- and nanosatellites” | 学术术语规范写法 |
| 结构优化 | “However, as satellite constellations scale beyond 100 units” | “However, as constellation sizes exceed 100 satellites” | 简洁且精准 |
| 逻辑清晰 | “Simultaneously, remote sensing systems face dual technological transitions” | “Simultaneously, remote sensing systems are undergoing dual technological transitions” | 语态统一，清晰 |
| 表达规范 | “transform the constellation planning problem from single-satellite scheduling to dynamic, collaborative multi-satellite coordination” | “transforms the planning problem from single-satellite scheduling to dynamic, collaborative multi-satellite coordination” | 主谓一致 |
| 句子合并 | “The NP-hard nature of this challenge fundamentally constrains the efficiency of constellations comprising hundreds of satellites.” | "The NP-hard nature of this challenge critically constrains the efficiency of constellations comprising hundreds of satellites. " | 连贯性加强 |
| 精确表述 | “Coupled heterogeneous resource constraints — factors such as attitude adjustment, storage, and energy impose multidimensional trade-offs;” | " Coupled heterogeneous resource constraints—including attitude adjustments, onboard storage, and energy—impose multidimensional trade-offs;" | 保持原意但精炼 |
| 句式调整 | “Although methods like reinforcement learning show promise, their effectiveness in sparse-reward environments and in modeling complex physical constraints remains insufficient.” | "Although reinforcement learning methods show potential, their effectiveness in sparse-reward environments and modeling complex physical constraints remains limited." | 更流畅准确 |
| 结构层次 | 将技术方案介绍分为架构设计、系统实现、硬件方案 | | 便于读者理解层次 |
| 细节补充 | 解释Transformer架构中encoder/decoder功能及其交互 | | 提升可读性 |
| 专业术语 | “microsecond-level message transmission is realized via the DDS communication mechanism” | "microsecond-level message transmission is achieved via the DDS (Data Distribution Service) communication protocol. " | 语言更规范 |
| 语义精准 | “a heterogeneous multi-core processor is employed, featuring an innovative hot-redundancy multi-core operating mode 详细说明 | "a heterogeneous multi-core processor operates in a novel hot-redundancy mode:" | 保持技术细节准确，精炼 |
| 句式简洁 | 三大系统突破点更规范呈现 | | 方便阅读 |
| 结尾提升 | "propelling our nation’s aerospace information systems toward an intelligent, next-generation architecture." | “advancing our nation’s aerospace information systems toward an intelligent, next-generation architecture” | 强化战略意义 |

## Related Work

### 🔹润色后版本（Revised Version）

> As remote sensing satellite constellations expand exponentially, traditional optimization algorithms are increasingly limited by escalating computational complexity. Recent studies reveal a technological evolution from region-specific customization to globally complex coverage paradigms. In regional scenarios, [4] proposes a multimodal ARM constellation for resource management in Africa, while [5] achieves a revisit interval of 15–35 minutes over the Indian subcontinent using a constellation of 12 SAR microsatellites. At the global scale, [6] presents a 72-satellite LEO constellation equipped with onboard AI computing capabilities, yet fails to address dynamic resource allocation. In addition, [7] introduces a two-dimensional grid-based optimization method for complex coverage, and [8] underscores the coordination challenges of heterogeneous sensors in the face of increasing miniaturization and scalability demands. However, most existing methods encounter NP-hard computational bottlenecks when scaled beyond one hundred satellites, highlighting the pressing need for the deep integration of intelligent algorithms with onboard systems.

------

### 🔍修改说明（Justification of Revisions）

| 原句 | 修改后句子 | 修改理由 |
| --- | --- | --- |
| **With the exponential growth...** | **As remote sensing satellite constellations expand exponentially...** | 使用“As...expand exponentially”结构更加自然且学术化。 |
| **constrained by surging computational complexity** | **limited by escalating computational complexity** | “Limited”更符合通用学术用语，“escalating”在描述复杂性增长方面比“surging”更准确。 |
| **Recent research indicates a technological shift...** | **Recent studies reveal a technological evolution...** | “Reveal”比“indicate”更清晰，“evolution”比“shift”更能体现从区域到全球的渐进过程。 |
| **regional applications** | **regional scenarios** | “Scenarios”语气更学术化且更贴合研究语境。 |
| **literature [4] designs... literature [5] achieves...** | **[4] proposes... [5] achieves...** | “Literature”重复使用显得累赘，改为直接引用编号简洁明了；“proposes”更符合对设计方案的表述习惯。 |
| **At the global scale** | **At the global scale** | 保留，原用法合适，未作改动。 |
| **with integrated onboard AI computing, yet fails...** | **equipped with onboard AI computing capabilities, yet fails...** | “Equipped with”更自然；“capabilities”增强技术表达完整性。 |
| **highlights the challenges of heterogeneous sensor coordination** | **underscores the coordination challenges of heterogeneous sensors** | “Underscores”在学术论文中更具强调意味；调整语序提升可读性。 |
| **under the trends of miniaturization and scalability** | **in the face of increasing miniaturization and scalability demands** | 改写为“in the face of...”更具逻辑性，“demands”体现技术压力。 |
| **when scaling beyond a hundred satellites** | **when scaled beyond one hundred satellites** | “Scaled”语态更自然；“one hundred”为规范学术写法。 |
| **underscoring the urgent need...** | **highlighting the pressing need...** | “Highlighting”比“underscoring”更符合连接句结构；“pressing”比“urgent”语气更平衡。 |
| **between intelligent algorithms and onboard systems** | **of intelligent algorithms with onboard systems** | “Integration of...with...”是标准搭配，提升语言流畅度。 |

------

### 🔹润色后版本（Revised Version）

> **(1) Intelligent Algorithms**
>
> Traditional mathematical programming techniques exhibit theoretical optimality in small- to medium-scale scenarios, but their computational efficiency deteriorates markedly as problem size increases. For example, [9] employs Sequential Convex Programming (SCP) for agile satellite attitude trajectory optimization but depends on precomputed grids, limiting scalability. [10] adopts a column generation approach for imaging sequence planning, yet overlooks the coordination of heterogeneous payloads. [11] proposes a semi-analytical constellation design algorithm that balances temporal resolution and deployment cost, though its static framework is ill-suited for dynamic mission environments. [12] compares various combinatorial optimization methods and observes that the solution space expands superlinearly with the incorporation of three-degree-of-freedom maneuvers. Collectively, these methods suffer from rigid modeling assumptions and poor computational scalability.
>
> To mitigate the scalability issues of conventional solvers, heuristic search algorithms seek to balance computational efficiency and solution quality through approximate optimization. For instance, [13] introduces a divide-and-conquer hybrid framework (EHE-DCF) that improves task completion rates by 18%, although its iterative nature impairs real-time responsiveness. [14] presents a foresighted heuristic that reduces response latency to the minute level, but its solution quality is highly sensitive to orbital configurations. [15] applies a saturated neighborhood tabu search strategy, improving imaging performance by 30%, yet sees a 40% drop in neighborhood generation efficiency as constellation size increases. These heuristics often fall victim to the curse of dimensionality and oversimplified physical models, resulting in significant gaps between simulated and in-orbit performance.
>
> Reinforcement learning (RL) introduces a promising end-to-end decision-making paradigm for dynamic planning tasks. [16] employs a Markov Decision Process (MDP) framework for priority-based scheduling of single satellites, achieving a 23% improvement in high-value target acquisition. [17] applies neural combinatorial optimization to the Traveling Salesman Problem (TSP), attaining near-optimal performance at the hundred-node scale. [18] uses Pointer Networks (Ptr-Net) to accommodate variable output structures, but 15% of the generated plans violate physical constraints. [19] combines Monte Carlo Tree Search (MCTS) with supervised learning, achieving an 80% reduction in runtime relative to genetic algorithms, albeit with an 18% generalization error on out-of-distribution tasks. Despite these advances, current RL methods remain limited by abstract state representations, inadequate modeling of physical laws, and insufficient capability for multi-satellite collaboration.
>
> In summary, existing research lacks planning methods that are both computationally efficient and capable of producing near-optimal solutions for large-scale satellite constellations within operational time constraints.

------

### 🔍修改说明（Change Justification）

| 原句 | 修改后句 | 理由 |
| --- | --- | --- |
| “approaches have demonstrated theoretical optimality” | “techniques exhibit theoretical optimality” | “Techniques”更正式，动词“exhibit”更学术化，避免重复使用“approach”。 |
| “diminishes significantly” | “deteriorates markedly” | 更精准的学术语言，“deteriorate”用于性能下降，“markedly”提升语气准确性。 |
| “literature [x]” | “[x]” | 省略“literature”符合标准论文引用写法，避免累赘。 |
| “enhancing imaging benefits” | “improving imaging performance” | “Performance”是更广义、更学术的术语，覆盖“benefit”的语义。 |
| “though neighborhood generation efficiency...” | “yet sees a 40% drop...” | 使用主动句式和“sees a drop”增强语言流畅性与清晰度。 |
| “these heuristic approaches often suffer...” | “These heuristics often fall victim...” | “Fall victim to”为地道表达方式，避免重复“suffer from”。 |
| “dynamic planning problems” | “dynamic planning tasks” | “Tasks”搭配“decision-making paradigm”更自然，提升语言紧凑性。 |
| “highlighting”/“underscoring” | “observes”/“introduces” | 统一学术动词选择，根据上下文强调“方法”和“现象”。 |
| “Current RL approaches are still constrained by...” | “Despite these advances, current RL methods remain limited by...” | 加入让步逻辑，更好衔接前后文；使用“remain limited by”更符合惯用表达。 |
| “within practical timeframes” | “within operational time constraints” | 更专业术语，“operational constraints”更符合卫星系统语境。 |

------

### 🔹润色后版本（Revised Version）

> **(2) Onboard Systems**
>
> As satellite constellations expand in scale, observation tasks become increasingly complex, requiring the processing of vast and continuously growing volumes of data. This trend has led to an escalating demand for enhanced onboard computational capabilities [20]. Currently, most small satellites utilize ARM-based processors (e.g., STM32, Tegra X2/X2i [21–30]) in conjunction with real-time operating systems (RTOS) such as VxWorks and μC/OS-II [31–33]. However, conventional microcontrollers (MCUs) and their associated RTOSs fall short in handling computationally demanding tasks such as neural network inference, highlighting the urgent need for upgraded multi-core embedded processors.
>
> While the development of multi-core onboard software based on Linux is technically viable—as demonstrated by the Aalto-1 nanosatellite [34]—its general-purpose design necessitates the integration of additional mechanisms for process communication and reliability assurance [35]. NASA’s F Prime framework is compatible with multi-core Linux environments; however, its task scheduling reliability remains insufficiently validated [36]. The Robot Operating System (ROS) has gained traction in aerospace applications due to its modularity. For instance, the CubeSat platform D3/PATCOOL has been verified under ROS [37–38], and JAXA has successfully integrated ROS with NASA’s cFS to enhance cross-platform portability [39]. Nevertheless, the centralized communication architecture of ROS1, which relies on a single master node, introduces inherent reliability vulnerabilities.
>
> ROS2, built upon the Data Distribution Service (DDS) communication standard, supports decentralized system architectures and offers improved real-time performance and fault tolerance [40–41]. Early applications in aerospace include a Raspberry Pi–based satellite control system developed by Politecnico di Torino [42], Micro-ROS–based implementations for attitude control [43], and NASA’s adaptation of ROS2 into the Space ROS framework for validation on Mars rovers [44]. However, these efforts remain limited in terms of real-time scheduling support and end-to-end system integration. Similarly, SpaceData’s Space Station OS has thus far achieved only high-level subsystem simulation [45].
>
> In summary, there is still no mature, robust ROS2-based aerospace flight software platform capable of supporting Transformer-scale onboard inference while simultaneously meeting the stringent requirements of real-time responsiveness and system reliability.

------

### 🔍修改说明（Change Justification）

| 原句 | 修改后 | 修改理由 |
| --- | --- | --- |
| “continue to scale” | “expand in scale” | 更正式表达，避免口语化；“expand”更贴合技术语境。 |
| “vast and growing data volumes” | “vast and continuously growing volumes of data” | 增加“continuously”以突出趋势，符合论文对趋势性分析的要求。 |
| “onboard computational capacity” | “onboard computational capabilities” | “Capabilities”更贴切于“能力范畴”，较“capacity”更广义。 |
| “are inadequate for” | “fall short in handling” | 用更自然、学术化的表达替代，且与“computationally demanding tasks”搭配更顺畅。 |
| “multi-core embedded processor upgrades” | “upgraded multi-core embedded processors” | 调整词序提升可读性；“upgraded processors”比“processor upgrades”更自然。 |
| “While developing...” | “While the development of...” | 将动名词改为名词结构，使句子更正式，符合技术写作风格。 |
| “non-aerospace-specific design” | “general-purpose design” | 使用更准确的术语，“general-purpose”是Linux常用描述，语义清晰。 |
| “remains unverified” | “remains insufficiently validated” | 更学术、更具体，“unverified”语义较弱。 |
| “poses reliability risks” | “introduces inherent reliability vulnerabilities” | 强化语气并使用更技术化术语“vulnerabilities”。 |
| “Preliminary explorations” | “Early applications” | “Applications”比“explorations”更符合“已部署实例”的语境。 |
| “remain limited in terms of...” | “remain limited in terms of real-time scheduling support and end-to-end system integration” | 更精确地指出限制点，增强逻辑性。 |
| “no mature and reliable” | “no mature, robust” | “Robust”在嵌入式系统中常用于描述容错性和稳定性，更贴切。 |
| “Transformer-level” | “Transformer-scale” | “Scale”更符合模型计算复杂度语境，“-level”略带模糊。 |
| “ensuring stringent real-time and reliability requirements” | “meeting the stringent requirements of real-time responsiveness and system reliability” | 拆解复合名词，使句子结构更清晰。 |

## Method

### 🔹润色后版本（Revised Version）

> ### (I) Hardware Layer
>
> The hardware layer ensures high reliability and real-time performance through a heterogeneous multi-core architecture and a multi-bus communication design. The system employs a Rockchip RK3588 as the primary control processor and an i.MX RT as the auxiliary processor. The overall architecture is depicted in Figure 1.
>
> The primary processor is responsible for compute-intensive tasks such as Transformer inference and image processing. To address the computational demands of Transformer models, the RK3588 integrates a dedicated Neural Processing Unit (NPU), optimized for accelerating matrix multiply–accumulate operations in attention mechanisms and for parallel feature extraction. During inference, input data is transferred from the main CPU to the NPU via shared memory. Leveraging a hard-coded operator library, the NPU decomposes computations into parallel pipelines and employs mixed-precision arithmetic on Tensor Cores to enhance throughput, achieving single-step inference latency within 10 milliseconds. The quad-core Cortex-A76 and quad-core Cortex-A55 CPUs form a heterogeneous cluster for dynamic task scheduling: the main thread oversees the NPU task queue and memory allocation, while auxiliary threads handle input preprocessing and output postprocessing. This CPU–NPU collaborative computing architecture maximizes hardware utilization.
>
> Image processing is performed using the RK3588’s multi-stage pipelined architecture. Raw image data is transmitted from the CMOS sensor to the integrated Image Signal Processor (ISP) via the MIPI bus. The ISP conducts essential preprocessing operations—including demosaicing, noise reduction, and dynamic range compression—outputting standardized RGB images. These are subsequently processed by the GPU, which executes compression and encryption algorithms to enable reliable high-speed data transmission under bandwidth constraints.
>
> Critical control signals are handled using a triple modular redundancy (TMR) mechanism with two-out-of-three majority voting. Three processors operate independently and in parallel to compute control instructions, which are forwarded to an arbitration module. The module compares outputs in real time: if all agree, the instruction is executed directly; if two match, the consensus result is adopted and the dissenting processor is isolated to preserve system integrity. Lightweight control tasks are executed concurrently across the processors and then voted upon, while high-load tasks are handled exclusively by the main processor to minimize overhead.
>
> The main processor interfaces with subsystems via multiple buses: the CAN bus connects to payloads; the MIPI bus provides high-speed links to the CMOS sensor; and the RS422 interface supports the telemetry and telecommand (TT&C) subsystem, ensuring robust command and data transmission. External sensors, peripheral switches, and timing signals are routed via GPIOs, forming a comprehensive perception–control loop at the hardware level.
>
> Time synchronization is achieved via an onboard multi-mode GNSS receiver that supports robust dual-frequency civilian signals including GPS L5, BeiDou B2I, and Galileo E5a. The receiver decodes UTC timestamps and satellite clock offsets from navigation messages and generates a Pulse Per Second (PPS) signal precisely aligned to Coordinated Universal Time (UTC). This rising edge triggers the satellite’s control unit through a hardware interrupt, resetting the internal second counter for hardware-level synchronization with nanosecond accuracy. Simultaneously, UTC timestamps are refined using software calibration algorithms and microsecond-resolution timers to compensate for propagation delays and oscillator drift, ensuring global temporal consistency.
>
> To ensure robustness in complex space environments, the system adopts a multi-source redundancy strategy that dynamically switches among GPS, BeiDou, and Galileo signals, prioritizing high-precision bands such as L5/B2I/E5a. This enables system-wide synchronization at the microsecond level. By integrating a time-division multiplexed CAN bus with a functionally partitioned heterogeneous multi-core architecture, the system achieves a balance between computational performance, real-time responsiveness, and operational reliability—providing a solid hardware foundation for the autonomous coordination of ultra-large-scale satellite constellations.

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/原结构 | 修改后 | 修改理由 |
| --- | --- | --- | --- |
| 语言准确性 | “compute-intensive tasks such as Transformer model inference and image processing” | “compute-intensive tasks such as Transformer inference and image processing” | 删去冗余词“model”，语义已明晰，语言更流畅。 |
| 表达凝练 | “leveraging a hard-coded operator library” | “Leveraging a hard-coded operator library” | 改为完整句开头，提升逻辑承接。 |
| 专业术语替换 | “quad-core Cortex-A76 and quad-core Cortex-A55 CPUs” | “The quad-core Cortex-A76 and quad-core Cortex-A55 CPUs” | 明确句子主语，句式更完整。 |
| 术语精度 | “standardized RGB output” | “standardized RGB images” | “Images”更具体，避免“output”含义模糊。 |
| 连贯性优化 | “Meanwhile,” | 删除“Meanwhile,”，改用并列句结构统一逻辑。 | 避免使用口语连接词，提升专业性。 |
| 技术准确性 | “high-load tasks are exclusively handled by the main processor to avoid unnecessary performance overhead.” | “…to minimize overhead.” | “Minimize”比“avoid unnecessary”更精确，语义更专业。 |
| 风格统一 | “the main processor communicates with each payload through the CAN bus” | “The main processor interfaces with subsystems via multiple buses…” | 精简列举，避免啰嗦，风格统一。 |
| 技术术语统一 | “peripheral switch signals” → “peripheral switches” | 简化术语表述，避免重复。 | |
| 逻辑清晰 | “GNSS receiver that captures robust, wide-bandwidth dual-frequency civilian signals such as…” | “GNSS receiver that supports robust dual-frequency civilian signals including…” | 使用“supports… including”表达支持范围，更清晰。 |
| 更学术表达 | “ensuring global consistency with UTC” | “ensuring global temporal consistency” | 使用更正式术语“temporal consistency”。 |
| 句尾强调 | “establishing a solid hardware foundation…” | “providing a solid hardware foundation…” | “Providing”语义更明确自然；避免句式重复。 |

------

### 🔹润色后版本（Revised Version）

> ### (II) System Layer
>
> The system layer is constructed atop the ROS2 framework, utilizing the DDS (Data Distribution Service) communication standard to implement a decentralized architecture. All nodes communicate directly in an end-to-end manner without reliance on any centralized management node, thereby significantly enhancing system flexibility and fault tolerance.
>
> Real-time performance is ensured by employing a Linux kernel patched with PREEMPT_RT (version 4.19.232-rt104), combined with ROS2’s priority-based scheduling mechanism. This guarantees that attitude-control command latencies consistently remain within the millisecond range.
>
> The CAN bus adopts a time-division multiplexing scheme to optimize bus resource utilization, with the sequential control flow illustrated in Figure 2. A timing-management node publishes a synchronization topic at fixed intervals. Upon detecting updates to this topic, the CAN-bus task-switching node immediately assesses the current bus occupation status. If the preceding payload node has released the bus, the task-switching node promptly publishes updated task-identification information. Each payload node subscribes to this topic and acquires bus send/receive privileges according to strict priority order, enabling orderly payload data transmission. Leveraging ROS’s parallel processing capabilities, once a preceding node completes data acquisition and enters processing, the subsequent node can immediately seize the bus to transmit its data. This pipeline-style mechanism markedly enhances bus utilization, fosters efficient multi-node collaboration, and improves real-time responsiveness.
>
> Node reliability is maintained through three core mechanisms: heartbeat monitoring, cyclic restart, and node maintenance.
>
> The heartbeat-monitoring mechanism combines hardware and software components, as depicted in Figure 3. Following reception of a heartbeat signal from the GPS and completion of time synchronization, the time-synchronization node issues a “feeding” signal to the onboard computer’s watchdog. Failure of the watchdog to receive this signal within a predefined interval triggers a system-wide reboot to prevent failures during operation. By integrating hardware watchdog functionality with the software system, this mechanism provides a fundamental guarantee for system stability.
>
> The cyclic restart mechanism utilizes ROS2’s service-based communication to verify node liveness in accordance with the information flow topology. As illustrated in Figure 4, an upstream node acts as a client, sending liveness-check requests to its downstream node server upon task completion. An active downstream node responds accordingly; otherwise, no response is returned. If multiple consecutive requests go unanswered, the downstream node is deemed inactive and a restart procedure is initiated to reboot it, ensuring uninterrupted information flow. This approach enables autonomous detection and recovery from internal anomalies. In theory, chained liveness checks allow the system to sustain orderly operation even in the face of multiple node failures, while each node enhances the reliability of its immediate predecessor.
>
> The node-maintenance mechanism is triggered by a dedicated remote command, as shown in Figure 5. Upon receipt of a maintenance command by the TT&C node, a corresponding maintenance topic is published to activate the mechanism. The maintenance node identifies the command type: for parameter updates, it modifies the target node’s parameters via the ROS2 parameter interface, enabling uninterrupted operation. For adding or modifying nodes—such as introducing a new image-processing node—the maintenance node creates or modifies source code files, compiles them, and launches the new node. Existing nodes are gracefully terminated prior to replacement, ensuring seamless updates.
>
> All nodes adopt the LifecycleNode interface to manage their lifecycles akin to a finite-state machine. Nodes transition among four principal states (Unconfigured, Active, Inactive, and Finalized) and six transitional states, enabling tight operational control; the state transition diagram is shown in Figure 6. For instance, after hardware configuration during initialization, the task-planning node enters the Active state; upon anomaly detection, it automatically terminates and releases resources to prevent fault propagation. Communication mechanisms are task-specific: timing signals and telemetry data are published as topics; image-processing tasks utilize Action interfaces to support asynchronous execution with state feedback; and maintenance commands dynamically adjust node parameters via the parameter interface. Collectively, these design elements form a multilayered, highly reliable, real-time interactive system.

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/表达 | 修改后 | 理由 |
| --- | --- | --- | --- |
| 语言流畅 | “is built upon the ROS2 framework and adopts the DDS…” | “is constructed atop the ROS2 framework, utilizing the DDS…” | 结构更紧凑，专业表达 |
| 术语精准 | “significantly enhancing system flexibility and fault tolerance” | 保持 | 精确表达核心优势 |
| 句式完善 | “Real-time performance is guaranteed by using a Linux kernel patched with PREEMPT_RT…” | “Real-time performance is ensured by employing a Linux kernel patched with PREEMPT_RT…” | 用词更正式、学术 |
| 逻辑清晰 | “When the CAN-bus task-switching node detects an update to this topic…” | “Upon detecting updates to this topic, the CAN-bus task-switching node immediately assesses…” | 减少被动结构，提升阅读流畅 |
| 语义明确 | “strict priority order” | 保持 | 明确调度策略 |
| 语言紧凑 | “Once a preceding node finishes data acquisition and enters its processing phase…” | “Once a preceding node completes data acquisition and enters processing…” | 更简洁，去除冗余 |
| 机制说明 | “heartbeat-monitoring mechanism is implemented via a combination of hardware and software” | “heartbeat-monitoring mechanism combines hardware and software components” | 更加简练清晰 |
| 专业术语 | “feeding” signal | 保持 | 术语标准 |
| 逻辑准确 | “If the watchdog does not receive this ‘feeding’ signal within a specified interval…” | “Failure of the watchdog to receive this signal within a predefined interval…” | 被动结构改主动，更正式 |
| 描述清晰 | “the cyclic restart mechanism leverages ROS2’s service-based communication to verify the liveness…” | 保持 | 技术描述准确 |
| 句式多样 | “After completing its task, the upstream node sends a liveness-check request…” | “Upon task completion, an upstream node sends a liveness-check request…” | 更自然流畅 |
| 语义精炼 | “If the downstream node is active, it responds to the request; otherwise, it does not.” | “An active downstream node responds accordingly; otherwise, no response is returned.” | 避免重复，简洁明了 |
| 逻辑强化 | “This mechanism guarantees self-detection and handling of internal information-flow anomalies.” | “This approach enables autonomous detection and recovery from internal anomalies.” | 更具学术严谨性 |
| 细节补充 | “If adding a new node… the maintenance node will create a new source-code file or modify an existing one…” | “The maintenance node creates or modifies source code files, compiles them, and launches the new node.” | 句子简洁且动作连贯 |
| 状态机描述 | “All nodes employ the LifecycleNode type to manage their lifecycles in a manner analogous to a finite-state machine.” | 保持 | 表达精准专业 |
| 细节丰富 | “The communication mechanisms are differentiated according to task requirements…” | 保持 | 突出系统设计合理性和针对性 |

------

### 🔹润色后版本（Revised Version）

> ### (III) Software Layer
>
> The software layer is designed following a **centralized training–distributed inference** paradigm, enabling intelligent and collaborative planning for ultra-large-scale satellite constellations via a Transformer-based model.
>
> #### 1. Centralized Training: Transformer Model with Multi-Constraint Integration
>
> During data collection, this study systematically aggregated historical mission data from thousands of real remote sensing satellites, accounting for diversity in orbital types, heterogeneous payload configurations, and dynamic task demands. Utilizing the Basilisk simulation platform, automated parameter tuning of MRP (Modified Rodrigues Parameters) was performed alongside validation of performance metrics. From a candidate pool of 1,000 to 2,000 satellites, random subsets ranging from 1 to 50 satellites were sampled to create constellation prototypes, ultimately generating a training dataset comprising millions of constellation combinations. A real-world scenario mapping mechanism was employed during simulation, associating each constellation instance with 50 to 300 randomly distributed ground observation targets, thereby constructing comprehensive space-ground collaborative training samples.
>
> To address complex operational scenarios, the research team developed a heuristic algorithmic framework grounded in dynamic constraints. This framework simulates typical applications such as emergency disaster monitoring and multi-target regional collaborative coverage, incorporating an adaptive task prioritization mechanism under energy constraints. By integrating multi-dimensional constraints—such as attitude maneuver windows, onboard energy consumption cycles, and storage capacity thresholds—a composite training sample library with high engineering relevance was established, providing a robust and realistic data foundation for training intelligent decision-making models.
>
> Building on this foundation, a Transformer model featuring 16-head attention mechanisms was designed. The input layer encodes both satellite state parameters and task requirement parameters. Satellite state inputs have dimensions of `batchsize × number of satellites × 53`, where each satellite is represented by parameters including solar panel status, momentum wheel data, RAAN, orbital elements, real-time position, remaining energy, storage capacity, and attitude angle range. Task requirement inputs have dimensions of `batchsize × number of tasks × 6`, with each task characterized by coordinates, progress status, release time, deadline, and required observation duration. The hidden layer dimension is set to 512. Spatiotemporal correlations across satellites and tasks are captured via self-attention mechanisms, while cross-attention layers establish dynamic mappings between task demands and satellite resource states. The model outputs the optimal task assignment strategy at each timestep, with dimensions of `batchsize × number of satellites × 1`, indicating the target task assigned to each satellite at the current moment.
>
> The training process comprises 100,000 epochs of iteration, during which differentiable satellite attitude dynamics and energy consumption models are embedded as physical constraint loss terms. This ensures that the resulting strategies strictly comply with the maneuvering capabilities and system constraints of agile satellites.
>
> #### 2. Distributed Inference: Onboard NPU Acceleration and Rolling Optimization
>
> Once trained, the Transformer model is lightweighted and deployed on the NPU (Neural Processing Unit) of the onboard RK3588 processor. Leveraging hardware-level parallel computation, the system achieves millisecond-level latency for single-step inference. During satellite operations, the model runs in a **rolling time-domain optimization** mode:
>
> At the start of each timestep *t*, the satellite executes attitude and orbit control commands predicted at timestep *t–1*. These commands include momentum wheel inputs, thruster ignition signals, magnetic torque actuator controls, sensor calibration instructions, and mode switching operations. Concurrently, based on the current constellation state, the model performs inference to asynchronously precompute control commands for timestep *t+1*, creating a dual-thread pipeline of **execution and prediction**.
>
> If any precomputed commands violate system constraints—such as exceeding attitude limits or insufficient energy reserves—a lightweight onboard heuristic correction algorithm is activated. This module dynamically replans feasible control actions according to real-time system status, ensuring reliable and safe operation in rapidly changing environments.
>
> By integrating onboard edge computing with closed-loop rolling optimization, the system realizes a full-cycle autonomous control process encompassing **current command execution, future action prediction, and real-time anomaly correction**. This capability supports minute-level coordinated responses and ensures high-reliability mission execution across ultra-large-scale satellite constellations.

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/表达 | 修改后 | 理由 |
| --- | --- | --- | --- |
| 逻辑连贯 | “this study systematically gathered historical mission data…” | “this study systematically aggregated historical mission data…” | “aggregate” 更符合数据集合的表达 |
| 术语统一 | “random subsets of 1 to 50 satellites were sampled” | “random subsets ranging from 1 to 50 satellites were sampled” | 明确范围表达，更自然 |
| 语言简洁 | “multi-dimensional constraints—such as attitude maneuver windows…” | 保持 | 表达清晰专业 |
| 结构优化 | “Transformer model with 16-head attention mechanisms” | “Transformer model featuring 16-head attention mechanisms” | 更流畅的表达 |
| 细节增强 | “input layer encodes both satellite state parameters and task requirement parameters” | 保持 | 结构合理 |
| 精确表达 | “outputs the optimal task assignment strategy at each time step” | “outputs the optimal task assignment strategy at each timestep” | 统一术语 |
| 句式变化 | “training process involves 100,000 epochs of iteration” | “training process comprises 100,000 epochs of iteration” | 更正式用语 |
| 细节补充 | “Once trained, the Transformer model is lightweighted and deployed…” | 保持 | 术语准确，语义明确 |
| 术语标准 | “dual-thread pipeline of execution and prediction” | 保持 | 专业术语表达 |
| 逻辑清晰 | “If any precomputed commands violate system constraints…” | 保持 | 语义完整 |
| 专业用词 | “a lightweight onboard heuristic correction algorithm is triggered” | “a lightweight onboard heuristic correction algorithm is activated” | “activated”更标准 |
| 结构紧凑 | “By integrating onboard edge computing with closed-loop rolling optimization…” | 保持 | 逻辑严密 |

## Experiment Results

### 🔹润色后版本（Revised Version）

> ### Experiment 1: Real-Time System Latency
>
> Given that CAN bus tasks in satellite missions are inherently periodic, the software system must comply with stringent real-time constraints. Prior work [46] has demonstrated that a ROS2 environment built on a PREEMPT_RT-patched Linux kernel can satisfy such requirements. Following this precedent, we constructed our environment using a Linux kernel version **4.19.232-rt104**. Here, *planned latency* is defined as the temporal deviation between the configured task period and the actual task activation time. Within this setup, we evaluated both the scheduling latency of the PREEMPT_RT-patched Linux kernel and the end-to-end latency of ROS2’s publish-subscribe mechanism—from message publication to reception.
>
> Scheduling performance was measured using the **cyclictest** tool [47]. A single real-time task was configured with a 1 ms period and deadline, assigned the highest possible priority (99) to assess the system’s peak performance. Tests were conducted under idle conditions and under full load, where the **stress-ng** tool simulated intensive computational overload by continuously running a diverse mix of CPU-intensive operations. This setup accurately reflects the system’s real-time behavior under extreme workloads.
>
> Figure 8 presents the scheduling latency evaluation results: Figure 8a shows latency in idle conditions, while Figure 8b reports results under full load. The maximum observed latency was **336 μs** at idle and **94 μs** under load. Despite the higher maximum latency under load compared to idle, both remain well within microsecond-level delays acceptable for the software system. Notably, no latency exceeding **500 μs** was observed, confirming the system’s real-time capabilities.
>
> To evaluate ROS2 publish-subscribe latency, we measured the time interval from message publication by a publisher node to reception by a subscriber node. Leveraging built-in timestamping in ROS2 logs, no additional instrumentation was necessary. As stringent real-time constraints apply primarily to the satellite’s mission management component, latency tests focused exclusively on messages pertaining to this module. Two scenarios were considered:
>
> 1. **Light-load state**: Only the mission management component active.
> 2. **Heavy-load state**: Concurrent execution of mission management and image processing tasks.
>
> Figure 9 depicts the ROS2 publish-subscribe latency results, with Figure 9a showing low-load conditions and Figure 9b illustrating high-load conditions. Latency fluctuated within a few milliseconds across both scenarios. Under light load, delays exceeding **10 ms** were rare, whereas such delays became more frequent under heavy load. Nevertheless, the maximum latency under heavy load remained below **20 ms**.
>
> Tables 1 and 2 provide detailed statistical summaries of ROS2 publish-subscribe latency. As system load increases, average latency exhibits a slight decrease, while standard deviation and maximum latency rise. Crucially, maximum latency consistently remains below **20 ms**, validating the system’s ability to satisfy real-time performance requirements.

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/表达 | 修改后 | 理由 |
| --- | --- | --- | --- |
| 术语精准 | “software system must satisfy real-time constraints” | “software system must comply with stringent real-time constraints” | “comply with” 更正式，强调严格要求 |
| 语言简洁 | “We adopted a similar software stack to construct our environment…” | “Following this precedent, we constructed our environment…” | 避免重复，逻辑顺畅 |
| 逻辑清晰 | “*Planned latency* is defined as…” | 保持，表述准确 | 术语定义明确 |
| 专业术语 | “evaluated the scheduling latency of the PREEMPT_RT-patched Linux system…” | “evaluated both the scheduling latency of the PREEMPT_RT-patched Linux kernel…” | “kernel”更准确 |
| 句式优化 | “Tests were conducted under both idle and fully loaded conditions…” | “Tests were conducted under idle conditions and under full load…” | 表达更简洁自然 |
| 细节丰富 | “with the stress-ng tool simulating computational overload…” | “where the stress-ng tool simulated intensive computational overload by continuously running…” | 补充描述，增强理解 |
| 数据表达 | “The maximum latency observed was 336 μs in idle conditions and 94 μs under load.” | “The maximum observed latency was 336 μs at idle and 94 μs under load.” | 语句更简洁 |
| 语义准确 | “microsecond-level delays remain acceptable…” | “both remain well within microsecond-level delays acceptable for the software system.” | 逻辑更严密 |
| 细节补充 | “no additional tools were required for measurement.” | “Leveraging built-in timestamping in ROS2 logs, no additional instrumentation was necessary.” | 表达更专业 |
| 术语统一 | “light-load state” | “light-load state” | 保持，表达明确 |
| 逻辑连贯 | “Two scenarios were evaluated:” | “Two scenarios were considered:” | 表达多样化 |
| 数字表达 | “latency fluctuates within a few milliseconds in both scenarios.” | “Latency fluctuated within a few milliseconds across both scenarios.” | 统一时态，表达更自然 |
| 细节精准 | “maximum latency under high load remains below 20 ms.” | “maximum latency under heavy load remained below 20 ms.” | 术语统一，时态准确 |
| 数据表达 | “Tables 1 and 2 provide detailed statistical results…” | “Tables 1 and 2 provide detailed statistical summaries…” | 用词更准确 |
| 逻辑严密 | “maximum latency consistently stays below 20 ms…” | “maximum latency consistently remains below 20 ms…” | 语态调整，表达更正式 |

------

### 🔹润色后版本（Revised Version）

> ### Experiment 2: Time-Step Deduction for Transformer
>
> To evaluate the real-time performance of different algorithms, we adopt **per-step computation latency** as a critical quantitative metric. This measure captures the computational delay required for an algorithm to complete a single iteration, directly reflecting system responsiveness.
>
> As shown in Figure 10, experimental comparisons demonstrate that the Transformer algorithm holds significant advantages when constellation scales dynamically expand:
>
> - Its per-step latency is markedly lower than that of heuristic algorithms.
> - Latency remains consistently stable at the **millisecond level**.
>
> Importantly, as constellation scales grow larger:
>
> - The Transformer’s computational latency increases at approximately **half the rate of heuristic algorithms**.
> - This indicates a **more favorable linear scaling relationship** between computational complexity and problem size for the Transformer.
>
> The Transformer’s stable millisecond-level latency provides it with **substantial practical value** for real-time satellite-ground communication scheduling applications.

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/表达 | 修改后 | 理由 |
| --- | --- | --- | --- |
| 语言精炼 | “we employ the per-step computation latency as a key quantitative metric” | “we adopt per-step computation latency as a critical quantitative metric” | 用词更准确，语句更简洁 |
| 句式优化 | “This indicator reflects the computational delay required for an algorithm to complete a single iteration” | “This measure captures the computational delay required for an algorithm to complete a single iteration” | 表达更流畅 |
| 逻辑连贯 | “experimental comparisons reveal that the Transformer algorithm exhibits significant advantages under dynamically expanding constellation scales” | “experimental comparisons demonstrate that the Transformer algorithm holds significant advantages when constellation scales dynamically expand” | 句式更自然 |
| 词汇准确 | “substantially reduced compared to heuristic algorithms” | “markedly lower than that of heuristic algorithms” | 专业表达 |
| 语态一致 | “Latency remains strictly stable at the millisecond level” | “Latency remains consistently stable at the millisecond level” | 统一表达 |
| 句式调整 | “when constellation scales expand to larger magnitudes” | “as constellation scales grow larger” | 更简洁自然 |
| 逻辑严密 | “The computational latency increase of Transformer is merely half that of heuristic algorithms” | “The Transformer’s computational latency increases at approximately half the rate of heuristic algorithms” | 更准确表达增长关系 |
| 词汇准确 | “more favorable linear relationship between computational complexity and problem scale” | “more favorable linear scaling relationship between computational complexity and problem size” | 术语统一，表达精准 |
| 结尾表达 | “substantial engineering value” | “substantial practical value” | 用词更符合实际应用背景 |

## Conclusion

### 🔹润色后版本（Revised Version）

> ## Conclusion
>
> This study introduces **SRFS-Transformer**, an integrated architecture designed to address the challenges of dynamic coordination and real-time responsiveness in ultra-large-scale remote sensing satellite constellations. By seamlessly integrating algorithm design, system software, and hardware implementation, SRFS-Transformer transforms traditional mission planning systems into a real-time, intelligent, and autonomous framework.
>
> At the algorithmic level, a Transformer-based spatiotemporal attention mechanism is developed to encode complex constraints—such as attitude dynamics, energy consumption cycles, and onboard storage capacity—into a differentiable task representation space. This approach effectively overcomes the scalability limitations inherent in traditional optimization algorithms and the physical modeling deficiencies commonly found in reinforcement learning.
>
> At the system level, the **Satellite Real-time Flight System (SRFS)**, built on the ROS2 middleware, achieves microsecond-level scheduling precision and sub-20 ms command latency by leveraging a heterogeneous multi-core architecture alongside a fault-tolerant design. Its modular structure, combined with real-time Linux and DDS-based communication, ensures robust performance under high-load, distributed operational conditions.
>
> Experimental results demonstrate that SRFS-Transformer delivers:
>
> - **23.7× faster policy generation** compared to traditional methods in 100-satellite scenarios;
> - **Millisecond-level inference latency** for per-step decision-making;
> - **Sub-500 μs jitter** and **sub-20 ms latency** under full computational load.
>
> The proposed methodology establishes a full-cycle paradigm encompassing algorithm iteration, digital twin simulation, and hardware deployment, providing both theoretical foundations and practical feasibility for the control of future mega-constellations. SRFS-Transformer lays the groundwork for evolving remote sensing satellites from passive data collectors into intelligent autonomous agents, enabling responsive, scalable, and commercially viable space operations.

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/表达 | 修改后 | 理由 |
| --- | --- | --- | --- |
| 词汇提升 | “proposes SRFS-Transformer, an integrated architecture that addresses the challenges” | “introduces SRFS-Transformer, an integrated architecture designed to address the challenges” | 语气更正式，表达更专业 |
| 逻辑顺畅 | “tightly coupling algorithm design, system software, and hardware implementation” | “seamlessly integrating algorithm design, system software, and hardware implementation” | 更自然的连接词汇 |
| 细节补充 | “energy cycles” | “energy consumption cycles” | 使表达更具体准确 |
| 词汇准确 | “physical modeling deficiencies of reinforcement learning” | “physical modeling deficiencies commonly found in reinforcement learning” | 说明更清晰 |
| 专业术语 | “sub-20 ms command latency” | “sub-20 ms command latency by leveraging a heterogeneous multi-core architecture” | 强调技术手段 |
| 结构优化 | “modular construction, together with real-time Linux and DDS-based communication” | “modular structure, combined with real-time Linux and DDS-based communication” | 更简洁流畅 |
| 表达统一 | “Experimental results demonstrate that SRFS-Transformer achieves” | “Experimental results demonstrate that SRFS-Transformer delivers” | 语言更凝练 |
| 语法规范 | “23.7× faster policy generation than traditional approaches in 100-satellite scenarios” | “23.7× faster policy generation compared to traditional methods in 100-satellite scenarios” | 语法更规范 |
| 结尾凝练 | “laying the groundwork for transforming remote sensing satellites from passive data collectors into intelligent agents of autonomous decision-making” | “laying the groundwork for evolving remote sensing satellites from passive data collectors into intelligent autonomous agents” | 语言更精炼，句式更紧凑 |

## Future Work

### 🔹润色后版本（Revised Version）

> ## Future Work
>
> Building on the demonstrated capabilities of SRFS-Transformer, future work will focus on strategic expansion across both commercial and deep-space domains.
>
> ### 1. **Scalable Commercial Ecosystem**
>
> Leveraging onboard deployment of lightweight Transformer models and real-time rolling optimization, the SRFS system is poised to support a variety of commercial applications:
>
> - **Cross-domain resource sharing:** Real-time switching between remote sensing and communication modes enables infrastructure sharing with LEO operators, thereby enhancing satellite return on investment (ROI).
> - **High-value data services:** AI-powered onboard preprocessing facilitates rapid-response applications such as agricultural insurance claims and energy pipeline monitoring.
> - **Open API ecosystem:** Modular ROS2 nodes expose scheduling and sensing capabilities through standardized APIs (e.g., `/task/priority`, `/sensor/calibration`), allowing downstream developers to integrate services like carbon monitoring, urban planning, and disaster response.
>
> These features position SRFS-Transformer as a core platform within a future “data subscription – algorithm service – industry collaboration” ecosystem, with plans to engage over 200 enterprise partners.
>
> ### 2. **Strategic and Lunar Deployment**
>
> The modular and adaptable design of SRFS-Transformer enables future applications in deep-space and lunar environments:
>
> - **Lunar navigation constellations:** The architecture can support networks such as Queqiao-2 and beyond, enabling terrain-aware scheduling, precise coordination of lunar rovers, and persistent positioning accuracy on the order of 10 cm.
> - **Transfer learning for new environments:** Transformer models trained in Earth orbit may be fine-tuned for lunar or interplanetary missions, leveraging shared attention mechanisms to facilitate dynamic coordination in unstructured and novel environments.
>
> This strategic vision reinforces China’s leadership in autonomous space systems and positions SRFS-Transformer as a foundational platform for establishing international standards in Commercial Space 2.0 and the emerging lunar economy.

------

### 🔍修改说明（Change Justifications）

| 类型 | 原句/表达 | 修改后 | 理由 |
| --- | --- | --- | --- |
| 句式精炼 | “Building upon the demonstrated capabilities” | “Building on the demonstrated capabilities” | 更简洁自然 |
| 语态统一 | “the SRFS system supports multiple commercial applications” | “the SRFS system is poised to support a variety of commercial applications” | 语气更正式、预期未来发展 |
| 专业词汇 | “enhancing satellite ROI” | “enhancing satellite return on investment (ROI)” | 首次出现时写出全称，增强专业性 |
| 结构调整 | 列举商业应用时增加“Leveraging…” | 更明确表达依托的技术基础 | |
| 细节补充 | “AI-enabled onboard preprocessing supports rapid applications” | “AI-powered onboard preprocessing facilitates rapid-response applications” | 语义更明确，强调响应速度 |
| 术语准确 | “Open API ecosystem” | “Open API ecosystem” 保持一致，结构清晰 | |
| 语法流畅 | “modular ROS2 nodes expose scheduling and sensing functions via standardized APIs” | “Modular ROS2 nodes expose scheduling and sensing capabilities through standardized APIs” | 表达更简洁且学术化 |
| 逻辑优化 | “These capabilities position SRFS-Transformer as a core platform…” | “These features position SRFS-Transformer as a core platform within a future…” | 逻辑更连贯 |
| 词汇提升 | “modular and transferable nature” | “modular and adaptable design” | 术语更贴合设计特点 |
| 精确表达 | “persistent 10 cm-level positioning accuracy” | “persistent positioning accuracy on the order of 10 cm” | 科学表述更准确 |
| 补充细节 | “leveraging shared attention structures” | “leveraging shared attention mechanisms” | 术语更规范 |
| 语句凝练 | “positions SRFS-Transformer as a foundational platform in setting international standards” | “positions SRFS-Transformer as a foundational platform for establishing international standards” | 语句更简洁 |
