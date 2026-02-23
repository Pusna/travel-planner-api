from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, database

router = APIRouter(tags=["Places"])


@router.post("/projects/{project_id}/places", response_model=schemas.PlaceResponse)
async def add_place_to_project(
    project_id: int,
    place: schemas.PlaceCreate,
    db: AsyncSession = Depends(database.get_db)
):
    return await crud.add_place_to_project(db, project_id, place)


@router.patch("/places/{place_id}", response_model=schemas.PlaceResponse)
async def update_place(
    place_id: int,
    place_data: schemas.PlaceUpdate,
    db: AsyncSession = Depends(database.get_db)
):
    return await crud.update_place(db, place_id, place_data)