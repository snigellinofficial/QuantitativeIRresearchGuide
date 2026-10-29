# -*- coding: utf-8 -*-
"""按预设目标清单，用 Crossref 逐条核验题录。

思路：先以学科知识与顶刊清单草拟目标，再用 Crossref 的 bibliographic 检索
取得 DOI、刊物、卷期、页码与引用量。命中失败者列入未匹配报告，绝不臆造。
"""
import difflib
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "verified.json")
UA = "lit-review/1.0 (mailto:research-agent@example.org)"
WS = re.compile(r"\s+")
TAG = re.compile(r"<[^>]+>")

# (专题, 标题, 第一作者姓氏提示, 期望年份或 None)
TARGETS = [
    # ---------------- G 地理、可达性与基础设施
    ("G", "On the road: Access to transportation infrastructure and economic growth in China", "Banerjee", 2020),
    ("G", "Roads to Rule, Roads to Rebel: Relational State Capacity and Conflict in Africa", "Muller-Crepon", 2020),
    ("G", "The Economics of Urban Density", "Duranton", 2020),
    ("G", "On the Geography of Global Value Chains", "Antras", 2020),
    ("G", "Measuring Economic Growth from Outer Space", "Henderson", 2012),
    ("G", "Did Highways Cause Suburbanization?", "Baum-Snow", 2007),
    ("G", "The Persistent Effects of Peru's Mining Mita", "Dell", 2010),
    ("G", "Trade Integration, Market Size, and Industrialization: Evidence from China's National Trunk Highway System", "Faber", 2014),
    ("G", "Railroads and American Economic Growth: A \"Market Access\" Approach", "Donaldson", 2016),
    ("G", "Rural Roads and Local Economic Development", "Asher", 2020),
    ("G", "The Value of Democracy: Evidence from Road Building in Kenya", "Burgess", 2015),
    ("G", "Regional Favoritism", "Hodler", 2014),
    ("G", "The Effects of Rural Electrification on Employment: New Evidence from South Africa", "Dinkelman", 2011),
    ("G", "Development Effects of Electrification: Evidence from the Topographic Placement of Hydropower Plants in Brazil", "Lipscomb", 2013),
    ("G", "National Institutions and Subnational Development in Africa", "Michalopoulos", 2014),
    ("G", "Pre-Colonial Ethnic Institutions and Contemporary African Development", "Michalopoulos", 2013),

    # ---------------- C 冲突与政治暴力
    ("C", "Ethnicity, Insurgency, and Civil War", "Fearon", 2003),
    ("C", "Toward a Democratic Civil Peace? Democracy, Political Change, and Civil War, 1816-1992", "Hegre", 2001),
    ("C", "Armed Conflict 1946-2001: A New Dataset", "Gleditsch", 2002),
    ("C", "Introducing ACLED: An Armed Conflict Location and Event Dataset", "Raleigh", 2010),
    ("C", "Introducing the UCDP Georeferenced Event Dataset", "Sundberg", 2013),
    ("C", "Horizontal Inequalities and Ethnonationalist Civil War: A Global Comparison", "Cederman", 2011),
    ("C", "Economic Shocks and Civil Conflict: An Instrumental Variables Approach", "Miguel", 2004),
    ("C", "This Mine is Mine! How Minerals Fuel Conflicts in Africa", "Berman", 2017),
    ("C", "Economic Shocks and Conflict: Evidence from Commodity Prices", "Bazzi", 2014),
    ("C", "Commodity Price Shocks and Civil Conflict: Evidence from Colombia", "Dube", 2013),
    ("C", "On the Origins of the State: Stationary Bandits and Taxation in Eastern Congo", "Sanchez de la Sierra", 2020),
    ("C", "United Nations Peacekeeping Locally: Enabling Conflict Resolution, Reducing Communal Violence", "Smidt", 2019),
    ("C", "Climatic Stress, Internal Migration, and Syrian Civil War Onset", "Ash", 2020),
    ("C", "Prediction and Judgment: Why Artificial Intelligence Increases the Importance of Humans in War", "Goldfarb", 2022),
    ("C", "Non-state actors in civil wars: A new dataset", "Cunningham", 2013),
    ("C", "Voting for Victors: Why Violent Actors Win Postwar Elections", "Daly", 2019),

    # ---------------- S 制裁与经济治国
    ("S", "Weaponized Interdependence: How Global Economic Networks Shape State Coercion", "Farrell", 2019),
    ("S", "Threat and imposition of economic sanctions 1945-2005: Updating the TIES dataset", "Morgan", 2014),
    ("S", "The Return to Protectionism", "Fajgelbaum", 2020),
    ("S", "The Impact of the 2018 Tariffs on Prices and Welfare", "Amiti", 2019),
    ("S", "Anxiety or pain? The impact of tariffs and uncertainty on Chinese firms in the trade war", "Benguria", 2022),
    ("S", "Dominant Currency Paradigm", "Gopinath", 2020),
    ("S", "Exchange Arrangements Entering the Twenty-First Century: Which Anchor will Hold?", "Ilzetzki", 2019),
    ("S", "\"Wars without Gun Smoke\": Global Supply Chains, Power Transitions, and Economic Statecraft", "Chen", 2023),
    ("S", "Collective Resilience: Deterring China's Weaponization of Economic Interdependence", "Cha", 2023),
    ("S", "Infrastructural Geopolitics", "Goede", 2022),
    ("S", "Beyond ports, roads and railways: Chinese economic statecraft, the Belt and Road Initiative and the politics of global connectivity", "Petry", 2022),
    ("S", "Success of economic sanctions threats: coercion, information and commitment", "Walentek", 2021),
    ("S", "Introduction: The Power of Global Performance Indicators", "Kelley", 2019),
    ("S", "The Sword and the Shield: The Economics of Targeted Sanctions", "Ahn", 2020),
    ("S", "Friendly fire: the trade impact of the Russia sanctions and counter-sanctions", "Crozet", 2020),

    # ---------------- I 国际制度与援助
    ("I", "Diplomacy and domestic politics: the logic of two-level games", "Putnam", 1988),
    ("I", "Hard and Soft Law in International Governance", "Abbott", 2000),
    ("I", "The Rational Design of International Institutions", "Koremenos", 2001),
    ("I", "Who Gives Foreign Aid to Whom and Why?", "Alesina", 2000),
    ("I", "Development aid and international politics: Does membership on the UN Security Council influence World Bank decisions?", "Dreher", 2009),
    ("I", "Foreign Aid and State Legitimacy", "Blair", 2021),
    ("I", "Foreign Aid and Soft Power: Great Power Competition in Africa in the Early Twenty-first Century", "Blair", 2021),
    ("I", "Delegation to international organizations: Agency theory and World Bank environmental reform", "Nielson", 2003),
    ("I", "The independence of international organizations: Concept and applications", "Haftel", 2006),
    ("I", "Hybrid institutional complexes in global governance", "Abbott", 2021),
    ("I", "Why International Organizations Commit to Liberal Norms", "Tallberg", 2020),
    ("I", "Measuring institutional overlap in global governance", "Haftel", 2021),
    ("I", "Foreign Aid, Human Rights, and Democracy Promotion: Evidence from a Natural Experiment", "Carnegie", 2017),
    ("I", "Decision-making in international organizations: institutional design and performance", "Sommerer", 2021),
    ("I", "Money Talks: Foreign Aid and International Politics", "Dreher", 2009),

    # ---------------- N 网络、依赖与等级
    ("N", "Gravity's Rainbow: A Dynamic Latent Space Model for the World Trade Network", "Ward", 2013),
    ("N", "Inferential Network Analysis with Exponential Random Graph Models", "Cranmer", 2011),
    ("N", "The Diffusion of Microfinance", "Banerjee", 2013),
    ("N", "Ethnonationalist Triads: Assessing the Influence of Kin Groups on Civil Wars", "Cederman", 2009),
    ("N", "Intergovernmental Organizations and the Kantian Peace: A Network Perspective", "Dorussen", 2008),
    ("N", "Power Positions: International Organizations, Social Networks, and Conflict", "Hafner-Burton", 2006),
    ("N", "Network Dynamics and the Evolution of International Cooperation", "Kinne", 2013),
    ("N", "What Is the Enemy of My Enemy? Causes and Consequences of Imbalanced International Relations, 1816-2001", "Maoz", 2007),
    ("N", "Complex Dependencies in the Alliance Network", "Cranmer", 2012),
    ("N", "Networks of Cooperation: Rebel Alliances in Fragmented Civil Wars", "Gade", 2019),
    ("N", "Supply Chain Disruptions: Evidence from the Great East Japan Earthquake", "Carvalho", 2021),
    ("N", "Input Linkages and the Transmission of Shocks: Firm-Level Evidence from the 2011 Tohoku Earthquake", "Boehm", 2019),
    ("N", "Supply Network Formation and Fragility", "Elliott", 2022),

    # ---------------- L 气候、迁移与灾害
    ("L", "Quantifying the influence of climate on human conflict", "Hsiang", 2013),
    ("L", "Climate and Conflict", "Burke", 2015),
    ("L", "Temperature Shocks and Economic Growth: Evidence from the Last Half Century", "Dell", 2012),
    ("L", "What Do We Learn from the Weather? The New Climate-Economy Literature", "Dell", 2014),
    ("L", "Asylum applications respond to temperature fluctuations", "Missirian", 2017),
    ("L", "Nonlinear permanent migration response to climatic variations but minimal response to disasters", "Bohra-Mishra", 2014),
    ("L", "The impact of weather anomalies on migration in sub-Saharan Africa", "Marchiori", 2012),
    ("L", "The migration response to increasing temperatures", "Cattaneo", 2016),
    ("L", "The causal effect of environmental catastrophe on long-run human capital formation", "Hsiang", 2014),
    ("L", "Climate change, mortality, and adaptation: Evidence from annual fluctuations in weather in the US", "Deschenes", 2011),
    ("L", "Adapting to Climate Change: The Remarkable Decline in the US Temperature-Mortality Relationship over the Twentieth Century", "Barreca", 2016),
    ("L", "Valuing the Global Mortality Consequences of Climate Change Accounting for Adaptation Costs and Benefits", "Carleton", 2022),
    ("L", "Drought and Civil War in Sub-Saharan Africa", "Couttenier", 2014),

    # ---------------- F 测量、机器学习与前沿
    ("F", "Combining satellite imagery and machine learning to predict poverty", "Jean", 2016),
    ("F", "Machine learning and phone data can improve targeting of humanitarian aid", "Aiken", 2022),
    ("F", "Predicting poverty and wealth from mobile phone metadata", "Blumenstock", 2015),
    ("F", "Text as Data", "Gentzkow", 2019),
    ("F", "Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts", "Grimmer", 2013),
    ("F", "Large-Scale Computerized Text Analysis in Political Science: Opportunities and Challenges", "Wilkerson", 2017),
    ("F", "Machine Learning: An Applied Econometric Approach", "Mullainathan", 2017),
    ("F", "Machine Learning Methods That Economists Should Know About", "Athey", 2019),
    ("F", "Double/debiased machine learning for treatment and structural parameters", "Chernozhukov", 2018),
    ("F", "Estimation and Inference of Heterogeneous Treatment Effects using Random Forests", "Wager", 2018),
    ("F", "Using machine learning to assess the livelihood impact of electricity access", "Ratledge", 2022),
    ("F", "The changing surface of the world's roads", "Randhawa", 2026),
    ("F", "Aggregation Bias in Proxy Measurement: Nighttime Lights and Local Economic Activity", "Fiaschi", 2026),
    ("F", "Using luminosity data as a proxy for economic statistics", "Chen", 2011),

    # ---------------- M 方法基石（贯穿各专题）
    ("M", "Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects", "de Chaisemartin", 2020),
    ("M", "Difference-in-Differences with variation in treatment timing", "Goodman-Bacon", 2021),
    ("M", "Difference-in-Differences with multiple time periods", "Callaway", 2021),
    ("M", "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects", "Sun", 2021),
    ("M", "Shift-Share Designs: Theory and Inference", "Adao", 2019),
    ("M", "Quasi-Experimental Shift-Share Research Designs", "Borusyak", 2022),
    ("M", "Bartik Instruments: What Do (and Don't Do) When You Use Them", "Goldsmith-Pinkham", 2020),
    ("M", "The Economic Costs of Conflict: A Case Study of the Basque Country", "Abadie", 2003),
    ("M", "Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program", "Abadie", 2010),
    ("M", "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects", "Abadie", 2021),
    ("M", "Robust Inference With Multiway Clustering", "Cameron", 2011),
    ("M", "Greed and grievance in civil war", "Collier", 2004),
    ("M", "Civil War", "Blattman", 2010),
    ("M", "The Colonial Origins of Comparative Development: An Empirical Investigation", "Acemoglu", 2001),
    ("M", "Logistic Regression in Rare Events Data", "King", 2001),
]


def fetch(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if k == tries - 1:
                return {}
            time.sleep(2.0)
    return {}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def clean(t):
    if not t:
        return ""
    return WS.sub(" ", html.unescape(TAG.sub(" ", t))).strip()


def verify(topic, title, hint, year):
    q = urllib.parse.quote(title)
    url = ("https://api.crossref.org/works?query.bibliographic=" + q +
           "&rows=5&select=DOI,title,author,container-title,issued,is-referenced-by-count,volume,issue,page,type")
    d = fetch(url)
    items = ((d.get("message") or {}).get("items") or [])
    best = None
    for it in items:
        t = clean((it.get("title") or [""])[0])
        sim = difflib.SequenceMatcher(None, norm(title), norm(t)).ratio()
        fam = " ".join((a.get("family") or "") for a in (it.get("author") or [])[:3]).lower()
        bonus = 0.12 if hint.lower().replace("-", " ") in fam.replace("-", " ") else 0.0
        y = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
        ybonus = 0.06 if (year and y and abs(int(y) - int(year)) <= 1) else 0.0
        score = sim + bonus + ybonus
        if best is None or score > best[0]:
            best = (score, it, sim, y)
    if not best or best[2] < 0.72:
        return {"topic": topic, "title": title, "hint": hint, "year": year,
                "status": "unmatched", "best_sim": round(best[2], 3) if best else 0}
    score, it, sim, y = best
    ct = (it.get("container-title") or [""])
    au = []
    for a in (it.get("author") or [])[:5]:
        nm = " ".join(x for x in [a.get("given"), a.get("family")] if x)
        if nm:
            au.append(nm)
    return {
        "topic": topic,
        "status": "ok",
        "sim": round(sim, 3),
        "doi": (it.get("DOI") or "").lower(),
        "title": clean((it.get("title") or [""])[0]),
        "venue": ct[0] if ct else "",
        "year": y,
        "volume": it.get("volume"),
        "issue": it.get("issue"),
        "page": it.get("page"),
        "cites": it.get("is-referenced-by-count", 0),
        "authors": au,
        "type": it.get("type"),
    }


def main():
    res = []
    for i, (topic, title, hint, year) in enumerate(TARGETS):
        r = verify(topic, title, hint, year)
        r["q_title"] = title
        r["q_hint"] = hint
        res.append(r)
        flag = "OK " if r["status"] == "ok" else "MISS"
        print("%s [%s] %s | %s" % (flag, topic, title[:62],
                                   (r.get("venue") or "")[:34] if r["status"] == "ok" else r.get("best_sim")),
              flush=True)
        time.sleep(0.24)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    ok = sum(1 for r in res if r["status"] == "ok")
    print("VERIFIED %d / %d -> %s" % (ok, len(res), OUT))


if __name__ == "__main__":
    main()
