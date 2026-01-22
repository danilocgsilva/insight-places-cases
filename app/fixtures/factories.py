import uuid
from faker import Faker
from models import Proprietario

fake = Faker('pt_BR')  # Brazilian Portuguese locale for realistic data

class ProprietarioFactory:
    """Factory for creating Proprietario instances"""
    
    @staticmethod
    def create(
        proprietario_id: str = None,
        nome: str = None,
        cpf_cnpj: str = None,
        contato: str = None
    ) -> Proprietario:
        """Create a Proprietario instance with default or custom values"""
        return Proprietario(
            proprietario_id=proprietario_id or str(uuid.uuid4()),
            nome=nome or fake.name(),
            cpf_cnpj=cpf_cnpj or fake.cpf(),
            contato=contato or fake.phone_number()
        )
    
    @staticmethod
    def create_batch(count: int = 5) -> list[Proprietario]:
        """Create multiple Proprietario instances"""
        return [ProprietarioFactory.create() for _ in range(count)]