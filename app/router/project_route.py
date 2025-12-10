from typing import Optional
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Header,
    File,
    Request,
    UploadFile,
    Form,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.core import get_db
from app.auth.deps import get_current_user
from fastapi.responses import HTMLResponse
from app.crud import (
    get_project_by_id,
    create_project,
    update_project,
    delete_project,
    get_projects,
)
from app.models import Project, User
from app.schemas.project import ProjectCreate, ProjectRead
from fastapi.templating import Jinja2Templates


project_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@project_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@project_router.get("/projects", response_class=HTMLResponse)
async def list_projects(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    projects = await get_projects(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        request=request, name="project.html", context={"projects": projects}
    )


@project_router.post("/projects", response_class=HTMLResponse)
async def add_project(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    url: Optional[str] = Form(None),
    github_repo: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    project_in = ProjectCreate(
        name=name,
        description=description,
        url=url,
        github_repo=github_repo,
    )

    new_project = await create_project(db, project_in, image)

    return templates.TemplateResponse(
        request=request, name="project.html", context={"new_projects": new_project}
    )
