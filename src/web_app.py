import datetime
import os
import fastapi
from fastapi import HTTPException
from model import CreateNote, ReadNoteById, GetNoteTimeInfo, UpdateNoteText, PrintNoteId, DeleteNoteById

api_router = fastapi.APIRouter()
local_path = "D:\\CODE\\Python\\IVOLab4\\"

path = local_path + "notes\\"
token_path = local_path + "token1.txt"

id_count = len(os.listdir(path))


def get_full_path(id):
    return path + "\\" + str(id) + ".txt"


def get_access_by_token(actual_token):
    file = open(token_path)
    expected_token = file.read()
    file.close()
    if expected_token == actual_token:
        return
    else:
        raise HTTPException(status_code=401, detail="Wrong token")


@api_router.post("/create_note", response_model=CreateNote)
def create_note(token: str):
    """
        Метод создаёт заметку
    """
    global id_count
    id_count += 1
    id = id_count

    get_access_by_token(token)

    if not os.path.isfile(get_full_path(id)):
        file = open(get_full_path(id), "w")
    else:
        id_count -= 1
        raise HTTPException(status_code=400, detail="A note with this id already exists")

    return CreateNote(id=id)


@api_router.get("/read_note_by_id", response_model=ReadNoteById)
def read_note_by_id(id: int, token: str):
    """
        Метод считывает заметку по её id
    """

    get_access_by_token(token)
    if os.path.isfile(get_full_path(id)):
        file = open(path + str(id) + ".txt", "r")
        text = file.read()
        file.close()
    else:
        raise HTTPException(status_code=404, detail="Note not found")

    return ReadNoteById(id=id, text=text)


@api_router.get("/get_note_time_info_by_id", response_model=GetNoteTimeInfo)
def get_note_time_info_by_id(id: int, token: str):
    """
        Получение информации о заметке:
    """
    get_access_by_token(token)
    if os.path.isfile(get_full_path(id)):
        timestamp = os.path.getmtime(get_full_path(id))
        last_update = datetime.datetime.fromtimestamp(timestamp)

        c_timestamp = os.path.getctime(get_full_path(id))
        create_time = datetime.datetime.fromtimestamp(c_timestamp)
    else:
        raise HTTPException(status_code=404, detail="Note not found")

    return GetNoteTimeInfo(created_at=str(create_time), updated_at=str(last_update))


@api_router.put("/update_note_text", response_model=UpdateNoteText)
def update_note_text(id: int, text: str, token: str):
    """
        Обновление текста заметки
    """
    get_access_by_token(token)
    if os.path.isfile(get_full_path(id)):
        file = open(get_full_path(id), "w")
        file.write(text)
        file.close()
    else:
        raise HTTPException(status_code=404, detail="Note not found")

    return UpdateNoteText(id=id, text=text)


@api_router.delete("/delete_note_by_id", response_model=DeleteNoteById)
def delete_note_by_id(id: int, token: str):
    """
        Удаление заметки
    """
    global id_count

    get_access_by_token(token)
    if os.path.isfile(get_full_path(id)):
        os.remove(get_full_path(id))
    else:
        raise HTTPException(status_code=404, detail="Note not found")

    return DeleteNoteById(isDelete=True)


@api_router.get("/print_note_id", response_model=PrintNoteId)
def print_note_id(token: str):
    """
        Вывод списка id заметок
    """
    get_access_by_token(token)
    all_notes = os.listdir(path)
    output = {}
    count = 0
    for note in all_notes:
        output[count] = note[0:len(note) - 4]
        count += 1

    return PrintNoteId(dict_id=output)
