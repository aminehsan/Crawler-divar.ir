from pydantic import BaseModel


class Input(BaseModel):
    url: str
