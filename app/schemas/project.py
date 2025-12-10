# app/schemas/project.py
from pydantic import BaseModel, HttpUrl, computed_field
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    name: str
    description: str
    url: Optional[str] = None
    github_repo: Optional[str] = None


class ProjectRead(BaseModel):
    id: str
    name: str
    description: str
    image_url: str       
    url: str
    github_repo: str
    created_at: datetime
   

    @computed_field
    @property
    def created_at_iso(self) -> str:
        return self.created_at.isoformat(timespec="seconds")

    model_config = {"from_attributes": True}