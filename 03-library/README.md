# 共享研究库说明

本目录管理跨主题共享的来源、证据、指标、因子与关系。主题引用共享对象，批次记录处理过程；观测数值与评估状态不覆盖对象的历史版本。

## 说明与数据分开

- `README.md`：目录职责、使用方法和导航，人工维护。
- [overview.md](overview.md)：真实数据统计和阅读入口，自动生成。
- 各子目录的专用 Markdown：对象数据、使用记录和关系，自动生成。

| 目录 | 说明 | 数据 |
|---|---|---|
| 01-sources | [来源说明](01-sources/README.md) | [来源数据](01-sources/sources.md) |
| 02-evidence | [证据说明](02-evidence/README.md) | [证据数据](02-evidence/evidence.md) |
| 03-metrics | [指标说明](03-metrics/README.md) | [指标数据](03-metrics/metrics.md) |
| 04-factors | [因子说明](04-factors/README.md) | [因子数据](04-factors/factors.md) |
| 05-relations | [关系说明](05-relations/README.md) | [因果假设与关系](05-relations/hypotheses.md) |
| 06-catalog | 导入索引 | imports 下的 JSON |
| 07-models | 版本化模型定义 | YAML 模型文件 |
| 08-packages | 不可覆盖的规范化结果包 | package.json，默认仅在本机保存 |

## 更新方法

修改研究数据应生成新版结果包，校验并导入后执行：

```bash
python3 90-system/03-scripts/research.py library
```

命令刷新数据页和研究视图，不覆盖本目录及子目录的 README 说明。Markdown 是结构化数据的阅读视图，不是需要手动同步的另一份数据源。

同名不自动合并；共同引用不等于独立验证。支持/反驳需按 [关系声明规则](05-relations/assertions/README.md) 登记。

[研究问题与待核验事项](../04-research/README.md) · [返回项目总入口](../README.md)
