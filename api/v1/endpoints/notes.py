# api/v1/endpoints/notes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db, get_current_user
from services import note_service
from schemas.note import NoteCreate, NoteInDB

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=list[NoteInDB])
async def get_all_notes(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Получить все заметки текущего пользователя"""
    return await note_service.get_all_notes(db)


@router.post("/", response_model=NoteInDB, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Создать новую заметку"""
    return await note_service.create_note(db, note_data)


@router.get("/{note_id}", response_model=NoteInDB)
async def get_note(
    note_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Получить заметку по ID"""
    note = await note_service.get_note_by_id(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteInDB)
async def update_note(
    note_id: str,
    note_data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Полностью обновить заметку"""
    updated = await note_service.update_note(db, note_id, note_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Удалить заметку"""
    is_deleted = await note_service.delete_note(db, note_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Note not found")