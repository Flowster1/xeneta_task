from datetime import date
from typing import List
from app.repository.capacity_repo import CapacityRepository
from app.exceptions.custom_exceptions import DateRangeError


class CapacityService:
    def __init__(self, repo: CapacityRepository):
        self.repo = repo

    def get_capacity_report(self, date_from: date, date_to: date) -> List[dict]:
        if date_from > date_to:
            raise DateRangeError(f"Start date ({date_from}) cannot be after end date ({date_to}).")

        return self.repo.get_weekly_capacity(date_from, date_to)
