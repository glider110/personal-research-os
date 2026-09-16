# 共享因果假设数据

由结果包生成；不要手工修改。跨主题引用同一对象，评估状态和数值保留在各次使用记录中。

[目录说明](README.md) · [数据概览](../overview.md)

## 数据总表

| 因果假设 | 作用方向 | 机制 | 时滞 | 反证条件 | 审核状态 |
| --- | --- | --- | --- | --- | --- |
| [新开工计划](hypotheses.md#revision.eb152fd5cc1df108b103bb4399f485c0061fd9ffbe0f493aff3f59105130300e) | positive | 在销售预期和政策条件相近时，融资可得性改善可能支持新开工，融资约束可能使项目延后；同期相关性尚未识别因果。 | 数月至数季，尚未估计 | 融资改善后新开工仍持续下降，且其他条件相近，需检验需求与库存是否为主导。 | 待验证假设 |
| [未来新房价格](hypotheses.md#revision.6220b987a68db425359a14b74642f9dc64985cd9a65c9ac8de38b749deebed30) | conditional | 需求不变且存量供给有限时，新增供给下降可能支撑价格；若需求下降更快或二手房供给增加，价格仍可能承压。 | 从开工到可售或交付存在地区差异 | 同城供给收缩而需求稳定，价格仍下降时需检查库存、质量和政策。 | 待验证假设 |

<a id="revision.eb152fd5cc1df108b103bb4399f485c0061fd9ffbe0f493aff3f59105130300e"></a>
## 新开工计划

| 字段 | 内容 |
|---|---|
| 反证条件 | 融资改善后新开工仍持续下降，且其他条件相近，需检验需求与库存是否为主导。 |
| 时滞 | 数月至数季，尚未估计 |
| 机制 | 在销售预期和政策条件相近时，融资可得性改善可能支持新开工，融资约束可能使项目延后；同期相关性尚未识别因果。 |
| 影响结果 | 新开工计划 |
| 适用范围 | 全国房地产开发企业；需按企业与城市验证 |
| 作用方向 | positive |

<details>
<summary>追溯标识</summary>

| 标识 | 值 |
|---|---|
| 共享 ID | `shared.hypothesis.24a26dc0c2f94c12780e44d452f8d0fb745a66b5cd14e59c7f25997f577ae1f9` |
| 定义版本 | `revision.eb152fd5cc1df108b103bb4399f485c0061fd9ffbe0f493aff3f59105130300e` |
| 起点因子版本 | `revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d` |

</details>

### 使用与评估

| 研究 | 来源批次 | 本次记录 |
|---|---|---|
| [中国房地产](../../04-research/real-estate.md) | [package.lidang.2026-09-16.v1](../08-packages/real-estate/package.lidang.2026-09-16.v1/package.json) | hypothesis |

### 关联与交叉核验

| 起点 | 关系 | 终点 | 状态 | 解释 |
|---|---|---|---|---|
| [新开工计划](hypotheses.md#revision.eb152fd5cc1df108b103bb4399f485c0061fd9ffbe0f493aff3f59105130300e) | 引用证据 | [2021年1—12月总到位资金累计增长与国内贷款累计下降并存。](../02-evidence/evidence.md#revision.0c6a06c0e9ba45ba0f971a3eb9b26311278676d47dff28280ced127440dbd71d) | reference | 结构引用；不自动证明支持或因果成立 |
| [新开工计划](hypotheses.md#revision.eb152fd5cc1df108b103bb4399f485c0061fd9ffbe0f493aff3f59105130300e) | 引用证据 | [2021年1—12月房屋新开工、施工为不同口径，不能混用。](../02-evidence/evidence.md#revision.b04c2a48cad309fed41012c9460752e581932f35cc33ecdabc57a16165dc0288) | reference | 结构引用；不自动证明支持或因果成立 |

<a id="revision.6220b987a68db425359a14b74642f9dc64985cd9a65c9ac8de38b749deebed30"></a>
## 未来新房价格

| 字段 | 内容 |
|---|---|
| 反证条件 | 同城供给收缩而需求稳定，价格仍下降时需检查库存、质量和政策。 |
| 时滞 | 从开工到可售或交付存在地区差异 |
| 机制 | 需求不变且存量供给有限时，新增供给下降可能支撑价格；若需求下降更快或二手房供给增加，价格仍可能承压。 |
| 影响结果 | 未来新房价格 |
| 适用范围 | 城市级新房和二手房市场，不可直接外推全国所有住房 |
| 作用方向 | conditional |

<details>
<summary>追溯标识</summary>

| 标识 | 值 |
|---|---|
| 共享 ID | `shared.hypothesis.94b5a16a5f02a01a39ee2cca06b2abc8c22dd470314493db3d9d944a94d0780a` |
| 定义版本 | `revision.6220b987a68db425359a14b74642f9dc64985cd9a65c9ac8de38b749deebed30` |
| 起点因子版本 | `revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce` |

</details>

### 使用与评估

| 研究 | 来源批次 | 本次记录 |
|---|---|---|
| [中国房地产](../../04-research/real-estate.md) | [package.lidang.2026-09-16.v1](../08-packages/real-estate/package.lidang.2026-09-16.v1/package.json) | hypothesis |

### 关联与交叉核验

| 起点 | 关系 | 终点 | 状态 | 解释 |
|---|---|---|---|---|
| [未来新房价格](hypotheses.md#revision.6220b987a68db425359a14b74642f9dc64985cd9a65c9ac8de38b749deebed30) | 引用证据 | [2021年1—12月房屋新开工、施工为不同口径，不能混用。](../02-evidence/evidence.md#revision.b04c2a48cad309fed41012c9460752e581932f35cc33ecdabc57a16165dc0288) | reference | 结构引用；不自动证明支持或因果成立 |
| [未来新房价格](hypotheses.md#revision.6220b987a68db425359a14b74642f9dc64985cd9a65c9ac8de38b749deebed30) | 引用证据 | [2021年1—12月商品房销售面积累计同比为正，不能据此断言每个月均增长。](../02-evidence/evidence.md#revision.443ce3d136e8da517635dbb803989f9365c7bacb700765821538fd15b69ec109) | reference | 结构引用；不自动证明支持或因果成立 |
