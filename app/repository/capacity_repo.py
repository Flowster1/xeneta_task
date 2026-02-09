from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date
import logging

logger = logging.getLogger(__name__)


class CapacityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_weekly_capacity(self, date_from: date, date_to: date):
        logger.info(f"- Fetching capacity from {date_from} to {date_to} -")

        sql = text("""
            WITH latest_departures AS (
                SELECT DISTINCT ON (
                    "SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS",
                    "ORIGIN_SERVICE_VERSION_AND_MASTER",
                    "DESTINATION_SERVICE_VERSION_AND_MASTER"
                )
                    "OFFERED_CAPACITY_TEU" AS capacity,
                    "ORIGIN_AT_UTC" AS departure_time
                FROM sailing_level
                WHERE "ORIGIN_AT_UTC" BETWEEN :start_date AND :end_date
                ORDER BY
                    "SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS",
                    "ORIGIN_SERVICE_VERSION_AND_MASTER",
                    "DESTINATION_SERVICE_VERSION_AND_MASTER",
                    "ORIGIN_AT_UTC" DESC
            )
            SELECT
                DATE(DATE_TRUNC('week', departure_time)) AS week_start_date,
                CAST(EXTRACT(WEEK FROM departure_time) AS INTEGER) AS week_no,
                CAST(SUM(capacity) AS BIGINT) AS offered_capacity_teu
            FROM latest_departures
            GROUP BY week_start_date, week_no
            ORDER BY week_start_date ASC;
        """)

        try:
            result = self.db.execute(sql, {"start_date": date_from, "end_date": date_to})

            rows = result.mappings().all()
            return rows

        except Exception as e:
            logger.error(f"- Error while executin query: {e} -")
            raise e
