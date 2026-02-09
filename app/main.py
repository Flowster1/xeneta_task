import logging
from fastapi import FastAPI, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from typing import List
from datetime import date

from app.schemas.capacity_response import WeeklyCapacityResponse
from app.services.capacity_service import CapacityService
from app.dependencies import get_capacity_service
from app.exceptions.custom_exceptions import DateRangeError


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="- Sailing Capacity API -")


@app.on_event("startup")
async def startup_event():
    logger.info("- Application is starting -")


@app.exception_handler(DateRangeError)
async def date_range_exception_handler(request: Request, exc: DateRangeError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": "INVALID_DATE_RANGE",
            "message": exc.message,
            "help": "Ensure date_from is earlier than or equal to date_to."
        },
    )


@app.get("/capacity", response_model=List[WeeklyCapacityResponse])
def get_capacity(
    date_from: date = Query(..., description="Start date (YYYY-MM-DD)"),
    date_to: date = Query(..., description="End date (YYYY-MM-DD)"),
    service: CapacityService = Depends(get_capacity_service)
):
    logger.info(f"- Received capacity request for range: {date_from} to {date_to} -")
    try:
        result = service.get_capacity_report(date_from, date_to)
        logger.info(f"- Successfully retrieved {len(result)} weekly records -")
        return result
    except Exception as e:
        logger.error(f"- Error processing request: {str(e)} -", exc_info=True)
        raise
