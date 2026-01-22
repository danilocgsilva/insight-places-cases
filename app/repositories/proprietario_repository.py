from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Proprietario


class ProprietarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, proprietario: Proprietario) -> Proprietario:
        self.db.add(proprietario)
        self.db.commit()
        self.db.refresh(proprietario)
        return proprietario

    def get_by_id(self, proprietario_id: str) -> Optional[Proprietario]:
        return self.db.query(Proprietario).filter(
            Proprietario.proprietario_id == proprietario_id
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Proprietario]:
        return self.db.query(Proprietario).offset(skip).limit(limit).all()

    def get_by_cpf_cnpj(self, cpf_cnpj: str) -> Optional[Proprietario]:
        return self.db.query(Proprietario).filter(
            Proprietario.cpf_cnpj == cpf_cnpj
        ).first()

    def update(self, proprietario_id: str, proprietario_data: dict) -> Optional[Proprietario]:
        proprietario = self.get_by_id(proprietario_id)
        if proprietario:
            for key, value in proprietario_data.items():
                if hasattr(proprietario, key):
                    setattr(proprietario, key, value)
            self.db.commit()
            self.db.refresh(proprietario)
        return proprietario

    def delete(self, proprietario_id: str) -> bool:
        proprietario = self.get_by_id(proprietario_id)
        if proprietario:
            self.db.delete(proprietario)
            self.db.commit()
            return True
        return False

    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Proprietario]:
        return self.db.query(Proprietario).filter(
            Proprietario.nome.ilike(f"%{name}%")
        ).offset(skip).limit(limit).all()