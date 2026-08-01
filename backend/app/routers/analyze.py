from __future__ import annotations

import httpx
from fastapi import APIRouter

from app.models.schemas import AnalyzeRequest, AnalyzeResponse, Meta
from app.services import prompt_builder
from app.services.file_selector import select_files
from app.services.gemini_client import generate_analysis
from app.services.github_client import GithubClient, build_raw_url, parse_repo_url

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repo(request: AnalyzeRequest) -> AnalyzeResponse:
    owner, repo = parse_repo_url(request.repo_url)

    async with httpx.AsyncClient(timeout=30.0) as http_client:
        client = GithubClient(http_client)

        repo_info = await client.get_repo_info(owner, repo)
        default_branch = repo_info.get("default_branch", "main")

        tree_entries, truncated = await client.get_tree(owner, repo, default_branch)
        selected_paths = select_files(tree_entries, repo_name=repo)

    file_urls = [
        build_raw_url(owner, repo, default_branch, path) for path in selected_paths
    ]

    prompt = prompt_builder.build_prompt(
        owner=owner,
        repo=repo,
        description=repo_info.get("description"),
        primary_language=repo_info.get("language"),
        tree_entries=tree_entries,
        file_urls=file_urls,
    )

    analysis = await generate_analysis(prompt)

    return AnalyzeResponse(
        summary_overview=analysis.summary_overview,
        summary_detailed=analysis.summary_detailed,
        flowchart=analysis.flowchart,
        diagram=analysis.diagram,
        meta=Meta(
            repo_name=f"{owner}/{repo}",
            primary_language=repo_info.get("language"),
            partial_analysis=truncated,
        ),
    )
