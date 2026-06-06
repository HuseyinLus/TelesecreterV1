from pydantic import BaseModel


class UpdateDepartmentRequest(BaseModel):
    name: str
