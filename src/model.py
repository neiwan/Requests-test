from typing import Dict
from pydantic import BaseModel


class CreateNote(BaseModel):
    id: int


class ReadNoteById(BaseModel):
    id: int
    text: str


class GetNoteTimeInfo(BaseModel):
    created_at: str
    updated_at: str


class UpdateNoteText(BaseModel):
    id: int
    text: str


class DeleteNoteById(BaseModel):
    isDelete: bool


class PrintNoteId(BaseModel):
    dict_id: Dict[int, int]
