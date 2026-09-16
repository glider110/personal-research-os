# 因果研究台（Personal Research OS）

这是一个面向个人长期投研的本地研究系统。它把原始资料、标准化指标、证据、因子、因果模型、行为树、运行快照和复盘结果组织成可追溯、可版本化的研究资产。

当前阶段只搭建数据和知识架子，暂不包含前端。后续网页只是这些对象的一个阅读、编辑、运行和复盘界面。

## 核心原则

- 原始来源必须可追溯，但原始文件不直接塞进 SQLite。
- 因子是对证据的解释，不能替代原始数据。
- 因果模型和行为树分开：前者描述机制，后者控制研究流程。
- 正式判断必须绑定数据、模型、规则和运行版本。
- 运行快照只追加、不覆盖，复盘时不能事后改写历史判断。
- Drive 用于同步资料和导出物，Git 管理定义、模型、规则和代码。

## 目录速览

```text
inbox/                         Drive/NotebookLM 待整理输入
raw/<主题>/<type>/              原始资料：先按内容、再按类型（不可覆盖）
catalog/                       来源、指标、证据等登记信息
models/topics/                 各主题的因子、因果图、情景和行为树
db/schema.sql                 SQLite 结构定义
data/normalized/               指标时间序列（Parquet 等）
data/runtime/                  本地运行数据库，不进入 Git
runs/                          不可覆盖的研究运行快照
reviews/                       结果验证和错误归因
exports/                       给 NotebookLM 或人工阅读的导出物
prompts/                       NotebookLM 与 Agent 的任务模板
docs/                          系统设计和同步规则
schemas/                       对象字段约定
```

## 建议工作流

源文件统一按“内容主题 → 文件类型 → 来源 → 快照版本”整理，支持视频、音频、PDF、Markdown、文本、图片、网页、Excel 等资料的归档。详见 [源文件整理规则](docs/source-organization.md)；各类自动解析器尚未实现。

```text
inbox
  -> raw
  -> catalog/source
  -> metric/evidence
  -> factor state
  -> causal model/scenario
  -> behavior tree run
  -> run snapshot
  -> review
```

## 第一阶段范围

房地产是第一个验证主题，但这里只放模型模板，不预置房地产市场结论。先完成一次手工导入、因子评估、行为树运行和历史快照，再扩展到其他行业。

## 当前状态

- 数据架子：已建立
- SQLite schema：已建立
- 前端：未开始
- 自动抓取：未开始
- 真实研究结论：未录入
