from fastapi import FastAPI
from routers import extractions
from db.database import create_db_and_tables
from contextlib import asynccontextmanager

#Creating table if it doesnt exist
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()    
    yield

#Initializing the App
app = FastAPI(lifespan=lifespan)

#Including the extractions router
app.include_router(extractions.router)


