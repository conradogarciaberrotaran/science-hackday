from abc import ABC

from sqlalchemy import func, select

from app.models import Record, SessionLocal


class BaseRepository(ABC):
    def __init__(self, db_session: SessionLocal):
        self.db_session = db_session


class RecordRepository(BaseRepository):
    def get_by(
        self, min_ruca: float, max_ruca: float, state_abbreviation: str
    ) -> tuple:
        """
        Returns the amount of times a procedure was done on every city of a determined state
        having each city fall in between a RUCA range [min_ruca, max_ruca]
        """
        query = (
            select(
                Record.city,
                Record.ruca,
                Record.procedure_code,
                func.count(Record.procedure_code),
            )
            .where(
                Record.state_abbreviation == state_abbreviation,
                Record.ruca >= min_ruca,
                Record.ruca <= max_ruca,
                Record.country == "US",
            )
            .group_by(Record.city, Record.ruca, Record.procedure_code)
            .order_by(Record.city, Record.procedure_code)
            .limit(10)
        )

        result = self.db_session.execute(query).all()
        return result
