from datetime import datetime, timezone
from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Заголовок заметки")
    content: str = Field(..., min_length=1, max_length=1000, description="Текст заметки")

    @field_validator("title")
    @classmethod
    def title_must_not_be_spam(cls, v:str) -> str:
        spam_words = ["казино", "крипта", "бесплатно"]
        if any(word in v.lower() for word in spam_words):
            raise ValueError("Заголовок содержит запрещенные слова")
        return v.strip().title()

    @model_validator(mode="after")
    def check_content_not_duplicates_title(self) -> Self:
        if self.content.lower().strip() == self.title.lower().strip():
            raise ValueError("Содержимое не должно дублировать заголовок")
        return self

class NoteInDB(NoteCreate):
    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True