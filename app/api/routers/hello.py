# fastAPI
from fastapi import APIRouter, Depends
# Starlette
from starlette import status

# App
from app import schemas
# from app.core.security import validate_key

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.HelloResponse
)
def hello(
        # api_key: str = Depends(validate_key)
) -> schemas.HelloResponse:
    return schemas.HelloResponse(message="Hello World!")


