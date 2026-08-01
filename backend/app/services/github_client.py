from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

from app.config import settings
from app.exceptions import GithubRateLimitError, InvalidUrlError, RepoNotFoundError

GITHUB_API_BASE = "https://api.github.com"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

REPO_URL_PATTERN = re.compile(
    r"^https?://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+?)(?:\.git)?/?$"
)


@dataclass
class TreeEntry:
    path: str
    type: str  # "blob" ou "tree"
    size: int | None


def parse_repo_url(url: str) -> tuple[str, str]:
    match = REPO_URL_PATTERN.match(url.strip())
    if not match:
        raise InvalidUrlError(
            "URL inválida. Use o formato https://github.com/owner/repo."
        )
    return match.group("owner"), match.group("repo")


def build_raw_url(owner: str, repo: str, branch: str, path: str) -> str:
    return f"{GITHUB_RAW_BASE}/{owner}/{repo}/{branch}/{path}"


def _auth_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    return headers


def _format_reset_wait(reset_header: str | None) -> str:
    if not reset_header:
        return "Tente novamente em alguns minutos."
    reset_at = datetime.fromtimestamp(int(reset_header), tz=timezone.utc)
    wait_minutes = max(0, round((reset_at - datetime.now(timezone.utc)).total_seconds() / 60))
    local_time = reset_at.astimezone().strftime("%H:%M")
    return f"Tente novamente em ~{wait_minutes} min (por volta de {local_time})."


def _raise_for_github_error(response: httpx.Response) -> None:
    if response.status_code == 404:
        raise RepoNotFoundError("Repositório não encontrado ou privado.")
    if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
        wait_message = _format_reset_wait(response.headers.get("X-RateLimit-Reset"))
        raise GithubRateLimitError(
            f"Limite de requisições públicas do GitHub atingido (60/hora). {wait_message}"
        )
    response.raise_for_status()


class GithubClient:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def get_repo_info(self, owner: str, repo: str) -> dict:
        response = await self._client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}", headers=_auth_headers()
        )
        _raise_for_github_error(response)
        return response.json()

    async def get_tree(self, owner: str, repo: str, sha: str) -> tuple[list[TreeEntry], bool]:
        response = await self._client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{sha}",
            params={"recursive": "1"},
            headers=_auth_headers(),
        )
        _raise_for_github_error(response)
        data = response.json()
        entries = [
            TreeEntry(path=item["path"], type=item["type"], size=item.get("size"))
            for item in data.get("tree", [])
        ]
        return entries, bool(data.get("truncated", False))
