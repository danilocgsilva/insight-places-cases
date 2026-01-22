from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Endereco


class EnderecoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, endereco: Endereco) -> Endereco:
        self.db.add(endereco)
        self.db.commit()
        self.db.refresh(endereco)
        return endereco

    def get_by_id(self, endereco_id: str) -> Optional[Endereco]:
        return self.db.query(Endereco).filter(
            Endereco.endereco_id == endereco_id
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Endereco]:
        return self.db.query(Endereco).offset(skip).limit(limit).all()

    def get_by_cep(self, cep: str) -> List[Endereco]:
        return self.db.query(Endereco).filter(
            Endereco.cep == cep
        ).all()

    def get_by_cidade(self, cidade: str, skip: int = 0, limit: int = 100) -> List[Endereco]:
        return self.db.query(Endereco).filter(
            Endereco.cidade.ilike(f"%{cidade}%")
        ).offset(skip).limit(limit).all()

    def update(self, endereco_id: str, endereco_data: dict) -> Optional[Endereco]:
        endereco = self.get_by_id(endereco_id)
        if endereco:
            for key, value in endereco_data.items():
                if hasattr(endereco, key):
                    setattr(endereco, key, value)
            self.db.commit()
            self.db.refresh(endereco)
        return endereco

    def delete(self, endereco_id: str) -> bool:
        endereco = self.get_by_id(endereco_id)
        if endereco:
            if endereco.hospedagens:
                return False
            self.db.delete(endereco)
            self.db.commit()
            return True
        return False

    def search_by_address(self, rua: str = None, bairro: str = None, 
                         cidade: str = None, estado: str = None) -> List[Endereco]:
        filters = []
        if rua:
            filters.append(Endereco.rua.ilike(f"%{rua}%"))
        if bairro:
            filters.append(Endereco.bairro.ilike(f"%{bairro}%"))
        if cidade:
            filters.append(Endereco.cidade.ilike(f"%{cidade}%"))
        if estado:
            filters.append(Endereco.estado == estado.upper())
        
        query = self.db.query(Endereco)
        if filters:
            query = query.filter(and_(*filters))
        
        return query.all()