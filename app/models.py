# Create a basic model for the FastAPI

from pydantic import BaseModel

class Query(BaseModel):
    query: str
    neighbours: int = 3

