from repositories.base_repository import BaseRepository, CRUDBase
from schemas.button_schemas import ButtonCreate, ButtonUpdate
from fastapi import Depends, HTTPException
from models.models import Button
from typing import Optional

class ButtonsRepository(CRUDBase):
    def __init__(self, base_repository: BaseRepository = Depends()):
        self.base_repository = base_repository

    @property
    def _entity(self):
        return Button

    def create(self, button_data: ButtonCreate, image_path: str, user_id: int):
        new_button = Button(
            name=button_data.name,
            description=button_data.description,
            image_path=image_path,
            user_id=user_id
        )
        try:
            return self.base_repository.create(new_button)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Erro ao criar botão."
            ) from e

    def find_one(self, button_id: int):
        button = self.base_repository.find_one(self._entity, button_id)
        if not button:
            raise HTTPException(
                status_code=404, detail="Botão não encontrado."
            )
        return button

    def find_all(self):
        return self.base_repository.find_all(self._entity)

    def update(self, button_id: int, button_data: ButtonUpdate, image_path: Optional[str] = None):
        try:
            button = self.base_repository.find_one(self._entity, button_id)
            if not button:
                raise HTTPException(
                    status_code=404, detail="Botão não encontrado."
                )

            if button_data.name is not None:
                button.name = button_data.name

            if button_data.description is not None:
                button.description = button_data.description

            if image_path:
                button.image_path = image_path

            self.base_repository.db.commit()
            self.base_repository.db.refresh(button)
            return {"message": "Botão atualizado com sucesso."}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Erro ao atualizar botão."
            ) from e

    def delete(self, button_id: int):
        try:
            button = self.find_one(button_id)
            self.base_repository.delete_one(self._entity, button_id)
            return {"message": "Botão removido com sucesso."}
        except Exception:
            raise HTTPException(
                status_code=500, detail="Erro ao remover botão."
            )
