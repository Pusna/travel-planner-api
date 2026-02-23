from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app import models, schemas, api_chicago


async def create_project(db: AsyncSession, project: schemas.ProjectCreate):
    if project.places and len(project.places) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 places allowed")

    new_project = models.Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date
    )

    if project.places:
        seen_external_ids = set()
        for p_schema in project.places:
            if p_schema.external_id in seen_external_ids:
                raise HTTPException(status_code=400, detail=f"Duplicate place ID: {p_schema.external_id}")

            if not await api_chicago.validate_external_place(p_schema.external_id):
                raise HTTPException(status_code=400,
                                    detail=f"Place {p_schema.external_id} not found in Art Institute API")

            seen_external_ids.add(p_schema.external_id)

            new_place = models.Place(**p_schema.model_dump())
            new_project.places.append(new_place)

    db.add(new_project)
    await db.commit()

    query = (
        select(models.Project)
        .where(models.Project.id == new_project.id)
        .options(selectinload(models.Project.places))
    )
    result = await db.execute(query)

    return result.scalar_one()


async def get_projects(db: AsyncSession):
    result = await db.execute(select(models.Project).options(selectinload(models.Project.places)))
    return result.scalars().all()


async def delete_project(db: AsyncSession, project_id: int):
    query = select(models.Project).where(models.Project.id == project_id).options(selectinload(models.Project.places))
    result = await db.execute(query)

    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for place in project.places:
        if place.is_visited:
            raise HTTPException(status_code=400, detail="Cannot delete project with visited places")

    await db.delete(project)
    await db.commit()
    return {"message": "Project deleted"}



async def add_place_to_project(db: AsyncSession, project_id: int, place_data: schemas.PlaceCreate):
    query = select(models.Project).where(models.Project.id == project_id).options(selectinload(models.Project.places))
    result = await db.execute(query)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if len(project.places) >= 10:
        raise HTTPException(status_code=400, detail="Project already has 10 places")

    for existing_place in project.places:
        if existing_place.external_id == place_data.external_id:
            raise HTTPException(status_code=400, detail="Place already added to this project")

    if not await api_chicago.validate_external_place(place_data.external_id):
        raise HTTPException(status_code=400, detail="Invalid External ID")

    new_place = models.Place(**place_data.model_dump(), project_id=project_id)
    db.add(new_place)
    await db.commit()
    await db.refresh(new_place)
    return new_place


async def get_project_by_id(db: AsyncSession, project_id: int):
    stmt = select(models.Project).where(models.Project.id == project_id).options(selectinload(models.Project.places))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_place(db: AsyncSession, place_id: int, place_data: schemas.PlaceUpdate):
    stmt = select(models.Place).where(models.Place.id == place_id)
    result = await db.execute(stmt)
    db_place = result.scalar_one_or_none()

    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")

    update_data = place_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_place, key, value)

    await db.commit()
    await db.refresh(db_place)
    return db_place