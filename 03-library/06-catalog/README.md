# Catalog

这里保存来源、指标和证据的登记材料，作为结构化数据库之外的可读索引。

推荐命名：

```text
source-<topic>-<slug>.yaml
metric-<topic>-<slug>.yaml
evidence-<topic>-<date>-<slug>.yaml
```

正式运行后，Catalog 可以由 SQLite 导出生成，但不应与数据库维护两套冲突的事实。
