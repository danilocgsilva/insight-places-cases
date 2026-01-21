from sqlalchemy import Column, String, Integer, Boolean, Date, DECIMAL, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Proprietario(Base):
    __tablename__ = "proprietarios"
    
    proprietario_id = Column(String(255), primary_key=True)
    nome = Column(String(255), nullable=False)
    cpf_cnpj = Column(String(20))
    contato = Column(String(255))
    
    # Relationships
    hospedagens = relationship("Hospedagem", back_populates="proprietario", cascade="all, delete-orphan")

class Cliente(Base):
    __tablename__ = "clientes"
    
    cliente_id = Column(String(255), primary_key=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14))
    contato = Column(String(255))
    
    # Relationships
    alugueis = relationship("Aluguel", back_populates="cliente", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="cliente", cascade="all, delete-orphan")

class Endereco(Base):
    __tablename__ = "enderecos"
    
    endereco_id = Column(String(255), primary_key=True)
    rua = Column(String(255), nullable=False)
    numero = Column(Integer, nullable=False)
    bairro = Column(String(255), nullable=False)
    cidade = Column(String(255), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(10))
    
    # Relationships
    hospedagens = relationship("Hospedagem", back_populates="endereco", cascade="all, delete-orphan")

class Hospedagem(Base):
    __tablename__ = "hospedagens"
    
    hospedagem_id = Column(String(255), primary_key=True)
    tipo = Column(String(50), nullable=False)
    endereco_id = Column(String(255), ForeignKey("enderecos.endereco_id"), nullable=False)
    proprietario_id = Column(String(255), ForeignKey("proprietarios.proprietario_id"), nullable=False)
    ativo = Column(Boolean, default=True)
    
    # Relationships
    endereco = relationship("Endereco", back_populates="hospedagens")
    proprietario = relationship("Proprietario", back_populates="hospedagens")
    alugueis = relationship("Aluguel", back_populates="hospedagem", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="hospedagem", cascade="all, delete-orphan")

class Aluguel(Base):
    __tablename__ = "alugueis"
    
    aluguel_id = Column(String(255), primary_key=True)
    cliente_id = Column(String(255), ForeignKey("clientes.cliente_id"), nullable=False)
    hospedagem_id = Column(String(255), ForeignKey("hospedagens.hospedagem_id"), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    preco_total = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    cliente = relationship("Cliente", back_populates="alugueis")
    hospedagem = relationship("Hospedagem", back_populates="alugueis")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    
    avaliacao_id = Column(String(255), primary_key=True)
    cliente_id = Column(String(255), ForeignKey("clientes.cliente_id"), nullable=False)
    hospedagem_id = Column(String(255), ForeignKey("hospedagens.hospedagem_id"), nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(Text)
    
    # Relationships
    cliente = relationship("Cliente", back_populates="avaliacoes")
    hospedagem = relationship("Hospedagem", back_populates="avaliacoes")