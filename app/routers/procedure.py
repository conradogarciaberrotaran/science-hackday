from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.data_models import ProcedureResponse
from app.dependencies import get_db
from app.repository import RecordRepository

api = APIRouter()


class QueryParameters:
    def __init__(
        self,
        min_ruca: float = Query(..., min=1.0, example="1.0"),
        max_ruca: float = Query(..., example="2.0"),
        state_abbreviation: str = Query(..., example="CA"),
    ):
        self.min_ruca = min_ruca
        self.max_ruca = max_ruca
        self.state_abbreviation = state_abbreviation


@api.get("/", response_model=List[ProcedureResponse])
def get_procedure_codes(db=Depends(get_db), parameters: QueryParameters = Depends()):
    if parameters.min_ruca > parameters.max_ruca:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="min_ruca must be less or equal than max_ruca",
        )

    records = RecordRepository(db).get_by(
        min_ruca=parameters.min_ruca,
        max_ruca=parameters.max_ruca,
        state_abbreviation=parameters.state_abbreviation,
    )

    response = [
        {
            "city": city,
            "ruca": ruca,
            "procedure_code": procedure_code,
            "quantity": quantity,
        }
        for city, ruca, procedure_code, quantity in records
    ]

    return response
