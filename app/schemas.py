from pydantic import BaseModel

class Symbol(BaseModel):
    id: int
    description: str
    image_url: str
