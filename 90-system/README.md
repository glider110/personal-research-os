# 系统文件

日常只看 [主题](../04-research/README.md) 和 [指标](../03-library/metrics.md)。

| 目录 / 文件 | 用途 |
|---|---|
| scripts/ | 校验、导入、生成三层阅读表 |
| schemas/ | 数据蒸馏包 2.0 契约 |
| tests/ | 数据真实性、去重、追溯与导入测试 |
| db/、runtime/ | 数据库结构与本机索引 |
| catalog/、packages/ | 导入索引与不可覆盖的结果包 |
| evidence.md | 原文核对记录 |
| config/ | 旧数据路径映射 |
| prompts/ | 资料提取约定 |
| history/ | 原始历史快照与复盘，仅存档 |

```bash
python3 90-system/scripts/research.py distill <package.json>
python3 90-system/scripts/research.py library
python3 -m unittest discover -s 90-system/tests -q
```

只依赖 Python 3.10+ 标准库。validate/import 可分步使用，status 查看记录数量。已移除 run/review 命令及因果执行器；新导入只接受 2.0 包，已导入旧包继续用于数据追溯。

历史文件原样保留，内部旧路径以 `config/legacy-paths.json` 解析；不另生成历史阅读副本。JSON 是正式结果，SQLite 是索引，Markdown 是阅读视图，不要手改生成表。
