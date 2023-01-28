from pydantic import BaseModel, Field


class LogSource(BaseModel):
    category: str | None = Field(default=None)
    product: str | None = Field(default=None)
    service: str | None = Field(default=None)
    definition: str | None = Field(default=None)
