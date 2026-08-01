from app.services.file_selector import select_files
from app.services.github_client import TreeEntry, build_raw_url, parse_repo_url


def test_parse_repo_url_valid():
    assert parse_repo_url("https://github.com/octocat/Hello-World") == (
        "octocat",
        "Hello-World",
    )
    assert parse_repo_url("https://github.com/octocat/Hello-World/") == (
        "octocat",
        "Hello-World",
    )
    assert parse_repo_url("https://github.com/octocat/Hello-World.git") == (
        "octocat",
        "Hello-World",
    )


def test_parse_repo_url_invalid():
    import pytest

    from app.exceptions import InvalidUrlError

    with pytest.raises(InvalidUrlError):
        parse_repo_url("not-a-url")

    with pytest.raises(InvalidUrlError):
        parse_repo_url("https://gitlab.com/owner/repo")


def test_select_files_prioritizes_readme_and_entrypoints():
    entries = [
        TreeEntry(path="README.md", type="blob", size=500),
        TreeEntry(path="main.py", type="blob", size=1000),
        TreeEntry(path="node_modules/foo/index.js", type="blob", size=2000),
        TreeEntry(path="src/deep/nested/module.py", type="blob", size=300),
        TreeEntry(path="assets/logo.png", type="blob", size=50_000),
        TreeEntry(path="package-lock.json", type="blob", size=100_000),
    ]

    selected = select_files(entries, repo_name="example")

    assert "README.md" in selected
    assert "main.py" in selected
    assert "node_modules/foo/index.js" not in selected
    assert "assets/logo.png" not in selected
    assert "package-lock.json" not in selected
    assert selected.index("README.md") < selected.index("src/deep/nested/module.py")


def test_select_files_respects_max_files(monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "max_files_to_analyze", 2)
    entries = [
        TreeEntry(path=f"src/file{i}.py", type="blob", size=100)
        for i in range(10)
    ]

    selected = select_files(entries, repo_name="example")

    assert len(selected) == 2


def test_build_raw_url():
    assert build_raw_url("octocat", "Hello-World", "main", "src/app.py") == (
        "https://raw.githubusercontent.com/octocat/Hello-World/main/src/app.py"
    )
