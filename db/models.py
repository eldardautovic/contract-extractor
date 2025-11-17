from sqlmodel import Field, SQLModel

class Extraction(SQLModel, table=True): 
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(index=True)
    created_at: str = Field()
