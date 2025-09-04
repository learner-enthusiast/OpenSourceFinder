import os
from dotenv import load_dotenv
from fastapi import HTTPException
import httpx
from app.utils.utils import ProjectFilters

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
BASE_URL = "https://api.github.com/search/repositories"


async def search_repositories(filters: dict):
    """
    filters can include{
      "language": "Python",
        "stars": ">500",
        "created": "2025-08-01",
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
        "page": 1
    }
    """
    query_parts = ["is:public"]
    if filters.get("stars"):
        query_parts.append(f"stars:>={filters['stars']}")
    if filters.get("created"):
        query_parts.append(f"created:>{filters['created']}")
    if filters.get("language"):
        query_parts.append(f"language:{filters['language']}")
    if filters.get("activity"):
        query_parts.append(f"pushed:>{filters['activity']}")
    if filters.get("category"):
        topics = ProjectFilters.get_github_topics(filters["category"])
        if topics:
            query_parts.extend(f"topic:{t}" for t in topics)

    query = " ".join(query_parts)
    params = {
        "q": query,
        "sort": filters.get("sort") or "stars",
        "order": filters.get("order") or "desc",
        "per_page": filters.get("per_page"),
        "page": filters.get("page"),
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Github API Request Failed {e}")
