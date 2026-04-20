from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="My first API")
notes: dict[str, "Note"] = {}

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Заголовок заметки")
    content: str = Field(..., min_length=1, max_length=1000, description="Текст заметки")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Note(NoteCreate):
     id: str

@app.get("/", tags=["Root"])
def read_root() -> dict[str,str]:
    return {"message": "FastApi is working"}

@app.get("/notes/", tags=["Notes"], response_model=list[Note])
def get_all_notes() -> list[Note]:
        return list(notes.values())

@app.get("/notes/{notes_id}", tags=["Notes"], response_model=Note)
def get_note(note_id: str) -> Note:
    note = notes.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.post("/notes/", tags=["Notes"], response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate) -> Note:
    note_id = str(len(notes) + 1)
    new_note = Note(id=note_id, **note.model_dump())
    notes[note_id] = new_note
    return new_note

@app.put("/notes/{notes_id}", tags=["Notes"], response_model=Note)
def update_note(note_id: str, note_update:NoteCreate) -> Note:
    if note_id not in notes:
         raise HTTPException(status_code=404, detail="Note not found")
    updated = Note(id=note_id, **note_update.model_dump())
    notes[note_id] = updated
    return updated 

@app.delete("/notes/{notes_id}", tags=["Notes"], status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str) -> None:
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    del notes[note_id]