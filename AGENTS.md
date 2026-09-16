# Personal Research OS 项目规则

## 项目边界

- 本仓库只负责个人投研系统的数据契约、研究模型、运行快照、复盘记录和后续工具代码。
- 不把投资结论当作事实，不把 NotebookLM 或 Agent 的草稿直接当作正式数据。
- 不在本仓库自动执行交易，不保存账号、Token、Cookie 或其他敏感凭据。

## 数据规则

- `raw/` 中的正式来源不可覆盖；来源变更必须创建新的 snapshot。
- `catalog/`、`models/`、`db/schema.sql` 和 `schemas/` 是 Git 管理的定义资产。
- `data/runtime/`、大体积原始文件和临时导出物默认不进入 Git。
- `runs/` 中的运行快照只追加，不修改历史判断。
- 每个正式判断必须能追溯到 source、metric、evidence、factor 和模型版本。

## 工作方式

- 修改数据契约或目录边界时，先更新 `docs/`，再修改实现。
- 新增主题时复制 `models/topics/real-estate/` 的模板，不复制已有结论。
- 不自动提交 Git；提交由用户明确要求后执行。
- 文档和配置默认使用 UTF-8 与 Markdown/YAML/JSON/SQL。
