from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import Cliente

class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def get_by_id(self, cliente_id: str) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(
            Cliente.cliente_id == cliente_id
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        return self.db.query(Cliente).offset(skip).limit(limit).all()

    def get_by_cpf(self, cpf: str) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(
            Cliente.cpf == cpf
        ).first()

    def update(self, cliente_id: str, cliente_data: dict) -> Optional[Cliente]:
        cliente = self.get_by_id(cliente_id)
        if cliente:
            for key, value in cliente_data.items():
                if hasattr(cliente, key):
                    setattr(cliente, key, value)
            self.db.commit()
            self.db.refresh(cliente)
        return cliente

    def delete(self, cliente_id: str) -> bool:
        cliente = self.get_by_id(cliente_id)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False

    def search(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Cliente]:
        return self.db.query(Cliente).filter(
            or_(
                Cliente.nome.ilike(f"%{search_term}%"),
                Cliente.cpf.ilike(f"%{search_term}%"),
                Cliente.contato.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit).all()

    def get_by_ids(self, cliente_ids: List[str]) -> List[Cliente]:
        return self.db.query(Cliente).filter(
            Cliente.cliente_id.in_(cliente_ids)
        ).all()