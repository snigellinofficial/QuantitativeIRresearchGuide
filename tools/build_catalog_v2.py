# -*- coding: utf-8 -*-
"""合并核验结果，套用人工选题与分类，生成 catalog-v2.json。

难度阶梯口径：
  1 描述与多元回归
  2 面板固定效应与双重差分
  3 工具变量、断点、合成控制、shift-share
  4 网络模型、结构模型、机器学习与遥感测量
  5 方法学前沿（异质性稳健估计、空间推断、聚合偏差）
数据形态：点、线、面、栅格、关系边、混合。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "verified2.json")
OUT = os.path.join(ROOT, "catalog-v2.json")

TOPIC_NAME = {
    "G": "地理、可达性与基础设施",
    "C": "冲突、资源与政治暴力",
    "S": "制裁、经济治国与全球价值链",
    "I": "国际制度、援助与发展",
    "N": "网络、依赖与等级",
    "L": "气候、迁移与灾害",
    "F": "测量、机器学习与前沿",
    "M": "方法论基石",
}

# (编号, 题名检索键, 简称, 难度, 数据形态, 识别策略, 观测单元, 一句话贡献)
SEL = [
    # ---------------- G 地理、可达性与基础设施
    ("G01", "Measuring Economic Growth from Outer Space", "Henderson 等 2012", 3, "栅格", "测量误差模型", "国家—年与次国家区域", "把夜间灯光当作带误差的产出代理，推导出更优的增长率估计量。"),
    ("G02", "The Persistent Effects of Peru's Mining Mita", "Dell 2010", 3, "混合", "空间断点回归", "县与到边界的距离", "用殖民劳役区边界切出邻域样本，识别制度的长期效应。"),
    ("G03", "Railroads and American Economic Growth", "Donaldson & Hornbeck 2016", 4, "线", "市场准入＋结构模型", "美国县", "把路网写成最短路函数，构造市场准入并接入一般均衡模型。"),
    ("G04", "Did Highways Cause Suburbanization", "Baum-Snow 2007", 3, "线", "工具变量", "大都市统计区", "用一九四七年规划路网作工具，识别高速公路对郊区化的影响。"),
    ("G05", "Trade Integration, Market Size, and Industrialization", "Faber 2014", 3, "混合", "双重差分＋工具变量", "中国县", "以规划线路而非建成线路构造处理变量，避开选址内生性。"),
    ("G06", "On the road: Access to transportation infrastructure", "Banerjee 等 2020", 3, "线", "双重差分＋工具变量", "中国县", "用路网连接与距离衰减构造可达性，估计交通对增长的效应。"),
    ("G07", "Pre-Colonial Ethnic Institutions and Contemporary African Development", "Michalopoulos & Papaioannou 2013", 3, "混合", "空间断点＋边界固定效应", "族群家园多边形与网格", "把人类学地图转成多边形，用边界两侧比较抵消地理混淆。"),
    ("G08", "National Institutions and Subnational Development in Africa", "Michalopoulos & Papaioannou 2014", 3, "栅格", "跨国界空间断点", "国界两侧网格", "同一族群被国界切开，两侧制度不同而地理相同。"),
    ("G09", "The Effects of Rural Electrification on Employment", "Dinkelman 2011", 3, "点", "工具变量＋固定效应", "南非农村社区", "以坡度与既有电网距离预测电网落点。"),
    ("G10", "The Economics of Density: Evidence from the Berlin Wall", "Ahlfeldt 等 2015", 4, "面", "空间断点＋结构模型", "柏林地块", "用一道被拆除的墙估计集聚弹性，再送回一般均衡做反事实。"),
    ("G11", "Rural Roads and Local Economic Development", "Asher & Novosad 2020", 2, "点", "双重差分＋事件研究", "印度村庄", "以工程批次构造处理时点，用事件研究检验事前趋势。"),
    ("G12", "The Value of Democracy: Evidence from Road Building in Kenya", "Burgess 等 2015", 2, "线", "差分中的差分", "道路分段与选区", "把路网拆成分段，检验民主化是否收窄族群偏袒。"),
    ("G13", "The Permanent Effects of Transportation Revolutions", "Jedwab & Moradi 2016", 2, "点", "准外生路线的长期比较", "加纳城镇点位", "用殖民路线的规划走向识别交通投资的持久影响。"),
    ("G14", "Development Effects of Electrification", "Lipscomb 等 2013", 3, "混合", "工具变量", "巴西自治市", "以河流落差代理发电潜力，作为电网落点的工具。"),
    ("G15", "Roads to Rule, Roads to Rebel", "Müller-Crepon 2020", 3, "线", "关系型国家能力＋空间模型", "非洲网格与路网", "把路网视为国家向地方投射权力的关系结构。"),
    ("G16", "Regional Favoritism", "Hodler & Raschky 2014", 3, "栅格", "三重差分＋三层固定效应", "夜光像素与族群聚居区", "用像素、国家—年、族群—年三层固定效应留下偏袒的净效应。"),

    # ---------------- C 冲突、资源与政治暴力
    ("C01", "Ethnicity, Insurgency, and Civil War", "Fearon & Laitin 2003", 1, "面", "横截面回归", "国家—年", "把内战发生写成国家能力与族群结构的函数。"),
    ("C02", "Armed Conflict 1946-2001: A New Dataset", "Gleditsch 等 2002", 1, "面", "数据基础设施", "冲突事件", "建立武装冲突的最低伤亡门槛与统一编码规则。"),
    ("C03", "Economic Shocks and Civil Conflict", "Miguel 等 2004", 3, "栅格", "气象工具变量", "国家—年", "以降雨增长率作收入的工具，估计经济冲击对冲突的影响。"),
    ("C04", "Introducing ACLED", "Raleigh 等 2010", 1, "点", "数据基础设施", "冲突事件", "把冲突事件编码到经纬度与日期，打开次国家分析。"),
    ("C05", "Introducing the UCDP Georeferenced Event Dataset", "Sundberg & Melander 2013", 1, "点", "数据基础设施", "冲突事件", "提供带地理坐标与精度的冲突事件数据。"),
    ("C06", "Toward a Democratic Civil Peace", "Hegre 等 2001", 1, "面", "面板逻辑斯蒂回归", "国家—年", "区分民主的层级与时间变动对内战风险的作用。"),
    ("C07", "Commodity Price Shocks and Civil Conflict: Evidence from Colombia", "Dube & Vargas 2013", 3, "面", "价格冲击＋固定效应", "哥伦比亚市镇", "不同作物价格冲击对冲突的影响方向不同。"),
    ("C08", "Horizontal Inequalities and Ethnonationalist Civil War", "Cederman 等 2011", 2, "面", "族群层面的不平等测量", "族群—年", "把族群间的经济与政治排斥写成可测量的变量。"),
    ("C09", "This Mine is Mine! How Minerals Fuel Conflicts in Africa", "Berman 等 2017", 3, "栅格", "格内价格冲击＋三重差分", "零点五度网格—月", "全球矿价乘本地禀赋，构造随格子与月份变动的暴露度。"),
    ("C10", "PRIO-GRID: A unified spatial data structure", "Tollefsen 等 2012", 1, "栅格", "数据基础设施", "全球零点五度网格", "统一网格主键与聚合规则，使跨数据源结果可比。"),
    ("C11", "Economic Shocks and Conflict: Evidence from Commodity Prices", "Bazzi & Blattman 2014", 3, "面", "价格工具变量", "国家—年", "用出口价格指数作收入冲击的工具，检验冲突响应。"),
    ("C12", "On the Origins of the State", "Sanchez de la Sierra 2020", 3, "点", "空间断点＋田野数据", "刚果东部村落", "用道路与地形构造的国家投射边界识别征税与暴力。"),
    ("C13", "Climatic Stress, Internal Migration, and Syrian Civil War Onset", "Ash & Obradovich 2020", 2, "栅格", "中介分析＋面板", "叙利亚次国家区域", "把气候压力经迁移传导到冲突的路径拆成两步。"),

    # ---------------- S 制裁、经济治国与全球价值链
    ("S01", "Weaponized Interdependence", "Farrell & Newman 2019", 1, "关系边", "网络结构论证", "全球网络节点", "把经济网络中的枢纽位置写成可被武器化的权力。"),
    ("S02", "The Return to Protectionism", "Fajgelbaum 等 2020", 2, "面", "关税冲击＋弹性估计", "美国县与行业", "用二零一八年关税的暴露度估计价格与福利效应。"),
    ("S03", "The Impact of the 2018 Tariffs on Prices and Welfare", "Amiti 等 2019", 2, "面", "关税传递回归", "进口品—月", "估计关税在进口价格上的完全传递。"),
    ("S04", "Exchange Arrangements Entering the Twenty-First Century", "Ilzetzki 等 2019", 2, "面", "汇率制度分类＋面板", "国家—月", "重建汇率制度分类，刻画锚货币的分布。"),
    ("S05", "Dominant Currency Paradigm", "Gopinath 等 2020", 3, "面", "主导货币定价检验", "国家—产品—月", "证明贸易定价以美元为主导，而非生产者货币。"),
    ("S06", "Threat and imposition of economic sanctions 1945-2005", "Morgan 等 2014", 1, "面", "威胁—实施两阶段", "威胁事件", "把制裁拆成威胁与实施两个阶段并编码。"),
    ("S07", "Anxiety or pain? The impact of tariffs", "Benguria 等 2022", 2, "面", "企业层面差分", "中国上市企业", "区分关税的直接影响与不确定性渠道。"),
    ("S08", "Friendly fire: the trade impact of the Russia sanctions", "Crozet & Hinz 2020", 2, "面", "三重差分", "企业—目的地—产品", "用欧盟企业内部差异识别制裁的贸易损失。"),
    ("S09", "The sword and the shield: the economics of targeted sanctions", "Ahn & Ludema 2020", 4, "关系边", "网络中心性＋结构估计", "企业与所有权网络", "把定向制裁写成网络中心性的函数并估计其福利代价。"),
    ("S10", "Introduction: The Power of Global Performance Indicators", "Kelley & Simmons 2019", 1, "面", "指标作为治理工具", "国家—年", "把国际排名当作一种无需强制力的治理手段。"),
    ("S11", "Wars without Gun Smoke", "Chen 2023", 4, "关系边", "供应链网络模型", "国家—行业", "把全球供应链的结构写成权力转移与经济治国的约束。"),
    ("S12", "Collective Resilience: Deterring China", "Cha 2023", 1, "关系边", "依赖性测量与比较", "国家—产品", "用进口集中度衡量被胁迫的脆弱性与集体韧性。"),
    ("S13", "Beyond ports, roads and railways", "Petry 2022", 1, "线", "过程追踪与描述", "一带一路项目", "把互联互通项目读作地缘经济权力的载体。"),

    # ---------------- I 国际制度、援助与发展
    ("I01", "Who Gives Foreign Aid to Whom and Why", "Alesina & Dollar 2000", 1, "面", "双边援助面板回归", "援助国—受援国—年", "把援助分配写成殖民关系、战略与民主程度的函数。"),
    ("I02", "Hard and Soft Law in International Governance", "Abbott & Snidal 2000", 1, "面", "概念化的可测维度", "条约条款", "把法律的硬度拆成义务、精确与授权三个维度。"),
    ("I03", "Delegation to international organizations", "Nielson & Tierney 2003", 2, "面", "委托—代理回归", "世界银行项目", "用代理理论检验委托方对国际组织的控制。"),
    ("I04", "Development aid and international politics", "Dreher 等 2009", 3, "面", "安理会席位作为外生变动", "受援国—年", "用非常任理事国席位轮换识别世界银行贷款的政治偏向。"),
    ("I05", "The Independence of International Organizations", "Haftel & Thompson 2006", 1, "面", "指标构造与相关", "国际组织", "把国际组织的独立性写成可比较的指标。"),
    ("I06", "Foreign Aid and Soft Power", "Blair 等 2021", 2, "面", "调查实验＋地理分配", "非洲受访者", "用调查实验测量援助对受援国民众态度的作用。"),
    ("I07", "Hybrid institutional complexes in global governance", "Abbott 等 2021", 1, "面", "制度重叠的描述统计", "制度—议题", "刻画议题领域内正式与非正式制度的混合结构。"),
    ("I08", "Foreign Aid, Human Rights, and Democracy Promotion", "Carnegie & Marinov 2017", 3, "面", "自然实验", "受援国—年", "用援助项目的时点变动识别对外部治理的效应。"),
    ("I09", "Why International Organizations Commit to Liberal Norms", "Tallberg 等 2020", 1, "面", "文本编码与回归", "国际组织", "把国际组织的规范承诺编码后解释其差异。"),
    ("I10", "Foreign Aid and State Legitimacy", "Blair 等 2021b", 2, "面", "调查实验", "非洲受访者", "区分不同援助来源对合法性的差异化影响。"),
    ("I11", "The Rational Design of International Institutions", "Koremenos 等 2001", 1, "面", "设计维度的概念化", "制度条款", "提出成员数、范围、集中度等五个可测的设计维度。"),
    ("I12", "Diplomacy and domestic politics", "Putnam 1988", 1, "面", "两层博弈框架", "国家间谈判", "把国际谈判写成国内批准约束下的两层博弈。"),

    # ---------------- N 网络、依赖与等级
    ("N01", "Supply Chain Disruptions: Evidence from the Great East Japan Earthquake", "Carvalho 等 2021", 4, "关系边", "网络传播模型", "日本企业", "用震灾冲击估计供应链网络的传播与恢复。"),
    ("N02", "The Diffusion of Microfinance", "Banerjee 等 2013", 4, "关系边", "网络中心性＋工具变量", "印度村庄的家庭", "先做网络普查，再识别参与沿网络而非地理扩散。"),
    ("N03", "Input Linkages and the Transmission of Shocks", "Boehm 等 2019", 4, "关系边", "投入产出网络＋企业差分", "日本企业与其海外子公司", "用母公司冲击识别投入联系对子公司产出的传导。"),
    ("N04", "Inferential Network Analysis with Exponential Random Graph Models", "Cranmer & Desmarais 2011", 4, "关系边", "指数随机图模型", "国际组织成员网络", "把整张图当因变量，用结构统计量建立似然。"),
    ("N05", "Supply Network Formation and Fragility", "Elliott 等 2022", 5, "关系边", "网络形成＋一般均衡", "企业网络", "把网络形成内生化为成本与风险的权衡。"),
    ("N06", "Intergovernmental Organizations and the Kantian Peace", "Dorussen & Ward 2008", 3, "关系边", "网络加权＋冲突回归", "国家对—年", "把国际组织成员关系转成对距离加权的网络变量。"),
    ("N07", "What Is the Enemy of My Enemy", "Maoz 等 2007", 3, "关系边", "结构平衡指数", "国家对—年", "用符号网络的结构平衡衡量关系格局。"),
    ("N08", "Ethnonationalist Triads", "Cederman 等 2009", 3, "关系边", "三元组逻辑斯蒂回归", "政府—族群—外部亲缘族群", "把关系的组合而非个体属性当作观测单元。"),
    ("N09", "Complex Dependencies in the Alliance Network", "Cranmer 等 2012", 4, "关系边", "指数随机图＋时间指数", "国家对—年", "在联盟网络中同时建模互惠、传递与时间依赖。"),
    ("N10", "Network Dynamics and the Evolution of International Cooperation", "Kinne 2013", 4, "关系边", "随机行为者导向模型", "国家对—年", "把合作网络的形成写成行为者的局部选择规则。"),
    ("N11", "Gravity's Rainbow", "Ward 等 2013", 4, "关系边", "动态潜在空间模型", "国家对—年", "把国家亲疏压缩成低维坐标，用坐标距离替代虚拟变量。"),

    # ---------------- L 气候、迁移与灾害
    ("L01", "What Do We Learn from the Weather", "Dell 等 2014", 1, "栅格", "文献综述与方法分类", "多尺度", "把气象冲击的识别策略整理成一套统一框架。"),
    ("L02", "Quantifying the Influence of Climate on Human Conflict", "Hsiang 等 2013", 2, "栅格", "元分析与统一效应量", "多尺度", "把分散的估计换算成可比的标准化效应量。"),
    ("L03", "Temperature Shocks and Economic Growth", "Dell 等 2012", 2, "面", "面板温度冲击", "国家—年", "把温度与降水的高阶项放进增长回归。"),
    ("L04", "Adapting to Climate Change", "Barreca 等 2016", 2, "面", "长期面板＋技术变迁", "美国州—年", "证明温度—死亡率关系的下降来自适应技术。"),
    ("L05", "Climate Change, Mortality, and Adaptation", "Deschenes & Greenstone 2011", 2, "面", "面板气象冲击", "美国县—年", "用年度天气波动识别气温对死亡率的因果效应。"),
    ("L06", "Valuing the Global Mortality Consequences of Climate Change", "Carleton 等 2022", 5, "栅格", "全局剂量反应＋结构外推", "全球次国家单元", "用跨四十一国的面板估计统一的气温—死亡率反应函数。"),
    ("L07", "The migration response to increasing temperatures", "Cattaneo & Peri 2016", 2, "面", "面板＋长期差分", "原籍国—目的地", "区分国内迁移与国际迁移对温度的不同响应。"),
    ("L08", "The impact of weather anomalies on migration", "Marchiori 等 2012", 2, "面", "面板气象冲击", "撒哈拉以南国家—年", "把气象异常写成迁移率的解释变量。"),
    ("L09", "Nonlinear permanent migration response to climatic variations", "Bohra-Mishra 等 2014", 2, "点", "非线性剂量反应", "印度尼西亚家庭", "估计气候异常对永久迁移的非线性响应。"),
    ("L10", "Asylum applications respond to temperature fluctuations", "Missirian & Schlenker 2017", 2, "面", "面板＋外推", "原籍国—年", "把温度波动与避难申请联系起来并做未来外推。"),
    ("L11", "Drought and Civil War in Sub-Saharan Africa", "Couttenier & Soubeyran 2014", 2, "栅格", "干旱冲击面板", "撒哈拉以南网格", "用干旱指数刻画农业收入冲击与冲突风险。"),

    # ---------------- F 测量、机器学习与前沿
    ("F01", "Double/debiased machine learning", "Chernozhukov 等 2018", 5, "混合", "双重机器学习", "通用", "用交叉拟合与正交矩条件消除机器学习带来的正则化偏误。"),
    ("F02", "Text as Data: The Promise and Pitfalls", "Grimmer & Stewart 2013", 1, "关系边", "文本编码与效度检验", "政治文本", "提出文本分类必须做人工验证与效度检查。"),
    ("F03", "Estimation and Inference of Heterogeneous Treatment Effects", "Wager & Athey 2018", 5, "混合", "因果森林", "通用", "把随机森林改造成异质处理效应的估计量并给出推断。"),
    ("F04", "Machine Learning: An Applied Econometric Approach", "Mullainathan & Spiess 2017", 1, "混合", "预测与因果的分工", "通用", "区分预测目标与参数目标，提出两类任务的不同工具。"),
    ("F05", "Combining satellite imagery and machine learning to predict poverty", "Jean 等 2016", 4, "栅格", "迁移学习", "非洲五国小区域", "用夜光预训练再以调查数据校准，两阶段分离。"),
    ("F06", "Machine Learning Methods That Economists Should Know About", "Athey & Imbens 2019", 1, "混合", "方法综述", "通用", "把机器学习方法按统计目标分类整理。"),
    ("F07", "Using luminosity data as a proxy for economic statistics", "Chen & Nordhaus 2011", 2, "栅格", "代理变量回归", "国家—年", "检验灯光对产出的解释力并量化其误差结构。"),
    ("F08", "Predicting poverty and wealth from mobile phone metadata", "Blumenstock 等 2015", 4, "点", "监督学习", "卢旺达手机用户", "用通话与充值记录预测个人财富。"),
    ("F09", "Large-Scale Computerized Text Analysis in Political Science", "Wilkerson & Casas 2017", 1, "关系边", "文本计分与降维", "政治文本", "把大规模文本压缩成可回归的连续维度。"),
    ("F10", "Machine learning and phone data can improve targeting of humanitarian aid", "Aiken 等 2022", 4, "点", "预测评估＋瞄准误差", "多哥手机用户", "在同一评估集上比较手机数据与代理家计调查的瞄准精度。"),
    ("F11", "Using machine learning to assess the livelihood impact of electricity access", "Ratledge 等 2022", 5, "栅格", "影像测量＋双重稳健去偏", "乌干达村庄", "把构造结果变量与估计因果效应分成两个独立步骤。"),
    ("F12", "Aggregation Bias in Proxy Measurement", "Fiaschi 等 2026", 5, "栅格", "反向回归分解", "行政单元", "把聚合层级写成模型参数，分解预测弹性的三个来源。"),

    # ---------------- M 方法论基石
    ("M01", "Difference-in-Differences with multiple time periods", "Callaway & Sant'Anna 2021", 5, "混合", "分组—时点稳健估计", "通用", "用分组与处理时点定义的条件效应替代双向固定效应。"),
    ("M02", "Difference-in-differences with variation in treatment timing", "Goodman-Bacon 2021", 5, "混合", "估计量分解", "通用", "把双向固定效应估计量分解为所有两两比较的加权和。"),
    ("M03", "Estimating dynamic treatment effects in event studies", "Sun & Abraham 2021", 5, "混合", "交互加权事件研究", "通用", "指出事件研究中污染系数的来源并给出修正估计量。"),
    ("M04", "Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects", "de Chaisemartin & D'Haultfoeuille 2020", 5, "混合", "负权重诊断", "通用", "证明双向固定效应估计量在效应异质时可能出现符号反转。"),
    ("M05", "Synthetic Control Methods for Comparative Case Studies", "Abadie 等 2010", 3, "面", "合成控制法", "单个处理单元", "用加权组合的对照单元构造反事实。"),
    ("M06", "The Economic Costs of Conflict: A Case Study of the Basque Country", "Abadie & Gardeazabal 2003", 3, "面", "合成控制法", "巴斯克地区", "首次用合成控制估计恐怖冲突的经济代价。"),
    ("M07", "Using Synthetic Controls", "Abadie 2021", 1, "面", "方法综述", "通用", "系统整理合成控制的可行性条件与推断方式。"),
    ("M08", "Quasi-Experimental Shift-Share Research Designs", "Borusyak 等 2022", 4, "混合", "份额移动设计", "通用", "把份额移动写成处理暴露度并给出识别条件。"),
    ("M09", "Shift-Share Designs: Theory and Inference", "Adao 等 2019", 5, "混合", "暴露度推断", "通用", "指出份额移动的推断须按暴露度调整，并给出解析标准误。"),
    ("M10", "Robust Inference With Multiway Clustering", "Cameron 等 2011", 5, "混合", "多维聚类", "通用", "给出双向与多维聚类的三明治方差估计量。"),
    ("M11", "Logistic Regression in Rare Events Data", "King & Zeng 2001", 2, "面", "稀有事件校正", "通用", "指出稀有事件下逻辑回归的偏误并给出校正与抽样设计。"),
    ("M12", "Greed and grievance in civil war", "Collier & Hoeffler 2004", 1, "面", "横截面回归", "国家—年", "把内战发生写成可掠夺资源与不满两类变量的函数。"),
]


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def main():
    rows = json.load(open(SRC, encoding="utf-8"))
    by_key = {}
    for r in rows:
        by_key.setdefault(norm(r["title"])[:60], []).append(r)

    papers, missing = [], []
    for (pid, key, short, diff, kind, design, unit, gist) in SEL:
        topic = pid[0]
        cands = by_key.get(norm(key)[:60])
        if not cands:
            # 前缀模糊匹配
            for k, v in by_key.items():
                if k.startswith(norm(key)[:40]):
                    cands = v
                    break
        if not cands:
            missing.append((pid, key))
            continue
        r = sorted(cands, key=lambda x: -(x.get("cites") or 0))[0]
        vol = r.get("volume") or ""
        iss = r.get("issue") or ""
        papers.append({
            "id": pid,
            "topic": topic,
            "topic_name": TOPIC_NAME[topic],
            "short": short,
            "authors": "; ".join(r.get("authors") or []),
            "year": r.get("year"),
            "title": r.get("title"),
            "venue": r.get("venue"),
            "volume": (vol + ("(" + iss + ")" if iss else "")) if vol else "",
            "doi": r.get("doi"),
            "cites": r.get("cites"),
            "difficulty": diff,
            "data_kind": kind,
            "design": design,
            "unit": unit,
            "gist": gist,
        })

    cat = {
        "meta": {
            "title": "国际政治量化研究文献目录（第二版）",
            "retrieved": "2026-10-29",
            "citation_source": "Crossref is-referenced-by-count，检索日期 2026-10-29",
            "scope_note": "引用量为 Crossref 口径，与 OpenAlex 及 Google 学术不同，三者不可混用。页码从略，卷期与 DOI 为核验字段。",
            "n_papers": len(papers),
            "difficulty_legend": {
                "1": "描述与多元回归",
                "2": "面板固定效应与双重差分",
                "3": "工具变量、断点、合成控制、份额移动",
                "4": "网络模型、结构模型、机器学习与遥感测量",
                "5": "方法学前沿：异质性稳健估计、空间推断、聚合偏差",
            },
        },
        "topics": [
            {"id": k, "name": v, "count": sum(1 for p in papers if p["topic"] == k)}
            for k, v in TOPIC_NAME.items()
        ],
        "papers": papers,
    }
    json.dump(cat, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("papers", len(papers), "missing", missing)
    from collections import Counter
    print(Counter(p["topic"] for p in papers))
    print(Counter(p["difficulty"] for p in papers))


if __name__ == "__main__":
    main()
