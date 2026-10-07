# 🔎 DEEP RESEARCH SWARM

**广搜索. 深核验. 一份答案.**

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md)

> **状态：** `v0.1.0-beta`
> 一个面向 LobeHub 的公开 Beta 配置 —— 由一名 Curator 统一调度的六名专业化代理。本项目不是托管服务，也不是 LobeHub 官方产品。

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Release: beta](https://img.shields.io/badge/Release-beta-orange.svg)
![LobeHub](https://img.shields.io/badge/%E4%B8%BA-LobeHub-%E8%AE%BE%E8%AE%A1-1f6feb.svg)
![Multi-Agent](https://img.shields.io/badge/%E6%9E%B6%E6%9E%84-Multi--Agent-blueviolet.svg)
![Deep Research](https://img.shields.io/badge/%E5%9C%BA%E6%99%AF-Deep%20Research-2e7d32.svg)

---

## 为什么有本项目

大多数"研究型 Agent"把多种任务塞进同一个系统提示：检索、来源选择、阅读、核验、矛盾处理、撰写。DEEP RESEARCH SWARM 把这些任务拆给若干专职 Agent，由唯一的 Curator 协调。本项目的目标**不是**最大化代理数量，而是建立一个有纪律的证据流水线：

- 跨网页、GitHub、论坛、论文、官方文档并行检索；
- 优先原始来源而非转述；
- 让每条声明都能追溯到出处；
- 区分事实、来源主张、社区信号和假设；
- 发现并暴露矛盾，而不是掩盖；
- 在证据薄弱时进行二次定点核验；
- 最终交付**一份带有真实引用的连贯答案**。

## 架构

![Architecture](assets/architecture.svg)

```
用户
  │
  ▼
Curator / Research Director (Supervisor)
  │
  ├──► Wide Web Scout
  │       发现 · 查询 fan-out · 候选池
  │
  ├──► Primary Source Hunter
  │       官方文档 · 仓库 · 论文 · 公关材料
  │
  ├──► Evidence Analyst
  │       深读 · 证据台账 · 声明/实体/来源图
  │
  ├──► Fact Checker / Red Team
  │       矛盾搜索 · 引文审计 · 阻塞式质量门
  │
  └──► Research Synthesizer
          最终综合 · 不确定性 · 引用 · 可执行建议
```

这是 **由 Supervisor 控制的多对一星型拓扑**：专家把结果交回 Curator，不再递归互调。

## 六个代理

| 代理 | 职责 | 典型产出 |
|---|---|---|
| **Curator / Research Director** | 规划、调度、控制深度、合并证据、最终决策 | 研究计划、workstream、最终决策 |
| **Wide Web Scout** | 在广域检索候选空间 | 排序后的候选池 + 发现图 |
| **Primary Source Hunter** | 抓原始来源 | provenance-first 候选清单 |
| **Evidence Analyst** | 深读、抽取段落、建立台账 | Evidence Ledger + Claim/Entity/Source 图 |
| **Fact Checker / Red Team** | 试图**反驳**候选结论，运行阻塞式质量门 | PASS/FAIL 与缺口清单 |
| **Research Synthesizer** | 撰写唯一最终答案 | 单条 Markdown 消息，逐条声明带引用 |

每个代理的真实系统提示位于 `agents/`。

## 研究模式

Curator 根据问题自动伸缩努力程度。你也可以显式指定模式。

| 模式 | 使用场景 | 打开的来源 | Gap 轮次 |
|---|---|---|---|
| ⚡ QUICK | 单一事实 / 版本 / 价格 | 3–8 | 0 |
| 🔹 STANDARD | "对比 X 和 Y" | 8–20 | 0–1 |
| 🔎 DEEP | "寻找最佳替代" / 做决定 | 20–50 | 1–2 |
| 🧠 MAX | "研究市场" / 高错误成本 | 30–80 | 多次 |
| 🧬 ULTRA | 仅当显式说"最深" | 40–100 | 最大化闭合 |

详见 [`group/research-modes.md`](group/research-modes.md)。

## 你将获得

- **一份最终答案**：逐条声明都带引用，每条引用都对应一段原文。
- **真实的质量门**：Fact Checker 在发布前会尝试反驳答案。如果 FAIL，会进入循环直到关键缺口关闭或触发停止规则。
- **Evidence Ledger + 图**：每条声明有出处：来源类别、日期、检索日期、置信度、verdict。
- **与模式匹配的工作量**：简单问题得到快速答案；市场调研得到 30+ 来源。
- **MIT 开源许可**：不绑定供应商。

## 快速开始

1. 阅读 [`docs/lobehub-installation.md`](docs/lobehub-installation.md)，按步骤创建 LobeHub Group，添加六个代理，粘贴提示，启用必要工具。
2. 运行 [`tests/acceptance-test.md`](tests/acceptance-test.md)，在正式研究之前验证配置。
3. 试用 [`examples/quick-research.md`](examples/quick-research.md) 作为第一次跑通。
4. 试用 [`examples/deep-research.md`](examples/deep-research.md) 跑一次完整流水线。

## 文档

- [`docs/architecture.md`](docs/architecture.md) —— 架构设计思路
- [`docs/lobehub-installation.md`](docs/lobehub-installation.md) —— 安装指南
- [`docs/tools-and-skills.md`](docs/tools-and-skills.md) —— 每个代理使用的工具
- [`docs/evidence-ledger.md`](docs/evidence-ledger.md) —— 台账、置信度、声明图
- [`docs/citation-policy.md`](docs/citation-policy.md) —— 五步核验
- [`docs/quality-gate.md`](docs/quality-gate.md) —— 阻塞式质量门
- [`docs/troubleshooting.md`](docs/troubleshooting.md) —— 常见失败
- [`docs/known-issues.md`](docs/known-issues.md) —— 系统**未声称**的事情

## 示例

- [`examples/quick-research.md`](examples/quick-research.md) —— QUICK 流水线示例
- [`examples/deep-research.md`](examples/deep-research.md) —— DEEP 流水线示例
- [`examples/github-research.md`](examples/github-research.md) —— 原始来源优先
- [`examples/model-comparison.md`](examples/model-comparison.md) —— 对抗 + 基准归一化
- [`examples/long-form-technical-research.md`](examples/long-form-technical-research.md) —— MAX + 定点缺口闭合

## 仓库结构

```
DEEP-RESEARCH-SWARM-v0.1.0-beta/
├── README.md             ← 英文（主）
├── README.ru.md          ← 俄文
├── README.zh-CN.md       ← 简体中文
├── LICENSE               ← MIT
├── CHANGELOG.md
├── SECURITY.md
├── CONTRIBUTING.md
├── agents/               ← 六个代理的真实系统提示
├── group/                ← Group 提示、路由、模式、fallback
├── docs/                 ← 深度文档
├── tests/                ← acceptance + orchestration + secret scan
├── examples/             ← 5 个示例
```

## 设计灵感 / 相关工作

DEEP RESEARCH SWARM 的灵感来自以下公开记录的架构：

- Perplexity Deep Research
- OpenAI Deep Research
- Gemini Deep Research
- Kimi Researcher
- GPT Researcher
- DeerFlow
- LangChain Open Deep Research
- Anthropic 多代理研究（orchestrator-worker、四字段委派契约、努力档位、LLM-judge rubric）

本仓库**不包含**上述系统的任何专有提示，与上述任何组织**没有**关联、背书或支持关系。名称仅用于指明被记录在案的、对本项目设计产生影响的架构模式。

## 许可

MIT —— 见 [`LICENSE`](LICENSE)。