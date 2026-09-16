# 共享因子数据

由结果包生成；不要手工修改。跨主题引用同一对象，评估状态和数值保留在各次使用记录中。

[目录说明](README.md) · [数据概览](../overview.md)

## 数据总表

| 因子 | 评估日期 | 方向 | 置信度 | 研究 | 审核状态 |
| --- | --- | --- | --- | --- | --- |
| [房企融资与现金流结构](factors.md#revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d) | 2026-09-16 | 2021年银行贷款来源收缩；整体流动性因企业而异 | medium | 中国房地产 | 待人工审核 |
| [购买力与估值约束](factors.md#revision.c9921f0e6e4c64e83267ac2c556bb3c477fce797e2fe0369ee33508e2bc3ef42) | 2026-09-16 | 无法据现有证据定量判断 | low | 中国房地产 | 待人工审核 |
| [销售需求与城市分化](factors.md#revision.7d4fa1478f7ba7c60cea37eb66798ce08a8d6003acc7e6e586e37963f8dc59e6) | 2026-09-16 | 待补充数据 | low | 中国房地产 | 待人工审核 |
| [开发投资意愿与未来供给](factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce) | 2026-09-16 | 2021年新增开发活动收缩 | medium | 中国房地产 | 待人工审核 |

<a id="revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d"></a>
## 房企融资与现金流结构

| 字段 | 内容 |
|---|---|
| 机制 | 国内贷款累计下降、总到位资金仍增长，提示资金来源结构变化。它支持融资约束假设，但不能单凭全国汇总值证明所有房企资金链断裂。 |
| 名称 | 房企融资与现金流结构 |
| 适用范围 | 中国，全国口径优先，必要时区分城市层级 |

<details>
<summary>追溯标识</summary>

| 标识 | 值 |
|---|---|
| 共享 ID | `shared.factor.1713eac54f260d7524efa7f1591f5f2f78f59d5d3e6c2779cdafc7b6cf40efec` |
| 定义版本 | `revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d` |

</details>

### 使用与评估

| 研究 | 来源批次 | 本次记录 |
|---|---|---|
| [中国房地产](../../04-research/real-estate.md) | [package.lidang.2026-09-16.v1](../08-packages/real-estate/package.lidang.2026-09-16.v1/package.json) | 2026-09-16：2021年银行贷款来源收缩；整体流动性因企业而异 / medium（待人工审核） |

### 关联与交叉核验

| 起点 | 关系 | 终点 | 状态 | 解释 |
|---|---|---|---|---|
| [房企融资与现金流结构](factors.md#revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d) | 引用指标 | [房企到位资金：国内贷款累计同比](../03-metrics/metrics.md#revision.3ec573e2ee9d723d183afb11f99bd12bbd424b51bc23fd17af29c88d28c99e0e) | reference | 结构引用；不自动证明支持或因果成立 |
| [房企融资与现金流结构](factors.md#revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d) | 引用证据 | [2021年1—12月总到位资金累计增长与国内贷款累计下降并存。](../02-evidence/evidence.md#revision.0c6a06c0e9ba45ba0f971a3eb9b26311278676d47dff28280ced127440dbd71d) | reference | 结构引用；不自动证明支持或因果成立 |
| [房企融资与现金流结构](factors.md#revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d) | 引用指标 | [房企总到位资金累计同比](../03-metrics/metrics.md#revision.eb96c07c4b328ebfd5faa71fb519cbead03d5f7336aa0c8026d92604e5d2c9a6) | reference | 结构引用；不自动证明支持或因果成立 |
| [房企融资与现金流结构](factors.md#revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d) | 引用证据 | [2021年1—11月总到位资金累计增长与国内贷款累计下降并存。](../02-evidence/evidence.md#revision.d5ec098e1e995025dd3c7f9d4bb3981892f6ded0567eab43e2b21bf827217d55) | reference | 结构引用；不自动证明支持或因果成立 |

<a id="revision.c9921f0e6e4c64e83267ac2c556bb3c477fce797e2fe0369ee33508e2bc3ef42"></a>
## 购买力与估值约束

| 字段 | 内容 |
|---|---|
| 机制 | 房价相对收入、租金和融资成本会影响支付能力；目前讨论中的估值阈值和城镇化瓶颈没有独立核验。 |
| 名称 | 购买力与估值约束 |
| 适用范围 | 中国，全国口径优先，必要时区分城市层级 |

<details>
<summary>追溯标识</summary>

| 标识 | 值 |
|---|---|
| 共享 ID | `shared.factor.5f8e83cba320ad62ab039112161a4acbe67959e3a9202c6a0b560ce719c8a479` |
| 定义版本 | `revision.c9921f0e6e4c64e83267ac2c556bb3c477fce797e2fe0369ee33508e2bc3ef42` |

</details>

### 使用与评估

| 研究 | 来源批次 | 本次记录 |
|---|---|---|
| [中国房地产](../../04-research/real-estate.md) | [package.lidang.2026-09-16.v1](../08-packages/real-estate/package.lidang.2026-09-16.v1/package.json) | 2026-09-16：无法据现有证据定量判断 / low（待人工审核） |

### 关联与交叉核验

| 起点 | 关系 | 终点 | 状态 | 解释 |
|---|---|---|---|---|
| [购买力与估值约束](factors.md#revision.c9921f0e6e4c64e83267ac2c556bb3c477fce797e2fe0369ee33508e2bc3ef42) | 引用证据 | [城镇化率与住房需求之间的关系需核对年份与人口口径，不能用整数阈值断言需求结束。](../02-evidence/evidence.md#revision.e58489e4d836f8ae4c30059e8c771eda04cc98caf9ee9b5517e2d0e6fd2a75cd) | reference | 结构引用；不自动证明支持或因果成立 |
| [购买力与估值约束](factors.md#revision.c9921f0e6e4c64e83267ac2c556bb3c477fce797e2fe0369ee33508e2bc3ef42) | 引用证据 | [房价收入比及合理区间缺少城市、样本、时间与收入定义，不能直接当买卖阈值。](../02-evidence/evidence.md#revision.7d85a69238f58f9fe3268358bb90fea65a81b706cef0cb1ca5223f6470e0e61c) | reference | 结构引用；不自动证明支持或因果成立 |

<a id="revision.7d4fa1478f7ba7c60cea37eb66798ce08a8d6003acc7e6e586e37963f8dc59e6"></a>
## 销售需求与城市分化

| 字段 | 内容 |
|---|---|
| 机制 | 全年销售面积累计增长不排除下半年走弱。当前缺少月度、城市、二手房成交与库存数据，不能确认需求比供给下降更快。 |
| 名称 | 销售需求与城市分化 |
| 适用范围 | 中国，全国口径优先，必要时区分城市层级 |

<details>
<summary>追溯标识</summary>

| 标识 | 值 |
|---|---|
| 共享 ID | `shared.factor.93ff8d389d14ac1ec172c32d0b70e940dff1cb264ffe059707511293a6045a79` |
| 定义版本 | `revision.7d4fa1478f7ba7c60cea37eb66798ce08a8d6003acc7e6e586e37963f8dc59e6` |

</details>

### 使用与评估

| 研究 | 来源批次 | 本次记录 |
|---|---|---|
| [中国房地产](../../04-research/real-estate.md) | [package.lidang.2026-09-16.v1](../08-packages/real-estate/package.lidang.2026-09-16.v1/package.json) | 2026-09-16：待补充数据 / low（待人工审核） |

### 关联与交叉核验

| 起点 | 关系 | 终点 | 状态 | 解释 |
|---|---|---|---|---|
| [销售需求与城市分化](factors.md#revision.7d4fa1478f7ba7c60cea37eb66798ce08a8d6003acc7e6e586e37963f8dc59e6) | 引用证据 | [2021年1—11月商品房销售面积累计同比为正，不能据此断言每个月均增长。](../02-evidence/evidence.md#revision.c58a95f66b0c36c76af6e7db027762224402d4112e40323edfe72a8d922942f7) | reference | 结构引用；不自动证明支持或因果成立 |
| [销售需求与城市分化](factors.md#revision.7d4fa1478f7ba7c60cea37eb66798ce08a8d6003acc7e6e586e37963f8dc59e6) | 引用证据 | [2021年1—12月商品房销售面积累计同比为正，不能据此断言每个月均增长。](../02-evidence/evidence.md#revision.443ce3d136e8da517635dbb803989f9365c7bacb700765821538fd15b69ec109) | reference | 结构引用；不自动证明支持或因果成立 |
| [销售需求与城市分化](factors.md#revision.7d4fa1478f7ba7c60cea37eb66798ce08a8d6003acc7e6e586e37963f8dc59e6) | 引用指标 | [商品房销售面积累计同比](../03-metrics/metrics.md#revision.59118f6e59ca46779fa44648097aa0e89b519eedb76fb88b4faddd8f89c0b01f) | reference | 结构引用；不自动证明支持或因果成立 |

<a id="revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce"></a>
## 开发投资意愿与未来供给

| 字段 | 内容 |
|---|---|
| 机制 | 新开工和拿地均收缩，与融资和预期有关；二者不当作独立投票。新开工是未来供给流量，施工面积还包含往期开工项目。 |
| 名称 | 开发投资意愿与未来供给 |
| 适用范围 | 中国，全国口径优先，必要时区分城市层级 |

<details>
<summary>追溯标识</summary>

| 标识 | 值 |
|---|---|
| 共享 ID | `shared.factor.f0df50585fded35972490eb3d2a70319c16b8c218e9a57c8274d1360cd0fb90f` |
| 定义版本 | `revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce` |

</details>

### 使用与评估

| 研究 | 来源批次 | 本次记录 |
|---|---|---|
| [中国房地产](../../04-research/real-estate.md) | [package.lidang.2026-09-16.v1](../08-packages/real-estate/package.lidang.2026-09-16.v1/package.json) | 2026-09-16：2021年新增开发活动收缩 / medium（待人工审核） |

### 关联与交叉核验

| 起点 | 关系 | 终点 | 状态 | 解释 |
|---|---|---|---|---|
| [开发投资意愿与未来供给](factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce) | 引用指标 | [土地购置面积累计同比](../03-metrics/metrics.md#revision.bd186657b823ff5916de31680b24bae812ee585c31d2eddaafaa45277740e040) | reference | 结构引用；不自动证明支持或因果成立 |
| [开发投资意愿与未来供给](factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce) | 引用证据 | [2021年1—11月房屋新开工、施工为不同口径，不能混用。](../02-evidence/evidence.md#revision.47c38b832ae9fed02d73c7277d0efdfa38aa2e397cbe7b0d08211bd003789d34) | reference | 结构引用；不自动证明支持或因果成立 |
| [开发投资意愿与未来供给](factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce) | 引用证据 | [2021年1—12月房屋新开工、施工为不同口径，不能混用。](../02-evidence/evidence.md#revision.b04c2a48cad309fed41012c9460752e581932f35cc33ecdabc57a16165dc0288) | reference | 结构引用；不自动证明支持或因果成立 |
| [开发投资意愿与未来供给](factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce) | 引用证据 | [2021年1—12月全国房企土地购置面积累计同比下降。](../02-evidence/evidence.md#revision.ef32bf0391b5fd4f35876d9db38e698c73faff12e1008421864bae67a783403f) | reference | 结构引用；不自动证明支持或因果成立 |
| [开发投资意愿与未来供给](factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce) | 引用指标 | [房屋施工面积累计同比](../03-metrics/metrics.md#revision.5a95bc691be8e41386bcf3be8369448da9fea6f0499a1ee38fa83025ff269fad) | reference | 结构引用；不自动证明支持或因果成立 |
| [开发投资意愿与未来供给](factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce) | 引用指标 | [房屋新开工面积累计同比](../03-metrics/metrics.md#revision.f13676c2a73e532cc6e6ee66343ad726a0201feebf0067b6f3ba69d1fcf064e7) | reference | 结构引用；不自动证明支持或因果成立 |
| [开发投资意愿与未来供给](factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce) | 引用证据 | [2021年1—11月全国房企土地购置面积累计同比下降。](../02-evidence/evidence.md#revision.4b025237d64073729f907367646c179a4043991e55f4c4c8a71551a0b2d2718c) | reference | 结构引用；不自动证明支持或因果成立 |
