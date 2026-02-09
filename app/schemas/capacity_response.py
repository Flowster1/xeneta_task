from pydantic import BaseModel, ConfigDict
from datetime import date


class WeeklyCapacityResponse(BaseModel):
    week_start_date: date
    week_no: int
    offered_capacity_teu: int

    model_config = ConfigDict(from_attributes=True)
