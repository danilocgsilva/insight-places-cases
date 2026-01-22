from typing import List, Optional, Tuple
from datetime import date, datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, between
from models import Aluguel, Cliente, Hospedagem

class AluguelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, aluguel: Aluguel) -> Aluguel:
        self.db.add(aluguel)
        self.db.commit()
        self.db.refresh(aluguel)
        return aluguel

    def get_by_id(self, aluguel_id: str, with_relations: bool = False) -> Optional[Aluguel]:
        query = self.db.query(Aluguel)
        if with_relations:
            query = query.options(
                joinedload(Aluguel.cliente),
                joinedload(Aluguel.hospedagem)
            )
        return query.filter(Aluguel.aluguel_id == aluguel_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, 
                with_relations: bool = False) -> List[Aluguel]:
        query = self.db.query(Aluguel)
        if with_relations:
            query = query.options(
                joinedload(Aluguel.cliente),
                joinedload(Aluguel.hospedagem)
            )
        return query.offset(skip).limit(limit).all()

    def get_by_cliente(self, cliente_id: str, with_relations: bool = False) -> List[Aluguel]:
        query = self.db.query(Aluguel).filter(
            Aluguel.cliente_id == cliente_id
        )
        if with_relations:
            query = query.options(
                joinedload(Aluguel.cliente),
                joinedload(Aluguel.hospedagem)
            )
        return query.all()

    def get_by_hospedagem(self, hospedagem_id: str, with_relations: bool = False) -> List[Aluguel]:
        query = self.db.query(Aluguel).filter(
            Aluguel.hospedagem_id == hospedagem_id
        )
        if with_relations:
            query = query.options(
                joinedload(Aluguel.cliente),
                joinedload(Aluguel.hospedagem)
            )
        return query.all()

    def update(self, aluguel_id: str, aluguel_data: dict) -> Optional[Aluguel]:
        aluguel = self.get_by_id(aluguel_id)
        if aluguel:
            for key, value in aluguel_data.items():
                if hasattr(aluguel, key):
                    setattr(aluguel, key, value)
            self.db.commit()
            self.db.refresh(aluguel)
        return aluguel

    def delete(self, aluguel_id: str) -> bool:
        aluguel = self.get_by_id(aluguel_id)
        if aluguel:
            self.db.delete(aluguel)
            self.db.commit()
            return True
        return False

    def get_active_rentals(self, as_of_date: date = None) -> List[Aluguel]:
        if as_of_date is None:
            as_of_date = date.today()
        
        return self.db.query(Aluguel).filter(
            and_(
                Aluguel.data_inicio <= as_of_date,
                Aluguel.data_fim >= as_of_date
            )
        ).all()

    def check_availability(self, hospedagem_id: str, start_date: date, end_date: date) -> bool:
        overlapping_rentals = self.db.query(Aluguel).filter(
            and_(
                Aluguel.hospedagem_id == hospedagem_id,
                or_(
                    between(start_date, Aluguel.data_inicio, Aluguel.data_fim),
                    between(end_date, Aluguel.data_inicio, Aluguel.data_fim),
                    and_(Aluguel.data_inicio >= start_date, Aluguel.data_inicio <= end_date),
                    and_(Aluguel.data_fim >= start_date, Aluguel.data_fim <= end_date)
                )
            )
        ).count()
        
        return overlapping_rentals == 0

    def get_rentals_in_period(self, start_date: date, end_date: date) -> List[Aluguel]:
        return self.db.query(Aluguel).filter(
            or_(
                between(Aluguel.data_inicio, start_date, end_date),
                between(Aluguel.data_fim, start_date, end_date),
                and_(Aluguel.data_inicio <= start_date, Aluguel.data_fim >= end_date)
            )
        ).all()

    def get_revenue_by_period(self, start_date: date, end_date: date) -> float:
        result = self.db.query(
            sqlalchemy.func.sum(Aluguel.preco_total)
        ).filter(
            and_(
                Aluguel.data_inicio >= start_date,
                Aluguel.data_fim <= end_date
            )
        ).scalar()
        
        return float(result) if result else 0.0

    def get_most_frequent_clients(self, limit: int = 10) -> List[Tuple[Cliente, int]]:
        from sqlalchemy import func
        
        result = self.db.query(
            Cliente,
            func.count(Aluguel.aluguel_id).label('rental_count')
        ).join(Aluguel).group_by(Cliente.cliente_id).order_by(
            func.count(Aluguel.aluguel_id).desc()
        ).limit(limit).all()
        
        return result