# 中国房地产

[共享研究库](../03-library/README.md) · [待核验](01-pending.md)

## 核对讨论中2021年房地产收缩的指标口径，并解释为何新开工减少不必然意味着房价上涨。

追溯批次：`package.lidang.2026-09-16.v1`；截止日：2026-09-16；分析待人工审核。

### 引用对象

- 证据：[2023—2025年土地面积仅为讨论中的行业估算，不录入正式时间序列。](../03-library/02-evidence/evidence.md#revision.c33f86243071e6229eab5801cf11fbed5de074befc7ed02ecfe030367079b87d)
- 证据：[2021年12月单月新开工同比 -31.2%：需同口径前期原始值复算。](../03-library/02-evidence/evidence.md#revision.7458a192b2dd8bf14ef90e9f03ed573b80433f64e077aa5048df0b36a7dff144)
- 证据：[城镇化率与住房需求之间的关系需核对年份与人口口径，不能用整数阈值断言需求结束。](../03-library/02-evidence/evidence.md#revision.e58489e4d836f8ae4c30059e8c771eda04cc98caf9ee9b5517e2d0e6fd2a75cd)
- 证据：[房价收入比及合理区间缺少城市、样本、时间与收入定义，不能直接当买卖阈值。](../03-library/02-evidence/evidence.md#revision.7d85a69238f58f9fe3268358bb90fea65a81b706cef0cb1ca5223f6470e0e61c)
- 证据：[2021年1—11月房屋新开工、施工为不同口径，不能混用。](../03-library/02-evidence/evidence.md#revision.47c38b832ae9fed02d73c7277d0efdfa38aa2e397cbe7b0d08211bd003789d34)
- 证据：[2021年1—11月总到位资金累计增长与国内贷款累计下降并存。](../03-library/02-evidence/evidence.md#revision.d5ec098e1e995025dd3c7f9d4bb3981892f6ded0567eab43e2b21bf827217d55)
- 证据：[2021年1—11月全国房企土地购置面积累计同比下降。](../03-library/02-evidence/evidence.md#revision.4b025237d64073729f907367646c179a4043991e55f4c4c8a71551a0b2d2718c)
- 证据：[2021年1—11月商品房销售面积累计同比为正，不能据此断言每个月均增长。](../03-library/02-evidence/evidence.md#revision.c58a95f66b0c36c76af6e7db027762224402d4112e40323edfe72a8d922942f7)
- 证据：[2021年1—12月房屋新开工、施工为不同口径，不能混用。](../03-library/02-evidence/evidence.md#revision.b04c2a48cad309fed41012c9460752e581932f35cc33ecdabc57a16165dc0288)
- 证据：[2021年1—12月总到位资金累计增长与国内贷款累计下降并存。](../03-library/02-evidence/evidence.md#revision.0c6a06c0e9ba45ba0f971a3eb9b26311278676d47dff28280ced127440dbd71d)
- 证据：[2021年1—12月全国房企土地购置面积累计同比下降。](../03-library/02-evidence/evidence.md#revision.ef32bf0391b5fd4f35876d9db38e698c73faff12e1008421864bae67a783403f)
- 证据：[2021年1—12月商品房销售面积累计同比为正，不能据此断言每个月均增长。](../03-library/02-evidence/evidence.md#revision.443ce3d136e8da517635dbb803989f9365c7bacb700765821538fd15b69ec109)
- 因子：[销售需求与城市分化](../03-library/04-factors/factors.md#revision.7d4fa1478f7ba7c60cea37eb66798ce08a8d6003acc7e6e586e37963f8dc59e6)
- 因子：[开发投资意愿与未来供给](../03-library/04-factors/factors.md#revision.e1bc37e41af3ec2b015f7917f8c1d20b78b484055235c6cc811ff290d04603ce)
- 因子：[房企融资与现金流结构](../03-library/04-factors/factors.md#revision.f756f07e3f980e727e75d1b984ac7f4c7bd1d04bb52a2d50c049ee317b7bed3d)
- 因子：[购买力与估值约束](../03-library/04-factors/factors.md#revision.c9921f0e6e4c64e83267ac2c556bb3c477fce797e2fe0369ee33508e2bc3ef42)
- 因果假设：[新开工计划](../03-library/05-relations/hypotheses.md#revision.eb152fd5cc1df108b103bb4399f485c0061fd9ffbe0f493aff3f59105130300e)
- 因果假设：[未来新房价格](../03-library/05-relations/hypotheses.md#revision.6220b987a68db425359a14b74642f9dc64985cd9a65c9ac8de38b749deebed30)
- 指标：[房屋施工面积累计同比](../03-library/03-metrics/metrics.md#revision.5a95bc691be8e41386bcf3be8369448da9fea6f0499a1ee38fa83025ff269fad)
- 指标：[房企总到位资金累计同比](../03-library/03-metrics/metrics.md#revision.eb96c07c4b328ebfd5faa71fb519cbead03d5f7336aa0c8026d92604e5d2c9a6)
- 指标：[土地购置面积（累计）](../03-library/03-metrics/metrics.md#revision.c54e3fcb3abc3fbf225e2c7b4cd2edfd0542d6d47b3b2fe27a2ad68e8a218507)
- 指标：[土地购置面积累计同比](../03-library/03-metrics/metrics.md#revision.bd186657b823ff5916de31680b24bae812ee585c31d2eddaafaa45277740e040)
- 指标：[房企到位资金：国内贷款累计同比](../03-library/03-metrics/metrics.md#revision.3ec573e2ee9d723d183afb11f99bd12bbd424b51bc23fd17af29c88d28c99e0e)
- 指标：[商品房销售面积累计同比](../03-library/03-metrics/metrics.md#revision.59118f6e59ca46779fa44648097aa0e89b519eedb76fb88b4faddd8f89c0b01f)
- 指标：[房屋新开工面积（累计）](../03-library/03-metrics/metrics.md#revision.84d60236b3feca78b96b3a1c3ffd2483a7a0d0c2601fce2e565b197ba2a0ad73)
- 指标：[房屋新开工面积累计同比](../03-library/03-metrics/metrics.md#revision.f13676c2a73e532cc6e6ee66343ad726a0201feebf0067b6f3ba69d1fcf064e7)
- 指标：[房屋施工面积累计同比](../03-library/03-metrics/metrics.md#revision.5a95bc691be8e41386bcf3be8369448da9fea6f0499a1ee38fa83025ff269fad)
- 指标：[房企总到位资金累计同比](../03-library/03-metrics/metrics.md#revision.eb96c07c4b328ebfd5faa71fb519cbead03d5f7336aa0c8026d92604e5d2c9a6)
- 指标：[土地购置面积（累计）](../03-library/03-metrics/metrics.md#revision.c54e3fcb3abc3fbf225e2c7b4cd2edfd0542d6d47b3b2fe27a2ad68e8a218507)
- 指标：[土地购置面积累计同比](../03-library/03-metrics/metrics.md#revision.bd186657b823ff5916de31680b24bae812ee585c31d2eddaafaa45277740e040)
- 指标：[房企到位资金：国内贷款累计同比](../03-library/03-metrics/metrics.md#revision.3ec573e2ee9d723d183afb11f99bd12bbd424b51bc23fd17af29c88d28c99e0e)
- 指标：[商品房销售面积累计同比](../03-library/03-metrics/metrics.md#revision.59118f6e59ca46779fa44648097aa0e89b519eedb76fb88b4faddd8f89c0b01f)
- 指标：[房屋新开工面积（累计）](../03-library/03-metrics/metrics.md#revision.84d60236b3feca78b96b3a1c3ffd2483a7a0d0c2601fce2e565b197ba2a0ad73)
- 指标：[房屋新开工面积累计同比](../03-library/03-metrics/metrics.md#revision.f13676c2a73e532cc6e6ee66343ad726a0201feebf0067b6f3ba69d1fcf064e7)
- 来源：[立党专题：当前页面可见历史讨论](../03-library/01-sources/sources.md#revision.15930690dedcef01d75d29f7789719e408a8dde8fe19747c45e3f889c2ae8ce6)
- 来源：[中国房地产关键因子整理与分析指南（NotebookLM 草稿）](../03-library/01-sources/sources.md#revision.c2cdb279846e583f7013c1051e22bd11cf55ea73066805ccd97a1a3cb085f9de)
- 来源：[房地产市场深度探讨](../03-library/01-sources/sources.md#revision.7c762abd516e25d8eb10c228494f9ffbfaa48d3505e4a4473bacc8587748d420)
- 来源：[2021年1—11月份全国房地产开发投资增长6.0%](../03-library/01-sources/sources.md#revision.b47994da31c3ec2d907a22cc10941090334568c4c83082b82ba9c06ae36434f3)
- 来源：[2027年中国房地产终极大预测，中国房地产马上反弹还是继续阴跌？县城房地产还有救吗？房产税是否会马上征收？](../03-library/01-sources/sources.md#revision.485661256ba1ccc82e0c9452425511bf4bd24297e425446cc636710907947d7f)
- 来源：[个人投资因果决策框架.md](../03-library/01-sources/sources.md#revision.ae49a3101d9605caed34a06c1ecbb8848fad27c8b1ae03a60d649c3f7b1201e4)
- 来源：[个人投资因果决策框架.md](../03-library/01-sources/sources.md#revision.7c7e1dfead530171be7bab297132bfc4fcef5fff54bd822e67cf62d591deb281)
- 来源：[克而瑞：2021年中国房地产总结与展望](../03-library/01-sources/sources.md#revision.bbc43d11eacbe15bf2c23e7f25dbc882a77ba795223b1b6f31fa4a401be77579)
- 来源：[立党：日本衰退30年，中国步其后尘？](../03-library/01-sources/sources.md#revision.a8d0df7f6c0c91890f4bdaed5506f79a5cdf7fd2c67049a130a11e2fb34873eb)
- 来源：[立党：中国未来30年房地产深度分析及预测](../03-library/01-sources/sources.md#revision.c15687367197687891c7de7d1e0468ad19f4bb505a3dad264e340f4af96539ed)
- 来源：[立党讲座系列03：中国房地产崩盘，到底会持续多久，什么时候才能跌到底？](../03-library/01-sources/sources.md#revision.87b83623ea5a9fb0edadfbe03b45e438e0ad73e58231bdc2b8c12b988a8fb93d)
- 来源：[全国房地产开发经营数据解读（2021年1-12月）](../03-library/01-sources/sources.md#revision.ee3db2e02b3554064bda13e646422bc9f1e041282038602095fe7f3bb4a5cf23)
- 来源：[中国房地产拐点指标与价格走势逻辑深度总结](../03-library/01-sources/sources.md#revision.559173b7b152fc8e897d588e17fa5f8034515b1cc4a0c1464bb73ccbff53db4e)
- 来源：[Research report: 2021年房地产开工数据核验与查询渠道](../03-library/01-sources/sources.md#revision.fcd9149ac76b33b127e66acd1f5627f2f73cc2c27bca6f6cc002a48bbdc12b95)
- 来源：[国家统计局：2021年1—11月房地产开发与销售](../03-library/01-sources/sources.md#revision.5e790c609580aef44705562b0aa308d00b41467f3cbc3526154c5da62f3ec929)
- 来源：[国家统计局：2021年1—12月房地产开发与销售](../03-library/01-sources/sources.md#revision.75d8581a2c668da3a783e117fd80a9e413bfa661a036ea771d15548f7ee7d8fc)

### 条件性情景（本研究草稿）

- **基准假设：融资约束与需求偏弱并存**：条件：融资恢复有限；销售需求未显著改善；这一前提尚未被本轮数据确认。反证：融资与销售同步持续改善
- **向好假设：需求恢复、供给收缩支撑局部市场**：条件：政策与融资传导有效；人口流入城市需求恢复且库存可控。反证：销量改善不能持续或库存继续累积
- **压力假设：现金流与购房信心相互拖累**：条件：销售回款继续弱化；交付与偿债压力升高并影响信心。反证：交付、回款与信用条件稳定改善

### 审核缺口

- 本轮为2026年对2021年资料的历史重建，不是2021年真实预测，也不是无前视偏差回测。
- 2021年全年统计于2022年1月17日发布，不能用于声称在2021年12月31日已知全年结果。
- 视频仅保存NotebookLM可见转录片段，未下载原视频；页面采集也不保证包含未加载内容。
- NotebookLM原有引用编号只在对应消息中有意义，未全部解析成原文件页码/时间戳。
- 两个同名框架来源保留独立登记，尚未确认是否为同一版本，不能重复计权。
- -31.2%单月新开工降幅尚未独立复算；累计同比不能直接相减。
- 2023—2025年土地面积行业估算、房价收入比阈值和70%城镇化瓶颈均待核验。
- 因果机制与情景为本地Agent整理的假设，当前缺少城市量价、库存、家庭收入和企业现金流证据。
- 历史2021年指标不能用于直接发布2026年市场方向。
