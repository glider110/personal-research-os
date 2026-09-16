# 共享研究库数据概览

先找对象，再查看它在哪些研究中被使用。主题不拥有数据，批次不切割知识。

| 入口 | 定义版本数 |
|---|---:|
| [来源](01-sources/sources.md) | 16 |
| [证据](02-evidence/evidence.md) | 12 |
| [指标](03-metrics/metrics.md) | 8 |
| [因子](04-factors/factors.md) | 4 |
| [因果假设](05-relations/hypotheses.md) | 2 |

[研究问题与待核验事项](../04-research/README.md)

修改结果应创建新版结果包，然后执行 `python3 90-system/03-scripts/research.py library` 刷新这些视图。

同名不自动合并；共同引用不等于独立验证。支持/反驳必须登记在 `05-relations/assertions/` 的版本化 JSON 文件中。
