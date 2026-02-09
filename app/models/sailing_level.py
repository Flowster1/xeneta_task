from sqlalchemy import Column, String, DateTime, Index, Integer
from sqlalchemy.sql import text

from app.database import Base


class SailingLevel(Base):
    __tablename__ = 'sailing_level'

    __table_args__ = (
        Index(
            'idx_latest_sailing',
            "SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS",
            "ORIGIN_SERVICE_VERSION_AND_MASTER",
            "DESTINATION_SERVICE_VERSION_AND_MASTER",
            "ORIGIN_AT_UTC",
        ),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_version_and_roundtrip_identfiers = Column("SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS", String)
    origin_service_version_and_master = Column("ORIGIN_SERVICE_VERSION_AND_MASTER", String)
    destination_service_version_and_master = Column("DESTINATION_SERVICE_VERSION_AND_MASTER", String)
    origin_at_utc = Column("ORIGIN_AT_UTC", DateTime)
    origin = Column("ORIGIN", String)
    destination = Column("DESTINATION", String)
    origin_port_code = Column("ORIGIN_PORT_CODE", String)
    destination_port_code = Column("DESTINATION_PORT_CODE", String)
    offered_capacity_teu = Column("OFFERED_CAPACITY_TEU", Integer)

    __table_args__ = (
        Index(
            'idx_latest_sailing',
            "SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS",
            "ORIGIN_SERVICE_VERSION_AND_MASTER",
            "DESTINATION_SERVICE_VERSION_AND_MASTER",
            text('"ORIGIN_AT_UTC" DESC')
        ),
    )
