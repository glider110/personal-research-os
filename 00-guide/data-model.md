# 数据模型说明

## 分层

系统不把“数据”理解成一张表，而是六种有边界的对象：

1. `source` / `source_snapshot`：原始来源和不可覆盖的版本。
2. `metric` / `metric_observation`：有单位、频率、口径的标准化指标及观测值。
3. `evidence`：可引用、可定位、支持或反驳某个判断的事实。
4. `factor_definition` / `factor_state`：因子的稳定定义和某个时间点的状态。
5. `causal_edge` / `scenario`：因果关系、作用机制和条件性情景。
6. `behavior_rule` / `run_snapshot` / `review`：研究流程、不可覆盖的运行结果和后续校准。

## 物理存储

| 内容 | 首选存储 | 原因 |
|---|---|---|
| PDF、网页、CSV、Excel、API 原始返回 | Google Drive 的 `02-sources/` | 体积大，适合文件同步 |
| 来源登记、指标定义、因子状态、关系和规则 | SQLite | 需要查询和关联 |
| 大量指标时间序列 | Parquet | 适合批量分析和版本化导出 |
| 模型配置、提示词、SQL schema | Git | 需要 diff 和审查 |
| 运行快照和复盘报告 | `05-runs/`、`06-reviews/` | 需要追加保存并可被人阅读 |

数据库只保存原始文件的路径、Drive file ID、内容 hash 和版本信息，不保存大体积文件本体。

源文件按“内容主题 → 文件类型”组织，再按来源和快照区分版本。`source_snapshot.storage_uri` 指向实际归档文件；目录分类不改变来源 ID。详见 [源文件整理规则](source-organization.md)。

## 事实、解释与判断

- 指标是观测值，不是观点。
- 证据是带出处的事实片段。
- 因子是多个证据经过解释后的状态。
- 情景是多个条件和因果关系的组合。
- 判断是某一次运行的有时间范围的输出。

这五层不能混写。例如“居民购房能力偏弱”属于因子状态，不属于原始指标；“房地产需求将持续下降”属于情景或判断，不属于因子。

## 数据版本规则

运行实现额外使用 `processing_package`、`source_provenance`、`evidence_review` 和 `metric_evidence` 保存导入批次、采集完整性、审核记录及指标到证据的关联。`verified` 表示原文提取已核对，因子和情景仍需人工审核；详见 [处理流程](processing-pipeline.md)。

- 原始文件内容发生变化时，新增 `source_snapshot`。
- 指标口径发生变化时，新增 `metric_definition` 版本。
- 因子定义、因果边或行为树规则发生变化时，更新模型版本，不覆盖旧运行。
- 运行快照必须记录当时使用的数据、模型和规则版本。
