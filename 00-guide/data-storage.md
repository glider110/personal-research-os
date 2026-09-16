# 数据目录

- `normalized/<主题>/<package-id>/package.json`：已校验的结构化处理结果包；大量时间序列后续可导出 Parquet。
- `runtime/`：本机 SQLite 数据库和运行缓存，不进入 Git，也不通过 Drive 多机并发同步。

数据库结构定义在 `90-system/01-db/schema.sql`。数据文件不应脱离 source snapshot 单独存在。
