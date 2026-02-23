from pydantic import BaseModel, Field, computed_field
from typing import List, Optional
from datetime import date


class PlaceBase(BaseModel):
    external_id: str
    notes: Optional[str] = None
    is_visited: bool = False

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None

class PlaceResponse(PlaceBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class ProjectCreate(ProjectBase):
    places: Optional[List[PlaceCreate]] = Field(default=None, max_items=10)

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None

class ProjectResponse(ProjectBase):
    id: int
    places: List[PlaceResponse] = []

    @computed_field
    def is_completed(self) -> bool:
        if not self.places:
            return False

        for place in self.places:
            if not place.is_visited:
                return False

        return True

    class Config:
        from_attributes = True