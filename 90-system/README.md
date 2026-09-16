# 系统文件

日常研究请从 [共享库](../03-library/README.md) 和 [研究问题](../04-research/README.md) 进入。

| 目录 | 用途 |
|---|---|
| 01-db | SQLite 契约；历史批次表与全局共享对象层 |
| 02-schemas | JSON 结果包字段规范 |
| 03-scripts | 校验、导入、运行、复盘和阅读视图生成 |
| 04-tests | 来源、历史不可变、跨主题共享等行为测试 |
| 05-config | 项目配置与旧路径解析映射 |
| 06-prompts | Agent / NotebookLM 提示词 |
| 07-runtime | 本机 SQLite，不进入 Git |
| 08-examples | 后续示例 |

`shared_*` 表是由包和关系声明重建的查询层；包内对象的旧批次 ID 仍用于历史追溯，不当作全局身份。
