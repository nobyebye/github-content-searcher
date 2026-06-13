from pathlib import Path


def test_daily_catalog_workflow_exists():
    workflow = Path(".github/workflows/update-catalog.yml").read_text(encoding="utf-8")

    assert "schedule:" in workflow
    assert "github-content-searcher catalog" in workflow
    assert "data/catalog.json" in workflow
    assert "docs/index.html" in workflow
