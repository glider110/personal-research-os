# 立党专题：首轮研究快照

运行 ID：`run.real-estate.2026-09-16.da171d2e.3c536216.583bdde0`

研究问题：核对讨论中2021年房地产收缩的指标口径，并解释为何新开工减少不必然意味着房价上涨。

数据截止：2026-09-16；状态：待人工审核；模式：historical_reconstruction。

## 已核对的指标

| 指标 | 期间 | 值 | 单位 | 证据 |
|---|---|---:|---|---|
| 房屋新开工面积（累计） | 2021-01-01 至 2021-11-30 | 182820 | 万平方米 | evidence.nbs.11.construction |
| 房屋新开工面积累计同比 | 2021-01-01 至 2021-11-30 | -9.1 | % | evidence.nbs.11.construction |
| 土地购置面积（累计） | 2021-01-01 至 2021-11-30 | 18287 | 万平方米 | evidence.nbs.11.land |
| 土地购置面积累计同比 | 2021-01-01 至 2021-11-30 | -11.2 | % | evidence.nbs.11.land |
| 房企到位资金：国内贷款累计同比 | 2021-01-01 至 2021-11-30 | -10.8 | % | evidence.nbs.11.funding |
| 房企总到位资金累计同比 | 2021-01-01 至 2021-11-30 | 7.2 | % | evidence.nbs.11.funding |
| 房屋施工面积累计同比 | 2021-01-01 至 2021-11-30 | 6.3 | % | evidence.nbs.11.construction |
| 商品房销售面积累计同比 | 2021-01-01 至 2021-11-30 | 4.8 | % | evidence.nbs.11.sales |
| 房屋新开工面积（累计） | 2021-01-01 至 2021-12-31 | 198895 | 万平方米 | evidence.nbs.12.construction |
| 房屋新开工面积累计同比 | 2021-01-01 至 2021-12-31 | -11.4 | % | evidence.nbs.12.construction |
| 土地购置面积（累计） | 2021-01-01 至 2021-12-31 | 21590 | 万平方米 | evidence.nbs.12.land |
| 土地购置面积累计同比 | 2021-01-01 至 2021-12-31 | -15.5 | % | evidence.nbs.12.land |
| 房企到位资金：国内贷款累计同比 | 2021-01-01 至 2021-12-31 | -12.7 | % | evidence.nbs.12.funding |
| 房企总到位资金累计同比 | 2021-01-01 至 2021-12-31 | 4.2 | % | evidence.nbs.12.funding |
| 房屋施工面积累计同比 | 2021-01-01 至 2021-12-31 | 5.2 | % | evidence.nbs.12.construction |
| 商品房销售面积累计同比 | 2021-01-01 至 2021-12-31 | 1.9 | % | evidence.nbs.12.sales |

## 因子解释（草稿）

### 房企融资与现金流结构

国内贷款累计下降、总到位资金仍增长，提示资金来源结构变化。它支持融资约束假设，但不能单凭全国汇总值证明所有房企资金链断裂。

状态：2021年银行贷款来源收缩；整体流动性因企业而异；置信度：medium。

反转条件：同口径国内贷款与销售回款持续改善，且有企业现金流证据证明约束缓解。

### 开发投资意愿与未来供给

新开工和拿地均收缩，与融资和预期有关；二者不当作独立投票。新开工是未来供给流量，施工面积还包含往期开工项目。

状态：2021年新增开发活动收缩；置信度：medium。

反转条件：同口径新开工、拿地与销售连续改善，或证明下降主要来自统计口径调整。

### 销售需求与城市分化

全年销售面积累计增长不排除下半年走弱。当前缺少月度、城市、二手房成交与库存数据，不能确认需求比供给下降更快。

状态：待补充数据；置信度：low。

反转条件：补齐城市层级和月度销售量价数据后重新评估。

### 购买力与估值约束

房价相对收入、租金和融资成本会影响支付能力；目前讨论中的估值阈值和城镇化瓶颈没有独立核验。

状态：无法据现有证据定量判断；置信度：low。

反转条件：取得同城同期住房价格、家庭收入中位数、租金及按揭条件后重新计算。

## 因果机制（待检验假设）

- factor.re.financing → 新开工计划：在销售预期和政策条件相近时，融资可得性改善可能支持新开工，融资约束可能使项目延后；同期相关性尚未识别因果。；时滞：数月至数季，尚未估计；反证：融资改善后新开工仍持续下降，且其他条件相近，需检验需求与库存是否为主导。

- factor.re.development → 未来新房价格：需求不变且存量供给有限时，新增供给下降可能支撑价格；若需求下降更快或二手房供给增加，价格仍可能承压。；时滞：从开工到可售或交付存在地区差异；反证：同城供给收缩而需求稳定，价格仍下降时需检查库存、质量和政策。

## 条件性情景（草稿）

### 基准假设：融资约束与需求偏弱并存

条件：融资恢复有限；销售需求未显著改善；这一前提尚未被本轮数据确认

观察：补齐月度销售、回款和新开工同比；观察城市库存去化

反证：融资与销售同步持续改善

### 向好假设：需求恢复、供给收缩支撑局部市场

条件：政策与融资传导有效；人口流入城市需求恢复且库存可控

观察：同城销售回暖、去化期缩短；新开工恢复滞后于销售

反证：销量改善不能持续或库存继续累积

### 压力假设：现金流与购房信心相互拖累

条件：销售回款继续弱化；交付与偿债压力升高并影响信心

观察：企业经营现金流和债务到期数据恶化；同城成交下降、去化期拉长

反证：交付、回款与信用条件稳定改善

## 审核缺口

- 本轮为2026年对2021年资料的历史重建，不是2021年真实预测，也不是无前视偏差回测。
- 2021年全年统计于2022年1月17日发布，不能用于声称在2021年12月31日已知全年结果。
- 视频仅保存NotebookLM可见转录片段，未下载原视频；页面采集也不保证包含未加载内容。
- NotebookLM原有引用编号只在对应消息中有意义，未全部解析成原文件页码/时间戳。
- 两个同名框架来源保留独立登记，尚未确认是否为同一版本，不能重复计权。
- -31.2%单月新开工降幅尚未独立复算；累计同比不能直接相减。
- 2023—2025年土地面积行业估算、房价收入比阈值和70%城镇化瓶颈均待核验。
- 因果机制与情景为本地Agent整理的假设，当前缺少城市量价、库存、家庭收入和企业现金流证据。
- 历史2021年指标不能用于直接发布2026年市场方向。
- 4 条说法尚未核验，不得作为正式事实。
- 14 个来源仅采集到部分内容。

## 来源与复查入口

- [source.lidang.notebook-entry-00](../raw/real-estate/txt/source.lidang.notebook-entry-00/snapshot.source.lidang.notebook-entry-00.2a56de894b211763/source-00.txt)（ai_generated，partial）
- [source.lidang.notebook-entry-01](../raw/real-estate/txt/source.lidang.notebook-entry-01/snapshot.source.lidang.notebook-entry-01.bee697a2a0c1ac34/source-01.txt)（secondary，partial）
- [source.lidang.notebook-entry-02](../raw/real-estate/txt/source.lidang.notebook-entry-02/snapshot.source.lidang.notebook-entry-02.eae602987224efd7/source-02.txt)（secondary，partial）
- [source.lidang.notebook-entry-03](../raw/real-estate/txt/source.lidang.notebook-entry-03/snapshot.source.lidang.notebook-entry-03.9b8c4eccf3518a87/source-03.txt)（user_authored，partial）
- [source.lidang.notebook-entry-04](../raw/real-estate/txt/source.lidang.notebook-entry-04/snapshot.source.lidang.notebook-entry-04.c30d53889e514ce6/source-04.txt)（user_authored，partial）
- [source.lidang.notebook-entry-05](../raw/real-estate/txt/source.lidang.notebook-entry-05/snapshot.source.lidang.notebook-entry-05.fcba69a43032fefa/source-05.txt)（secondary，partial）
- [source.lidang.notebook-entry-06](../raw/real-estate/txt/source.lidang.notebook-entry-06/snapshot.source.lidang.notebook-entry-06.4065fed6a1bb4f0a/source-06.txt)（secondary，partial）
- [source.lidang.notebook-entry-07](../raw/real-estate/txt/source.lidang.notebook-entry-07/snapshot.source.lidang.notebook-entry-07.0b8129c46a1f1aff/source-07.txt)（secondary，partial）
- [source.lidang.notebook-entry-08](../raw/real-estate/txt/source.lidang.notebook-entry-08/snapshot.source.lidang.notebook-entry-08.4cff74811e01c1db/source-08.txt)（secondary，partial）
- [source.lidang.notebook-entry-09](../raw/real-estate/txt/source.lidang.notebook-entry-09/snapshot.source.lidang.notebook-entry-09.34eedd4f264d8b28/source-09.txt)（secondary，partial）
- [source.lidang.notebook-entry-10](../raw/real-estate/txt/source.lidang.notebook-entry-10/snapshot.source.lidang.notebook-entry-10.9c2764ca55b22569/source-10.txt)（ai_generated，partial）
- [source.lidang.notebook-entry-11](../raw/real-estate/txt/source.lidang.notebook-entry-11/snapshot.source.lidang.notebook-entry-11.e25d4759edbf0b4c/source-11.txt)（ai_generated，partial）
- [source.lidang.discussion](../raw/real-estate/txt/source.lidang.discussion/snapshot.source.lidang.discussion.61f536f3736bbfea/notebook-visible.txt)（ai_generated，partial）
- [source.lidang.factor-guide](../raw/real-estate/txt/source.lidang.factor-guide/snapshot.source.lidang.factor-guide.3a1ec6946681d06e/studio-factor-guide.txt)（ai_generated，partial）
- [source.nbs.real-estate.2021-11](../raw/real-estate/md/source.nbs.real-estate.2021-11/snapshot.source.nbs.real-estate.2021-11.24ee0be46e849f2b/nbs-2021-11.md)（primary，article_text）
- [source.nbs.real-estate.2021-12](../raw/real-estate/md/source.nbs.real-estate.2021-12/snapshot.source.nbs.real-estate.2021-12.51a5a32782f9fe3d/nbs-2021-12.md)（primary，article_text）

## 下一步

- 人工核对因子与情景
- 补齐待核验说法的原始来源
- 用独立结果数据做后续复盘

本轮只完成研究整理与数据核验，尚未发布投资判断；复盘不能替代未来结果验证。
