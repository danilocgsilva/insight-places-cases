from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from models import Hospedagem, Proprietario, Endereco


class HospedagemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, hospedagem: Hospedagem) -> Hospedagem:
        self.db.add(hospedagem)
        self.db.commit()
        self.db.refresh(hospedagem)
        return hospedagem

    def get_by_id(self, hospedagem_id: str, with_relations: bool = False) -> Optional[Hospedagem]:
        query = self.db.query(Hospedagem)
        if with_relations:
            query = query.options(
                joinedload(Hospedagem.proprietario),
                joinedload(Hospedagem.endereco)
            )
        return query.filter(Hospedagem.hospedagem_id == hospedagem_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, 
                only_active: bool = True, with_relations: bool = False) -> List[Hospedagem]:
        query = self.db.query(Hospedagem)
        if only_active:
            query = query.filter(Hospedagem.ativo == True)
        if with_relations:
            query = query.options(
                joinedload(Hospedagem.proprietario),
                joinedload(Hospedagem.endereco)
            )
        return query.offset(skip).limit(limit).all()

    def get_by_proprietario(self, proprietario_id: str, only_active: bool = True) -> List[Hospedagem]:
        query = self.db.query(Hospedagem).filter(
            Hospedagem.proprietario_id == proprietario_id
        )
        if only_active:
            query = query.filter(Hospedagem.ativo == True)
        return query.all()

    def get_by_endereco(self, endereco_id: str) -> List[Hospedagem]:
        return self.db.query(Hospedagem).filter(
            Hospedagem.endereco_id == endereco_id
        ).all()

    def update(self, hospedagem_id: str, hospedagem_data: dict) -> Optional[Hospedagem]:
        hospedagem = self.get_by_id(hospedagem_id)
        if hospedagem:
            for key, value in hospedagem_data.items():
                if hasattr(hospedagem, key):
                    setattr(hospedagem, key, value)
            self.db.commit()
            self.db.refresh(hospedagem)
        return hospedagem

    def delete(self, hospedagem_id: str) -> bool:
        hospedagem = self.get_by_id(hospedagem_id)
        if hospedagem:
            if hospedagem.alugueis:
                hospedagem.ativo = False
                self.db.commit()
            else:
                self.db.delete(hospedagem)
                self.db.commit()
            return True
        return False

    def search(self, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Hospedagem]:
        query = self.db.query(Hospedagem)
        
        if 'tipo' in filters:
            query = query.filter(Hospedagem.tipo.ilike(f"%{filters['tipo']}%"))
        
        if 'ativo' in filters:
            query = query.filter(Hospedagem.ativo == filters['ativo'])
        
        if 'cidade' in filters:
            query = query.join(Endereco).filter(
                Endereco.cidade.ilike(f"%{filters['cidade']}%")
            )
        
        if 'estado' in filters:
            query = query.join(Endereco).filter(
                Endereco.estado == filters['estado'].upper()
            )
        
        if 'proprietario_nome' in filters:
            query = query.join(Proprietario).filter(
                Proprietario.nome.ilike(f"%{filters['proprietario_nome']}%")
            )
        
        return query.offset(skip).limit(limit).all()

    def count_by_proprietario(self, proprietario_id: str) -> int:
        return self.db.query(Hospedagem).filter(
            Hospedagem.proprietario_id == proprietario_id,
            Hospedagem.ativo == True
        ).count()