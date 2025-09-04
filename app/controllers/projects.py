from app.utils.utils import ProjectFilters
from fastapi import Query
from app.controllers.github_client import search_repositories
from datetime import date


class Projects:
    @staticmethod
    async def get_projects(
        language: ProjectFilters.Language | None = Query(None),
        stars: int | None = Query(None),
        sort: ProjectFilters.SortField | None = Query("stars"),
        order: ProjectFilters.Order | None = Query("desc"),
        per_page: int = Query(10),
        page: int = Query(1),
        created: date | None = Query(None),
        activity: date | None = Query(None),
        category: ProjectFilters.Category | None = Query(None),
    ):
        return await search_repositories(
            filters={
                "language": language.value if language else None,
                "stars": stars,
                "sort": sort,
                "order": order,
                "per_page": per_page,
                "page": page,
                "created": created.isoformat() if created else None,
                "activity": activity.isoformat() if activity else None,
                "category": category.value if category else None,
            }
        )
