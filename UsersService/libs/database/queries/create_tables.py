import logging

from models.database_models import Base
from libs.database.database_management import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables() -> None:
    logger.info("Creating tables")
    Base.metadata.create_all(engine)