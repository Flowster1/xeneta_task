import pandas as pd
from app.database import engine, Base
import os
import logging

from app.models.sailing_level import SailingLevel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("populate_db")


def populate_db():
    logger.info("- Starting to populate the database -")

    try:
        logger.info("- Creating database tables -")
        Base.metadata.create_all(bind=engine)

        csv_path = os.path.join("data", "sailing_level_raw.csv")
        if not os.path.exists(csv_path):
            logger.error(f"- CSV not found at: {csv_path} -")
            return

        logger.info(f"- Reading CSV from {csv_path} -")
        df = pd.read_csv(csv_path)

        row_count = len(df)
        logger.info(f"- CSV loaded successfully. Found {row_count} rows -")

        if "ORIGIN_AT_UTC" in df.columns:
            df['ORIGIN_AT_UTC'] = pd.to_datetime(df["ORIGIN_AT_UTC"])
            logger.debug("- Converted ORIGIN_AT_UTC to datetime objects -")

        logger.info("- Inserting data into SQL -")
        df.to_sql(
            'sailing_level',
            con=engine,
            if_exists='append',
            index=False,
            chunksize=1000
        )
        logger.info("- Populating database completed successfully! -")

    except Exception as e:
        logger.critical(f"- Populating database failed: {e} -", exc_info=True)


if __name__ == "__main__":
    populate_db()
