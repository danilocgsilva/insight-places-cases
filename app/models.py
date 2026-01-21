from sqlalchemy import Column, String, Integer, Boolean, Date, Numeric, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Proprietario(Base):
    __tablename__ = 'proprietarios'
    
    proprietario_id = Column(String(255), primary_key=True)
    nome = Column(String(255))
    cpf_cnpj = Column(String(20))
    contato = Column(String(255))
    
    # Relationships
    hospedagens = relationship('Hospedagem', back_populates='proprietario')


class Cliente(Base):
    __tablename__ = 'clientes'
    
    cliente_id = Column(String(255), primary_key=True)
    nome = Column(String(255))
    cpf = Column(String(14))
    contato = Column(String(255))
    
    # Relationships
    alugueis = relationship('Aluguel', back_populates='cliente')
    avaliacoes = relationship('Avaliacao', back_populates='cliente')


class Endereco(Base):
    __tablename__ = 'enderecos'
    
    endereco_id = Column(String(255), primary_key=True)
    rua = Column(String(255))
    numero = Column(Integer)
    bairro = Column(String(255))
    cidade = Column(String(255))
    estado = Column(String(2))
    cep = Column(String(10))
    
    # Relationships
    hospedagens = relationship('Hospedagem', back_populates='endereco')


class Hospedagem(Base):
    __tablename__ = 'hospedagens'
    
    hospedagem_id = Column(String(255), primary_key=True)
    tipo = Column(String(50))
    endereco_id = Column(String(255), ForeignKey('enderecos.endereco_id'))
    proprietario_id = Column(String(255), ForeignKey('proprietarios.proprietario_id'))
    ativo = Column(Boolean)
    
    # Relationships
    endereco = relationship('Endereco', back_populates='hospedagens')
    proprietario = relationship('Proprietario', back_populates='hospedagens')
    alugueis = relationship('Aluguel', back_populates='hospedagem')
    avaliacoes = relationship('Avaliacao', back_populates='hospedagem')


class Aluguel(Base):
    __tablename__ = 'alugueis'
    
    aluguel_id = Column(String(255), primary_key=True)
    cliente_id = Column(String(255), ForeignKey('clientes.cliente_id'))
    hospedagem_id = Column(String(255), ForeignKey('hospedagens.hospedagem_id'))
    data_inicio = Column(Date)
    data_fim = Column(Date)
    preco_total = Column(Numeric(10, 2))
    
    # Relationships
    cliente = relationship('Cliente', back_populates='alugueis')
    hospedagem = relationship('Hospedagem', back_populates='alugueis')


class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    
    avaliacao_id = Column(String(255), primary_key=True)
    cliente_id = Column(String(255), ForeignKey('clientes.cliente_id'))
    hospedagem_id = Column(String(255), ForeignKey('hospedagens.hospedagem_id'))
    nota = Column(Integer)
    comentario = Column(Text)
    
    # Relationships
    cliente = relationship('Cliente', back_populates='avaliacoes')
    hospedagem = relationship('Hospedagem', back_populates='avaliacoes')
