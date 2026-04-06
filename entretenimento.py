# Pip install sqlachemy
# Criar as classes no arquivo models.py:
# Você deve ter:
# • Uma classe PAI (lado 1)
# • Uma classe FILHA (lado N)
# • Relacionamento usando relationship
# • Chave estrangeira com ForeignKey
# • Pelo menos 4 atributos em cada classe
# Commit:
# feat: cria models com relacionamento 1:N
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
# criar a base da classe

Base = declarative_base()
#Criar a classe pai

class Serie(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    genero = Column(String(100), nullable=False)
    temporadas = Column(Integer, nullable=False)
    episodios = Column(Float, nullable=False)

    #Relacionamento com a classe filha
    episodios = relationship('Episodio', back_populates='serie')

#Criar a classe filha
class Episodio(Base):
    __tablename__ = 'episodios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    duracao = Column(Float, nullable=False)
    lancamento = Column(String(20), nullable=False)
    serie_id = Column(Integer, ForeignKey('series.id'), nullable=False)

    #Relacionamento com a classe pai
    serie = relationship('Serie', back_populates='episodios')

    def __repr__(self):
        return f"Episodio(id={self.id}, nome='{self.nome}', duracao={self.duracao}, lancamento='{self.lancamento}', serie_id={self.serie_id})"

# Criar o banco de dados e as tabelas
engine = create_engine("sqlite:///Rede_entretenimento.db", echo=False)
Base.metadata.create_all(engine)

# Criar uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Criar uma série