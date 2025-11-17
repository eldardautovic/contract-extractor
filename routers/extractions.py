from datetime import datetime, timezone
import json
from typing import Generic, List, TypeVar
from fastapi import APIRouter, HTTPException, Query, UploadFile
from openai import OpenAI
from pydantic import BaseModel
from sqlmodel import func, select

from core.config import Settings
from db.database import SessionDep
from db.models import Extraction, ExtractionDetail
from services.prompt import systemPrompt
from services.utils import extract_text_from_pdf

router = APIRouter(prefix="/extractions", tags=["Extractions"])

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"
token = Settings.API_KEY

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

class ExtractionDetailRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

class ExtractionRead(BaseModel):
    id: int
    file_name: str
    created_at: datetime
    details: List[ExtractionDetailRead] = []

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    skip: int
    limit: int
    data: List[T]


@router.get("/", response_model=PaginatedResponse[Extraction])
async def read_extractions(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
):
    # row numbers
    total = session.exec(select(func.count(Extraction.id))).one()

    # statement with pagination
    statement = select(Extraction).offset(skip).limit(limit)
    results = session.exec(statement).all()

    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        data=results
    )

@router.get("/{extraction_id}", response_model=ExtractionRead)
async def read_extraction(extraction_id: int, session: SessionDep):
    #get extraction
    extraction = session.get(Extraction, extraction_id)
    if not extraction:
        raise HTTPException(status_code=404, detail="Extraction not found")

    #get details
    details = session.exec(
        select(ExtractionDetail).where(ExtractionDetail.extraction_id == extraction.id)
    ).all()

    return ExtractionRead(
        id=extraction.id,
        file_name=extraction.file_name,
        created_at=extraction.created_at,
        details=[
            ExtractionDetailRead(
                id=d.id,
                title=d.title,
                content=d.content,
                created_at=d.created_at
            ) for d in details
        ]
    )

@router.post("/upload", response_model=ExtractionRead)
async def upload_extraction(file: UploadFile, session: SessionDep):
    #validate file type
    if(file.content_type != "application/pdf"):
        raise HTTPException(status_code=400, detail="The file is not a pdf.")

    #extract text from pdf
    plainText = extract_text_from_pdf(file)

    # validate non empty file
    if len(plainText) == 0:
        raise HTTPException(status_code=400, detail="The file is empty.")
    
    #call model
    dirtyResponse = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": systemPrompt,
            },
            {
                "role": "user",
                "content": plainText,
            }
        ],
        temperature=1.0,
        top_p=1.0,
        model=model
    )

    #parse response
    response = json.loads(dirtyResponse.choices[0].message.content)

    #store extraction and details in db
    extraction = Extraction(
        file_name=file.filename,
        created_at=datetime.now(timezone.utc)
    )
    session.add(extraction)
    session.commit()
    session.refresh(extraction) 

    for item in response:
        detail = ExtractionDetail(
            extraction_id=extraction.id,
            title=item.get("title") or "",
            content=item.get("text") or item.get("content") or "",
            created_at=datetime.now(timezone.utc)
        )
        session.add(detail)

    session.commit()

    #get
    details = session.exec(
        select(ExtractionDetail).where(ExtractionDetail.extraction_id == extraction.id)
    ).all()

    return ExtractionRead(
        id=extraction.id,
        file_name=extraction.file_name,
        created_at=extraction.created_at,
        details=[
            ExtractionDetailRead(
                id=d.id,
                title=d.title,
                content=d.content,
                created_at=d.created_at
            ) for d in details
        ]
    )