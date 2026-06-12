import json


def render_candidates_json(result):
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n"


def recommendation_level(score):
    if score >= 55:
        return "强烈推荐"
    if score >= 35:
        return "可考虑"
    return "谨慎评估"


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

    for index, repo in enumerate(sorted_candidates, start=1):
        score = repo.get("score", 0)
        lines.extend(
            [
                f"## {index}. {repo['full_name']}",
                "",
                f"- URL: {repo['html_url']}",
                f"- 推荐等级：{recommendation_level(score)}",
                f"- Stars: {repo.get('stars', 0)}",
                f"- Language: {repo.get('language', 'Unknown')}",
                f"- Updated: {repo.get('updated_at') or 'Unknown'}",
                f"- Score: {score}",
                f"- 适合场景：围绕 `{requirement}` 进一步阅读 README、examples 和 issues。",
                f"- 风险 / Risk: license={repo.get('license', 'Unknown')}, open_issues={repo.get('open_issues', 'Unknown')}.",
                "- 下一步：打开仓库文档，确认安装方式、维护活跃度和最小可运行示例。",
                "",
            ]
        )

    return "\n".join(lines)
