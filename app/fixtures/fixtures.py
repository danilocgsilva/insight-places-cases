# fixtures.py
from database import SessionLocal, init_db
from repositories import ProprietarioRepository
from factories import ProprietarioFactory

def seed_proprietario():
    """Add a single proprietario to the database"""
    # Initialize database tables
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create repository
        repo = ProprietarioRepository(db)
        
        # Create proprietario using factory
        proprietario = ProprietarioFactory.create(
            nome="João da Silva",
            cpf_cnpj="123.456.789-00",
            contato="(11) 98765-4321"
        )
        
        # Save to database
        created = repo.create(proprietario)
        
        print(f"✓ Proprietario created: {created.nome} (ID: {created.proprietario_id})")
        return created
        
    except Exception as e:
        print(f"✗ Error creating proprietario: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def seed_multiple_proprietarios(count: int = 5):
    """Add multiple proprietarios to the database"""
    init_db()
    db = SessionLocal()
    
    try:
        repo = ProprietarioRepository(db)
        proprietarios = ProprietarioFactory.create_batch(count)
        
        created_proprietarios = []
        for proprietario in proprietarios:
            created = repo.create(proprietario)
            created_proprietarios.append(created)
            print(f"✓ Proprietario created: {created.nome}")
        
        print(f"\n✓ Total: {len(created_proprietarios)} proprietarios created")
        return created_proprietarios
        
    except Exception as e:
        print(f"✗ Error creating proprietarios: {e}")
        db.rollback()
        raise
    finally:
        db.close()