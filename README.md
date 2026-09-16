# 个人研究库

**数据源 → 指标 → 核真、去重、交叉验证 → 候选因子。**

[房地产主题](04-research/real-estate.md) · [来源表](03-library/sources.md) · [指标表](03-library/metrics.md) · [因子表](03-library/factors.md)

```text
00-guide/       当前规范、来源整理规则
01-inbox/       待处理资料
02-sources/     原始文件：内容 → 类型
03-library/     sources.md · metrics.md · factors.md
04-research/    主题入口、待核对项
90-system/      工具、契约、结果包和历史存档
```

导入并刷新：

```bash
python3 90-system/scripts/research.py distill <package.json>
```

[数据蒸馏规范](00-guide/data-distillation.md) · [来源整理规则](00-guide/source-organization.md) · [系统说明](90-system/README.md)

数据更新使用新包 ID，原文与历史数据不覆盖。资料提取由 Agent 或人工完成；结果包和原始资料默认保存在本机，不随 Git 自动同步。
