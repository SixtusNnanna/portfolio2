from typing import Optional
from fastapi import File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Sequence, delete, select, update
from app.models import Project, User
from app.schemas.project import ProjectCreate, ProjectRead
from app.utils import media_manager


async def get_project_by_id(db: AsyncSession, project_id: str) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


async def create_project(
    db: AsyncSession, project_in: ProjectCreate, image_file: Optional[UploadFile]
):

    new_project = Project(**project_in.model_dump(), image_url=None)

    db.add(new_project)
    await db.flush()

    image_url = await media_manager.upload_image(image_file, new_project.id)
    new_project.image_url = image_url

    await db.commit()

    return new_project


async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def update_project(db: AsyncSession, project_id: str, project_in: ProjectCreate):
    result = await db.execute(
        update(Project)
        .where(Project.id == project_id)
        .values(**project_in.model_dump(exclude_unset=True))
        .returning(Project)
    )
    await db.commit()
    return result.scalar_one_or_none()


async def delete_project(db: AsyncSession, project_id: str) -> bool:
    result = await db.execute(delete(Project).where(Project.id == project_id))
    await db.commit()
    return result.rowcount > 0
