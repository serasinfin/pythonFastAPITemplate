# Pydantic
from pydantic import BaseModel
# App schemas


class HelloResponse(BaseModel):
    message: str
