# 处理结果包与首轮研究流程

## 目的与边界

用同一个 JSON 处理结果包接收本地 Agent、NotebookLM 和人工整理结果，先保留原始输入，再校验引用、入库、生成不可覆盖的运行快照及复盘。浏览器读取是独立采集步骤；核心 CLI 不依赖登录态，也不保存凭据。

NotebookLM 页面导出是“该工具曾输出这些内容”的来源，不能冒充其引用的原始统计资料。页面只读到了部分内容时，必须记录 `coverage=partial`。视频转录片段不等于已下载视频原文件。原站网页需要另建来源并独立核对。

## 结果包

`90-system/02-schemas/processing-package.schema.json` 定义机器可校验的字段。包内包含：

- `schema_version`、`id`、`topic`、`created_at`：稳定身份与版本。
- `producer`：工具、模型（不知道时填 unknown）、提示词版本、处理方式。
- `sources`：来源身份、来源类别、实际文件类型、原网址、发布时间、采集时间、文件路径、SHA-256、覆盖范围。路径相对结果包所在目录。
- `evidence`：事实候选或工具说法、原文摘录、来源引用、定位、审核记录。只有原始资料中核对过的片段可以标为 verified。
- `metrics`：指标定义、单位、频率、时间范围、口径与数值，必须引用对应证据。`value_text` 保存原文数字，`value_transform` 明确直接读取或取负；程序核验数字是否存在、转换是否一致，语义与统计口径仍需来源审核。
- `analysis`：因子、因果假设（机制、时滞、范围、反证）、条件性情景、研究问题、数据截止日期及下一步。这些始终是待人工审核的解释。

来源分类 `primary`、`secondary`、`ai_generated`、`user_authored` 与文件类型分开。浏览器归档文件实际为 TXT 时归入 `txt/`，另用 `original_type` 标记它来自视频、网页或 Markdown。不能用改扩展名假装下载了原件。

## 目录和版本

- 待导入包：`01-inbox/<批次>/package.json` 和配套文件。
- 原始输入：`02-sources/<主题>/<type>/<source-id>/<snapshot-id>/<文件名>`。
- 结构化包：`03-library/08-packages/<主题>/<package-id>/package.json`。
- 本地数据库：`90-system/07-runtime/research.sqlite3`。
- 来源索引：`03-library/06-catalog/imports/<package-id>.json`，为包/数据库的派生索引。
- 模型冻结：运行快照内嵌本次 analysis 及哈希，另记录仓库模型文件哈希，避免配置变更使旧运行失真。
- 运行：`05-runs/<run-id>.json` 及配套 Markdown；复盘：`06-reviews/<review-id>.json` 及 Markdown。

所有归档使用稳定内容哈希，重复导入同 ID 同内容为幂等操作；同 ID 不同内容报错。导入前校验全部文件和引用；失败不留下半批数据库记录。文件写入只允许相同内容重试，不覆盖已有不同内容。

## 审核、时间与复盘

- 原始证据 `verified` 只表示摘录和口径已被本地 Agent 核对，不代表用户批准投资判断。
- AI 草稿证据只能为 pending/rejected；正式指标只从 verified 的非 AI 证据生成。
- 因子和情景仍是 `pending_human_review`，运行不得自动发布投资建议或执行交易。
- 运行校验已核对证据的来源 `published_at <= as_of_date`，且指标 period_end 不得晚于截止日期；否则阻止其进入当时判断。待核验讨论仅作为研究线索，不作为当时已知事实。
- 历史资料在今天补录，只能称历史重建，不能宣称当时真实预测或无前视偏差回测。模型本身也可能包含后见信息。
- 首轮复盘是数据和流程审计，记录口径错误、证据缺口、采集不完整；未来结果未到或缺少结果来源时标记未验证，不能伪造“预测成功”。

## 命令

```bash
python3 90-system/03-scripts/research.py validate 01-inbox/<批次>/package.json
python3 90-system/03-scripts/research.py import 01-inbox/<批次>/package.json
python3 90-system/03-scripts/research.py run <package-id>
python3 90-system/03-scripts/research.py review <run-id>
python3 90-system/03-scripts/research.py status
python3 -m unittest discover -s tests -v
```

第一版仅实现结构化结果包导入、核验、SQLite 入库、研究门禁、快照和数据审计。自动理解所有文件格式、自动登录 NotebookLM、市场结果自动复盘不在本轮实现范围。

## 跨主题共享

导入同时登记全局共享对象、定义版本与批次使用关系。指标定义不含观测期间/数值，因子定义不含评估状态。完全相同定义跨批次复用；指标和因子可填写可选 `shared_id` 明确沿用身份，定义改变生成新版本。已有 v1 包继续兼容。执行 `python3 90-system/03-scripts/research.py library` 补建共享索引并刷新阅读入口；引用不自动等于支持，详见 [共享研究库设计](shared-library-design.md)。
