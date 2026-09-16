# NotebookLM「立党专题」首轮运行

## 已执行

2026-09-16 从用户指定的 NotebookLM 笔记本读取可见历史讨论、12 个来源面板和现有因子报告。使用 Chrome 已有登录态只读采集；未新增问题、修改来源或修改笔记本。

将这些内容与独立获取的 2 份国家统计局发布稿组成处理结果包，执行了校验、归档、SQLite 入库、研究草稿快照和数据审计。

| 对象 | 数量 |
|---|---:|
| 来源快照 | 16 |
| 原文核对的证据 | 8 |
| 待核验说法 | 4 |
| 指标观测值 | 16 |
| 因子草稿 | 4 |
| 因果假设 | 2 |
| 条件性情景 | 3 |
| 研究运行 / 数据审计 | 1 / 1 |

## 阅读入口

- [首轮研究报告（当前路径阅读副本）](../04-research/02-history/run.real-estate.2026-09-16.da171d2e.3c536216.583bdde0.md)
- [不可覆盖的运行 JSON](../05-runs/run.real-estate.2026-09-16.da171d2e.3c536216.583bdde0.json)
- [数据与流程复盘](../06-reviews/review.run.real-estate.2026-09-16.da171d2e.3c536216.583bdde0.data-audit-v1.md)
- [来源索引](../03-library/06-catalog/imports/package.lidang.2026-09-16.v1.json)
- [本机输入包](../01-inbox/notebooklm-lidang-2026-09-16-v1/package.json)
- [本机规范化结果包](../03-library/08-packages/real-estate/package.lidang.2026-09-16.v1/package.json)

## 重复执行

```bash
python3 90-system/03-scripts/research.py validate 01-inbox/notebooklm-lidang-2026-09-16-v1/package.json
python3 90-system/03-scripts/research.py import 01-inbox/notebooklm-lidang-2026-09-16-v1/package.json
python3 90-system/03-scripts/research.py run package.lidang.2026-09-16.v1
python3 90-system/03-scripts/research.py review run.real-estate.2026-09-16.da171d2e.3c536216.583bdde0
python3 90-system/03-scripts/research.py status
```

同一版本重复执行不会增加重复记录。修改处理结果必须使用新的 package ID；修改代码、schema、SQL 或模型会形成新的运行版本。新机器需要另行同步本机输入包和原始来源；SQLite 可从包重建。

## 这轮确认了什么

核对了2021年前11月与全年新开工、施工、土地购置、资金来源和销售面积的累计口径。新开工下降与施工面积增长可以同时成立，不能混为一个指标；总到位资金增长与国内贷款下降也可以同时成立，不能直接描述为“所有资金都断了”。

原始发布稿：[国家统计局前11月数据](https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1901307.html)、[全年数据](https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1901340.html)。正文由 Jina Reader 提取，保存的是发布稿文本而非原始 HTML 或配图二进制。

## 明确未完成的部分

- NotebookLM 来源与讨论仅保证可见文本已采集，14 份页面采集全部保守标为 partial；视频只含可见转录片段，未下载原视频。
- 讨论里的单月 -31.2%、2023—2025年土地面积估算、房价收入比区间、城镇化瓶颈尚未独立核验。
- 原有脚注未全部映射为原件页码/时间戳；两个同名框架来源未合并。
- 运行状态是待人工审核，不能当作已发布投资结论；2021年历史数据不能代表2026年现状。
- 复盘是来源与流程审计，未来市场结果未验证，没有生成预测胜率。

首轮自动检查覆盖来源 hash、证据摘录、数值转换、引用关系、发布时间门禁、幂等导入、篡改检测和数据库快照保护。
