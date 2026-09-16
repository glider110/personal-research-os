# 对象字段约定

## processing_package

Agent/NotebookLM 结果统一通过 `processing-package.schema.json` 定义的 JSON 包导入。来源文件单独保存，包内登记 hash、覆盖范围和处理工具；指标必须引用已核对证据，因子和因果边只作为研究草稿。流程见 [处理结果包规范](../../00-guide/processing-pipeline.md)。

## source

原始来源的逻辑身份。来源内容变化时不修改 `source`，新增 `source_snapshot`。

必填：`id`、`title`、`source_type`、`created_at`。

## metric

可复算指标的定义和观测值。定义包括单位、频率、区域、统计口径和方法；观测值必须引用 `source_snapshot`。

## evidence

可以被定位和引用的事实片段。必须带来源、定位信息、适用范围和审核状态。

## factor

具有独立机制的解释变量。定义描述边界和机制，状态记录某个时间点的方向、强度、置信度、证据和反转条件。

## run_snapshot

一次研究运行的完整冻结结果。必须记录数据版本、模型版本、行为树版本、情景、判断和行动。快照创建后只读。

## ID 规则

使用稳定、可读、跨机器不冲突的字符串 ID，例如：

```text
topic.real-estate
metric.real-estate.home-sales-area
factor.real-estate.household-purchasing-power
run.real-estate.2026-09-16.001
```
