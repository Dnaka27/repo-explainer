from __future__ import annotations

import posixpath

from app.config import settings
from app.services.github_client import TreeEntry

NOISE_DIR_SEGMENTS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "vendor",
    ".venv",
    "venv",
    "__pycache__",
    ".next",
    ".nuxt",
    "target",
    "bin",
    "obj",
    "coverage",
}
NOISE_FILE_NAMES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Cargo.lock",
}
NOISE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp",
    ".woff", ".woff2", ".ttf", ".eot",
    ".mp4", ".mov", ".zip", ".tar", ".gz", ".pdf",
    ".lock", ".map", ".min.js", ".min.css",
}

ROOT_CONFIG_FILES = {
    "package.json", "pyproject.toml", "requirements.txt", "pipfile",
    "go.mod", "cargo.toml", "composer.json", "pom.xml", "build.gradle",
}
README_NAMES = {"readme.md", "readme.rst", "readme", "readme.txt"}
ENTRYPOINT_NAMES = {
    "main.py", "app.py", "manage.py", "index.js", "index.ts", "index.jsx", "index.tsx",
    "server.js", "server.ts", "main.go", "main.rs",
}
SHALLOW_DIRS = {"src", "app", "lib", "cmd"}


def _is_noise(path: str, size: int | None) -> bool:
    parts = path.split("/")
    if any(part in NOISE_DIR_SEGMENTS for part in parts[:-1]):
        return True
    name = parts[-1]
    if name in NOISE_FILE_NAMES:
        return True
    ext = posixpath.splitext(name)[1].lower()
    if ext in NOISE_EXTENSIONS:
        return True
    if size is not None and size > settings.max_file_size_bytes:
        return True
    return False


def _score(entry: TreeEntry, repo_name: str) -> int:
    parts = entry.path.split("/")
    name = parts[-1].lower()
    depth = len(parts) - 1

    if depth == 0 and name in README_NAMES:
        return 100
    if depth == 0 and name in ROOT_CONFIG_FILES:
        return 90
    if name in ENTRYPOINT_NAMES:
        return 80
    if depth <= 2 and parts[0].lower() in SHALLOW_DIRS:
        return 50
    if posixpath.splitext(name)[0] == repo_name.lower():
        return 45
    return max(10 - depth, 1)


def select_files(entries: list[TreeEntry], repo_name: str) -> list[str]:
    """Aplica a heurística de scoring/filtragem e retorna os paths selecionados,
    respeitando MAX_FILES_TO_ANALYZE e MAX_TOTAL_PROMPT_BYTES."""
    candidates = [
        entry
        for entry in entries
        if entry.type == "blob" and not _is_noise(entry.path, entry.size)
    ]
    scored = sorted(
        candidates,
        key=lambda e: (
            -_score(e, repo_name),
            len(e.path.split("/")),
            -(e.size or 0),
            e.path,
        ),
    )

    selected: list[str] = []
    total_bytes = 0
    for entry in scored:
        if len(selected) >= settings.max_files_to_analyze:
            break
        projected_size = min(entry.size or 0, settings.max_file_size_bytes)
        if total_bytes + projected_size > settings.max_total_prompt_bytes:
            break
        selected.append(entry.path)
        total_bytes += projected_size

    return selected
