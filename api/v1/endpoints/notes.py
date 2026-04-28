from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.note import NoteInDB, NoteCreate
from core.dependencies import get_db 
from services import note_service

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/", response_model=list[NoteInDB])
async def get_all_notes(db:AsyncSession = Depends(get_db)):
    return await note_service.get_all_notes(db)

@router.get("/{note_id}", response_model=NoteInDB)
async def get_note(note_id: str, db: AsyncSession = Depends(get_db)):
    return await note_service.get_note_by_id(db, note_id)

@router.post("/", response_model=NoteInDB, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    return await note_service.create_note(db, note)

@router.delete("{note_id}")
async def delete_note(note_id: str, db: AsyncSession = Depends(get_db)):
    await note_service.delete(db, note_id)