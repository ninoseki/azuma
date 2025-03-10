from typing import Literal

from pydantic import BaseModel, Field


class Related(BaseModel):
    id: str = Field(...)
    type: Literal["derived", "merged", "renamed", "similar", "obsolete"] = Field(...)
