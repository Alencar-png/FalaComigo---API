from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from http import HTTPStatus
from repositories.buttons_repository import ButtonsRepository
from repositories.security_repository import SecurityRepository
from schemas.button_schemas import ButtonCreate, ButtonUpdate, ButtonResponse
import os
import uuid
from typing import Optional, List

button = APIRouter()

@button.post("/buttons/", response_model=ButtonResponse, status_code=201)
async def create_button(
    name: str,
    description: Optional[str] = None,
    image: UploadFile = File(...),
    repo: ButtonsRepository = Depends(),
    current_user: SecurityRepository.get_current_user = Depends()
):
    # Qualquer usuário autenticado pode criar um botão
    user_id = current_user["user_id"]

    # Salvar a imagem
    upload_directory = "images"
    os.makedirs(upload_directory, exist_ok=True)
    unique_filename = f"{uuid.uuid4()}_{image.filename}"
    file_location = os.path.join(upload_directory, unique_filename)

    with open(file_location, "wb") as file_object:
        file_object.write(await image.read())

    # Criar o botão
    button_data = ButtonCreate(name=name, description=description)
    button = repo.create(button_data, image_path=file_location, user_id=user_id)
    return button

@button.get("/buttons/", response_model=List[ButtonResponse])
def read_buttons(
    repo: ButtonsRepository = Depends(),
    current_user: SecurityRepository.get_current_user = Depends()
):
    # Retornar todos os botões ou filtrar por usuário, se necessário
    buttons = repo.find_all()
    return buttons

@button.get("/buttons/{button_id}", response_model=ButtonResponse)
def read_button(
    button_id: int,
    repo: ButtonsRepository = Depends(),
    current_user: SecurityRepository.get_current_user = Depends()
):
    button = repo.find_one(button_id)
    # Verificar se o usuário tem permissão para visualizar o botão
    if button.user_id != current_user["user_id"] and not current_user["is_admin"]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para visualizar este botão.'
        )
    return button

@button.put("/buttons/{button_id}", response_model=ButtonResponse)
async def update_button(
    button_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    image: Optional[UploadFile] = File(None),
    repo: ButtonsRepository = Depends(),
    current_user: SecurityRepository.get_current_user = Depends()
):
    button = repo.find_one(button_id)
    # Verificar se o usuário tem permissão para atualizar o botão
    if button.user_id != current_user["user_id"] and not current_user["is_admin"]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar este botão.'
        )

    image_path = None
    if image:
        # Remover a imagem antiga
        if os.path.exists(button.image_path):
            os.remove(button.image_path)

        # Salvar a nova imagem
        upload_directory = "images"
        os.makedirs(upload_directory, exist_ok=True)
        unique_filename = f"{uuid.uuid4()}_{image.filename}"
        file_location = os.path.join(upload_directory, unique_filename)

        with open(file_location, "wb") as file_object:
            file_object.write(await image.read())
        image_path = file_location

    button_data = ButtonUpdate(name=name, description=description)
    repo.update(button_id, button_data, image_path=image_path)
    updated_button = repo.find_one(button_id)
    return updated_button

@button.delete("/buttons/{button_id}")
def delete_button(
    button_id: int,
    repo: ButtonsRepository = Depends(),
    current_user: SecurityRepository.get_current_user = Depends()
):
    button = repo.find_one(button_id)
    # Verificar se o usuário tem permissão para deletar o botão
    if button.user_id != current_user["user_id"] and not current_user["is_admin"]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para deletar este botão.'
        )

    # Remover a imagem associada
    if os.path.exists(button.image_path):
        os.remove(button.image_path)

    return repo.delete(button_id)
