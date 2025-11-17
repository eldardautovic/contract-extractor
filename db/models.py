from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Extraction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_name: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    details: List["ExtractionDetail"] = Relationship(back_populates="extraction")


class ExtractionDetail(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    extraction_id: int = Field(foreign_key="extraction.id")
    title: str = Field(index=True)
    content: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    extraction: Optional[Extraction] = Relationship(back_populates="details")
