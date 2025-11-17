from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db.database import SessionDep
from db.models import Extraction

router = APIRouter(prefix="/extractions", tags=["Extractions"])

@router.get("/", response_model=List[Extraction])
async def read_extractions(session: SessionDep):
    return session.exec(select(Extraction)).all()

@router.get("/{extraction_id}", response_model=Extraction)
async def read_extraction(extraction_id: int, session: SessionDep):
    extraction = session.get(Extraction, extraction_id)
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")
    return extraction

@router.post("/upload")
async def upload_extraction():
    return [{"username": "Rick"}, {"username": "Morty"}]