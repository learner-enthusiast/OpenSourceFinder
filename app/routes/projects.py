from fastapi import APIRouter, Depends, Query
from app.controllers.projects import Projects
from app.auth.dependencies import get_current_user
from app.utils.utils import ProjectFilters
from datetime import date

router = APIRouter(
    prefix="/projects", tags=["Repo"], dependencies=[Depends(get_current_user)]
)


@router.get("")
async def get_filtered_projects(
    language: ProjectFilters.Language | None = Query(
        default=list(ProjectFilters.Language)[0], description="Programming language"
    ),
    stars: int | None = Query(None, description="Minimum number of stars"),
    sort: ProjectFilters.SortField | None = Query("stars", description="Sort field"),
    order: ProjectFilters.Order | None = Query("desc", description="Sort order"),
    per_page: int = Query(10, description="Results per page"),
    page: int = Query(1, description="Page number"),
    created: date | None = Query(
        None, description="Repositories created after this date will be visible"
    ),
    activity: date | None = Query(
        None, description="Repositories with activity (last push) after this date"
    ),
    category: str | None = Query(None, description="Insert Project Categories"),
):
    """Get filtered projects"""
    return await Projects.get_projects(
        language=language,
        stars=stars,
        sort=sort,
        order=order,
        per_page=per_page,
        page=page,
        created=created,
        activity=activity,
        category=category,
    )


@router.get("/topWeekly")
async def get_topWeekly(
    language: ProjectFilters.Language | None = Query(
        default=list(ProjectFilters.Language)[0], description="Programming language"
    ),
):
    return await Projects.top_WeeklyProjects(language=language)
