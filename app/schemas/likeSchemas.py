from pydantic import BaseModel,Field
from typing_extensions import Annotated
from pydantic.types import conint



class Like(BaseModel):
    post_id: int
    dir:  Annotated[int, Field(strict=True, ge=0)]