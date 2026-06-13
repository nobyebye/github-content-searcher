import json
import re


DOMAIN_HINTS = [
    (("爬虫", "抓取", "采集", "web scraping", "scraper", "scraping", "crawler", "crawling", "spider"), "网页抓取和爬虫"),
    (("浏览器自动化", "browser automation", "playwright", "selenium", "headless", "headful"), "浏览器自动化"),
    (("知识检索", "rag", "retrieval", "vector", "embedding"), "RAG 和知识检索"),
    (("智能体", "agent", "multi-agent", "ai agent", "llm agent"), "AI Agent 应用开发"),
    (("model context protocol", "mcp"), "MCP 工具和上下文协议"),
    (("数据提取", "内容解析", "extract", "extraction", "parse", "parser", "parsing"), "数据提取和内容解析"),
]


def render_candidates_json(result):
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n"


def recommendation_level(score):
    if score >= 55:
        return "强烈推荐"
    if score >= 35:
        return "可考虑"
    return "谨慎评估"


def infer_domain_summary(repo, requirement):
    requirement_domains = infer_domain_labels(requirement)
    if requirement_domains:
        return "、".join(requirement_domains[:2])

    text = " ".join(
        [
            requirement,
            repo.get("full_name") or "",
            repo.get("description") or "",
            " ".join(repo.get("topics") or []),
        ]
    ).lower()
    domains = infer_domain_labels(text)

    if domains:
        return "、".join(domains[:3])

    language = repo.get("language", "Unknown")
    return f"{language} 工程实践"


def infer_domain_labels(text):
    normalized_text = text.lower()
    domains = []

    for keywords, label in DOMAIN_HINTS:
        if any(contains_keyword(normalized_text, keyword) for keyword in keywords):
            domains.append(label)

    return list(dict.fromkeys(domains))


def contains_keyword(text, keyword):
    normalized_keyword = keyword.lower()
    if re.fullmatch(r"[a-z0-9-]+", normalized_keyword):
        return re.search(rf"(?<![a-z0-9-]){re.escape(normalized_keyword)}(?![a-z0-9-])", text) is not None

    return normalized_keyword in text


def infer_capability_summary(repo, requirement, primary_domain):
    text = " ".join(
        [
            requirement,
            repo.get("full_name") or "",
            repo.get("description") or "",
            " ".join(repo.get("topics") or []),
        ]
    )
    secondary_domains = [
        label
        for label in infer_domain_labels(text)
        if label not in primary_domain
    ]
    if "网页抓取和爬虫" in primary_domain:
        secondary_domains = [
            label
            for label in secondary_domains
            if label in {"浏览器自动化", "数据提取和内容解析"}
        ]

    secondary_domains = secondary_domains[:2]

    if not secondary_domains:
        return ""

    return f" 项目描述还显示它可能涉及{'、'.join(secondary_domains)}能力。"


def project_summary_points(repo, requirement):
    description = repo.get("description") or "该项目没有提供描述，需要进一步阅读 README 判断具体用途。"
    language = repo.get("language", "Unknown")
    stars = repo.get("stars", 0)
    license_name = repo.get("license", "Unknown")
    score = repo.get("score", 0)
    domain_summary = infer_domain_summary(repo, requirement)
    capability_summary = infer_capability_summary(repo, requirement, domain_summary)

    what_it_is = f"这是一个面向{domain_summary}的 {language} 项目。仓库描述是：{description}"
    problem_solved = f"它主要解决{domain_summary}场景下的学习参考、方案选型和二次开发起点问题。{capability_summary}"
    conclusion = (
        f"综合评分 {score}，Stars {stars}，许可证 {license_name}；"
        f"建议作为“{recommendation_level(score)}”候选继续查看 README、examples 和 issues。"
    )

    return what_it_is, problem_solved, conclusion


def short_date(value):
    if not value:
        return "Unknown"

    return value[:10]


def recommendation_reason(repo, requirement):
    domain_summary = infer_domain_summary(repo, requirement)
    language = repo.get("language", "Unknown")
    score = repo.get("score", 0)
    stars = repo.get("stars", 0)

    return f"{language} 项目，匹配{domain_summary}，评分 {score}，Stars {stars}"


def readme_analysis(repo, requirement):
    description = repo.get("description") or "仓库描述为空，需要打开 README 判断项目定位。"
    domain_summary = infer_domain_summary(repo, requirement)

    return (
        f"README 应优先确认它是否真的围绕“{requirement}”提供安装、示例和核心能力说明。"
        f"从仓库描述看，它当前更像是{domain_summary}方向的项目：{description}"
    )


def suitable_users(repo, requirement):
    language = repo.get("language", "Unknown")
    domain_summary = infer_domain_summary(repo, requirement)

    return f"适合想用 {language} 学习、对比或二次开发{domain_summary}项目的人，尤其适合围绕“{requirement}”做选型。"


def getting_started(repo):
    return (
        "先看 README 的安装命令和 Quick Start，再找 examples、docs 或 demo；"
        "如果 10 分钟内找不到最小可运行示例，就把它降一级评估。"
    )


def risk_summary(repo):
    license_name = repo.get("license", "Unknown")
    open_issues = repo.get("open_issues", "Unknown")
    updated_at = short_date(repo.get("updated_at"))

    return f"许可证：{license_name}；开放 issue：{open_issues}；最近推送：{updated_at}。还要检查 README 是否过时、示例是否能跑通。"


def render_recommendations_markdown(candidates, requirement, top=5):
    sorted_candidates = sorted(
        candidates,
        key=lambda item: item.get("score", 0),
        reverse=True,
    )[:top]
    lines = [
        "# GitHub Content Recommendations",
        "",
        f"需求：{requirement}",
        "",
    ]

    if not sorted_candidates:
        lines.extend(
            [
                "没有找到合适候选项目。",
                "",
                "下一步：放宽关键词、降低 star 要求，或增加同义词重新搜索。",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "## Top 项目总览",
            "",
            "| 排名 | 项目 | Stars | 最近推送 | 推荐理由 |",
            "|---:|---|---:|---|---|",
        ]
    )

    for index, repo in enumerate(sorted_candidates, start=1):
        lines.append(
            "| {index} | [{name}]({url}) | {stars} | {updated} | {reason} |".format(
                index=index,
                name=repo["full_name"],
                url=repo["html_url"],
                stars=repo.get("stars", 0),
                updated=short_date(repo.get("updated_at")),
                reason=recommendation_reason(repo, requirement),
            )
        )

    lines.extend(["", "## Top 5 深度分析", ""])

    for index, repo in enumerate(sorted_candidates, start=1):
        score = repo.get("score", 0)
        what_it_is, problem_solved, conclusion = project_summary_points(repo, requirement)
        lines.extend(
            [
                f"## Top {index}: {repo['full_name']}",
                "",
                f"- URL: {repo['html_url']}",
                f"- 推荐等级：{recommendation_level(score)}",
                f"- Stars: {repo.get('stars', 0)}",
                f"- Language: {repo.get('language', 'Unknown')}",
                f"- Updated: {repo.get('updated_at') or 'Unknown'}",
                f"- Score: {score}",
                f"- README 分析：{readme_analysis(repo, requirement)}",
                f"- 主要是什么东西：{what_it_is}",
                f"- 解决了什么问题：{problem_solved}",
                f"- 主要的结论：{conclusion}",
                f"- 适合谁：{suitable_users(repo, requirement)}",
                f"- 怎么上手：{getting_started(repo)}",
                f"- 风险是什么：{risk_summary(repo)}",
                "",
            ]
        )

    return "\n".join(lines)
