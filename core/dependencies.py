from typing import Annotated

from fastapi import Depends, HTTPException, status
from schemas.note import NoteInDB

async def get_note_or_404(note_id: str) -> NoteInDB:
    from services.note_service import notes # type: ignore
    note = notes.get(note_id) # type: ignore
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note # type: ignore

NoteIDDep = Annotated[str, Depends(get_note_or_404)]