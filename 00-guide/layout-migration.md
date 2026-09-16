# 编号目录迁移（2026-09-16）

本次迁移将资料、共享研究库、问题视图和系统实现分开，并为顶层文件夹编号。文件名和对象 ID 不因目录变化而重命名。

- 迁移前本机备份：`/tmp/research-os-before-layout-20260916-171649/workspace.tar.gz`。此临时备份不是长期备份方案。
- 同目录 `immutable.json` 记录 39 份输入/归档/索引/运行/复盘文件迁移前 SHA-256；迁移后逐一核对未变。
- 完整路径映射见 [legacy-paths.json](../90-system/05-config/legacy-paths.json)。数据库和旧 JSON 中冻结的旧路径由 CLI 解析到新位置，不改写其原始内容。
- 历史 Markdown 保留原字节，其内部旧路径不再作为导航入口；[历史阅读入口](../04-research/README.md)提供解析为当前路径的阅读副本。
- 新生成的共享库与研究问题 Markdown 可重新生成；不要直接编辑这些视图。
- 未提交变更一并保留并迁移，未执行 commit 或 push。

迁移核验：运行结果包 `validate`、重复 `import` 应返回 `already_imported`；执行 `library` 应读取并校验旧结果包、来源和运行快照，再生成共享视图。测试入口：`python3 -m unittest discover -s 90-system/04-tests -v`。

恢复时先保留迁移后的新增内容，再将备份解压到独立目录核对；不要直接覆盖当前工作区或使用 Git reset 丢弃未提交成果。
