# Scripts

`research.py` 使用 Python 3.10+ 标准库，无额外依赖。它校验统一 JSON 结果包、自动初始化 SQLite、按主题和类型归档来源、写入证据与指标、冻结研究草稿并生成数据审计。

```bash
python3 90-system/03-scripts/research.py validate <package.json>
python3 90-system/03-scripts/research.py import <package.json>
python3 90-system/03-scripts/research.py run <package-id>
python3 90-system/03-scripts/research.py review <run-id>
python3 90-system/03-scripts/research.py status
```

`--root <目录>` 可指定隔离的输出根目录，放在子命令前。正常工作不需要指定。

重复导入相同包、重复运行和重复生成相同版本的数据审计保持幂等；同一包 ID 内容变化时报错，必须生成新版本。CLI 输出 JSON，失败以非零退出码及原因返回。输入来源、数据与模型哈希均写入快照。

`review` 目前只做数据与流程审计，不会自动评价市场预测准确率。浏览器采集、通用媒体解析、Parquet 导出尚未自动化。

脚本应保持幂等，并把输入来源、输出版本和失败原因写入日志。

共享阅读入口：`python3 90-system/03-scripts/research.py library`。从已导入包重建共享对象关系与 Markdown；指标、因子可填写 `shared_id` 实现跨主题稳定引用。
