from pydantic import BaseModel


class AddDepartmentRequest(BaseModel):
    name: str
