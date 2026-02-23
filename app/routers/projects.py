from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import crud, schemas, database

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=schemas.ProjectResponse, status_code=201)
async def create_project(project: schemas.ProjectCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_project(db, project)


@router.get("/", response_model=List[schemas.ProjectResponse])
async def list_projects(db: AsyncSession = Depends(database.get_db)):
    return await crud.get_projects(db)


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(database.get_db)):
    project = await crud.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_project(db, project_id)