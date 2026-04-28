from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.note import Note
from schemas.note import NoteCreate

async def create_note(db: AsyncSession, note_data: NoteCreate) -> Note:
    db_note = Note(**note_data.model_dump())
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

async def get_all_notes(db: AsyncSession) -> list[Note]:
    result = await db.execute(select(Note).order_by(Note.created_at.desc()))
    return list(result.scalars().all())

async def get_note_by_id(db: AsyncSession, note_id: str) -> Note | None:
    result = await db.execute(select(Note).where(Note.id == note_id))
    return result.scalar_one_or_none()

async def delete_note_by_id(db: AsyncSession, note_id: str) ->  None:
    await db.execute(delete(Note).where(Note.id == note_id))