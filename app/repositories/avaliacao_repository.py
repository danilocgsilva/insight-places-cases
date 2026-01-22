from typing import List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func
from models import Avaliacao, Cliente, Hospedagem


class AvaliacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, avaliacao: Avaliacao) -> Avaliacao:
        self.db.add(avaliacao)
        self.db.commit()
        self.db.refresh(avaliacao)
        return avaliacao

    def get_by_id(self, avaliacao_id: str, with_relations: bool = False) -> Optional[Avaliacao]:
        query = self.db.query(Avaliacao)
        if with_relations:
            query = query.options(
                joinedload(Avaliacao.cliente),
                joinedload(Avaliacao.hospedagem)
            )
        return query.filter(Avaliacao.avaliacao_id == avaliacao_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, 
                with_relations: bool = False) -> List[Avaliacao]:
        query = self.db.query(Avaliacao)
        if with_relations:
            query = query.options(
                joinedload(Avaliacao.cliente),
                joinedload(Avaliacao.hospedagem)
            )
        return query.offset(skip).limit(limit).all()

    def get_by_cliente(self, cliente_id: str, with_relations: bool = False) -> List[Avaliacao]:
        query = self.db.query(Avaliacao).filter(
            Avaliacao.cliente_id == cliente_id
        )
        if with_relations:
            query = query.options(
                joinedload(Avaliacao.cliente),
                joinedload(Avaliacao.hospedagem)
            )
        return query.all()

    def get_by_hospedagem(self, hospedagem_id: str, with_relations: bool = False) -> List[Avaliacao]:
        query = self.db.query(Avaliacao).filter(
            Avaliacao.hospedagem_id == hospedagem_id
        )
        if with_relations:
            query = query.options(
                joinedload(Avaliacao.cliente),
                joinedload(Avaliacao.hospedagem)
            )
        return query.all()

    def update(self, avaliacao_id: str, avaliacao_data: dict) -> Optional[Avaliacao]:
        avaliacao = self.get_by_id(avaliacao_id)
        if avaliacao:
            for key, value in avaliacao_data.items():
                if hasattr(avaliacao, key):
                    setattr(avaliacao, key, value)
            self.db.commit()
            self.db.refresh(avaliacao)
        return avaliacao

    def delete(self, avaliacao_id: str) -> bool:
        avaliacao = self.get_by_id(avaliacao_id)
        if avaliacao:
            self.db.delete(avaliacao)
            self.db.commit()
            return True
        return False

    def get_average_rating(self, hospedagem_id: str) -> Optional[float]:
        result = self.db.query(
            func.avg(Avaliacao.nota).label('average_rating')
        ).filter(
            Avaliacao.hospedagem_id == hospedagem_id
        ).scalar()
        
        return float(result) if result else None

    def get_ratings_summary(self, hospedagem_id: str) -> dict:
        result = self.db.query(
            Avaliacao.nota,
            func.count(Avaliacao.avaliacao_id).label('count')
        ).filter(
            Avaliacao.hospedagem_id == hospedagem_id
        ).group_by(Avaliacao.nota).all()
        
        summary = {rating: 0 for rating in range(1, 6)}
        for nota, count in result:
            summary[nota] = count
        
        return summary

    def get_recent_reviews(self, hospedagem_id: str, limit: int = 5) -> List[Avaliacao]:
        return self.db.query(Avaliacao).filter(
            Avaliacao.hospedagem_id == hospedagem_id
        ).order_by(Avaliacao.avaliacao_id.desc()).limit(limit).all()

    def get_highest_rated_hospedagens(self, limit: int = 10) -> List[Tuple[Hospedagem, float]]:
        from sqlalchemy import func
        
        result = self.db.query(
            Hospedagem,
            func.avg(Avaliacao.nota).label('average_rating'),
            func.count(Avaliacao.avaliacao_id).label('review_count')
        ).join(Avaliacao).group_by(Hospedagem.hospedagem_id).having(
            func.count(Avaliacao.avaliacao_id) >= 3
        ).order_by(
            func.avg(Avaliacao.nota).desc()
        ).limit(limit).all()
        
        return result

    def search_by_comment(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Avaliacao]:
        return self.db.query(Avaliacao).filter(
            Avaliacao.comentario.ilike(f"%{search_term}%")
        ).offset(skip).limit(limit).all()