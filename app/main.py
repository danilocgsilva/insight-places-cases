from sqlalchemy.orm import Session
from database import SessionLocal, engine, create_database
from models import *
import uuid
from datetime import date, timedelta

def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    
    try:
        # Create proprietario
        proprietario_id = str(uuid.uuid4())
        proprietario = Proprietario(
            proprietario_id=proprietario_id,
            nome="João Silva",
            cpf_cnpj="123.456.789-00",
            contato="joao@email.com"
        )
        db.add(proprietario)
        
        # Create endereco
        endereco_id = str(uuid.uuid4())
        endereco = Endereco(
            endereco_id=endereco_id,
            rua="Rua das Flores",
            numero=123,
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            cep="01234-567"
        )
        db.add(endereco)
        
        # Create hospedagem
        hospedagem_id = str(uuid.uuid4())
        hospedagem = Hospedagem(
            hospedagem_id=hospedagem_id,
            tipo="Apartamento",
            endereco_id=endereco_id,
            proprietario_id=proprietario_id,
            ativo=True
        )
        db.add(hospedagem)
        
        # Create cliente
        cliente_id = str(uuid.uuid4())
        cliente = Cliente(
            cliente_id=cliente_id,
            nome="Maria Santos",
            cpf="987.654.321-00",
            contato="maria@email.com"
        )
        db.add(cliente)
        
        # Create aluguel
        aluguel_id = str(uuid.uuid4())
        aluguel = Aluguel(
            aluguel_id=aluguel_id,
            cliente_id=cliente_id,
            hospedagem_id=hospedagem_id,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=7),
            preco_total=1500.00
        )
        db.add(aluguel)
        
        # Create avaliacao
        avaliacao_id = str(uuid.uuid4())
        avaliacao = Avaliacao(
            avaliacao_id=avaliacao_id,
            cliente_id=cliente_id,
            hospedagem_id=hospedagem_id,
            nota=5,
            comentario="Excelente hospedagem!"
        )
        db.add(avaliacao)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

def query_sample_data():
    """Query sample data"""
    db = SessionLocal()
    
    try:
        # Query all hospedagens
        hospedagens = db.query(Hospedagem).all()
        print(f"\nTotal hospedagens: {len(hospedagens)}")
        
        for h in hospedagens:
            print(f"\nHospedagem: {h.tipo}")
            print(f"Endereço: {h.endereco.rua}, {h.endereco.numero}")
            print(f"Proprietário: {h.proprietario.nome}")
            print(f"Ativo: {h.ativo}")
            
            # Show alugueis for this hospedagem
            if h.alugueis:
                print(f"Alugueis: {len(h.alugueis)}")
                for a in h.alugueis:
                    print(f"  - Cliente: {a.cliente.nome}, Período: {a.data_inicio} a {a.data_fim}")
            
            # Show avaliacoes for this hospedagem
            if h.avaliacoes:
                print(f"Avaliações: {len(h.avaliacoes)}")
                for av in h.avaliacoes:
                    print(f"  - Nota: {av.nota}, Comentário: {av.comentario[:50]}...")
                    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables (alternative to migrations)
    create_database()
    
    # Create sample data
    create_sample_data()
    
    # Query sample data
    query_sample_data()