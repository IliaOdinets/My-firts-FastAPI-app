import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.note import Note
from schemas.note import NoteCreate

async def create_note(db: AsyncSession, note_data: NoteCreate) -> Note:
    db_note = Note(
        id=str(uuid.uuid4()),
        title=note_data.title,
        content=note_data.content
    )
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

async def get_all_notes(db: AsyncSession) -> list[Note]:
    result = await db.execute(select(Note).order_by(Note.created_at.desc()))
    return list(result.scalars().all())

async def get_note_by_id(db: AsyncSession, note_id: str) -> Note | None:
    """Ищет заметку по ID"""
    stmt = select(Note).where(Note.id == note_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_note(db: AsyncSession, note_id: str, note_data: NoteCreate) -> Note | None:
    note = await get_note_by_id(db, note_id)
    if not note:
        return None
    
    note.title = note_data.title # type: ignore
    note.content = note_data.content # type: ignore
    
    await db.commit()
    await db.refresh(note)  
    return note

async def delete_note(db: AsyncSession, note_id: str) -> bool:
    stmt = delete(Note).where(Note.id == note_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0  # type: ignore