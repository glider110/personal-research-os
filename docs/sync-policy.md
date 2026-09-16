# 本地 Git 与 Drive 同步规则

## 权威边界

- Git 是定义资产的权威来源：`docs/`、`models/`、`schemas/`、`db/schema.sql`、`prompts/` 和配置文件由 Git 管理。
- Google Drive 是原始资料和跨工具交换区：`inbox/`、`raw/`、`exports/` 可以同步到 Drive。
- `data/runtime/` 下的 SQLite 数据库是本机运行产物，不通过 Drive 多机并发编辑。

## 推荐同步流程

1. 将报告、数据文件或 NotebookLM 导出物放入 `inbox/`。
2. Agent 或人工确认来源、发布日期和文件 hash。
3. 合格资料移动到 `raw/`，并在 `catalog/` 建立来源登记。
4. 提取指标和证据，写入 SQLite/Parquet 或相应的模型文件。
5. 生成 `exports/` 中的可读材料，供 NotebookLM 继续分析。
6. 模型和规则变更通过 Git diff 检查；运行结果写入 `runs/`，不覆盖旧文件。

## 注意事项

- 不建议多个设备同时通过 Drive 修改同一个 Git 工作树。
- 不把 `.git/`、运行数据库和临时缓存当作 NotebookLM 的资料来源。
- Drive 文件被替换时，必须检查 hash 并创建新 snapshot，不能静默覆盖旧来源。
