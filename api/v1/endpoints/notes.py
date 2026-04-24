from fastapi import APIRouter, Depends, status
from schemas.note import NoteInDB, NoteCreate
from core.dependencies import get_note_or_404
from services.note_service import notes # type: ignore

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/", response_model=list[NoteInDB])
def get_all_notes() -> list[NoteInDB]:
        return list(notes.values()) # type: ignore

@router.get("/{note_id}", response_model=NoteInDB)
def get_note(note: NoteInDB = Depends(get_note_or_404)):
    return note

@router.post("/", response_model=NoteInDB, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> NoteInDB:
    note_id = str(len(notes) + 1) # type: ignore
    new_note = NoteInDB(id=note_id, **note.model_dump())
    notes[note_id] = new_note
    return new_note

@router.put("{note_id}", response_model=NoteInDB)
def update_note(note_id: str, note_update:NoteCreate, note: NoteInDB = Depends(get_note_or_404)) -> NoteInDB:
    updated = NoteInDB(id=note_id, **note_update.model_dump(), created_at=note.created_at)
    notes[note_id] = updated
    return updated 

@router.delete("{note_id}")
def delete_note(note_id: str, note: NoteInDB = Depends(get_note_or_404)) -> None:
    del notes[note_id]