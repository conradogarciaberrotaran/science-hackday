from pydantic import BaseModel

class ProcedureResponse(BaseModel):
    city: str
    ruca: str
    procedure_code: str
    quantity: int
