# 数据目录

- `normalized/`：清洗后的指标时间序列，默认使用 Parquet。
- `runtime/`：本机 SQLite 数据库和运行缓存，不进入 Git，也不通过 Drive 多机并发同步。

数据库结构定义在 `db/schema.sql`。数据文件不应脱离 source snapshot 单独存在。
