from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository.capacity_repo import CapacityRepository
from app.services.capacity_service import CapacityService


def get_capacity_service(db: Session = Depends(get_db)) -> CapacityService:
    repo = CapacityRepository(db)
    return CapacityService(repo)
