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
    quantidade_episodios = Column(Integer, nullable=False)

    #Relacionamento com a classe filha
    episodios = relationship('Episodio', back_populates='serie', cascade="all, delete-orphan")

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

#Criação do Banco e Inserção de Dados
#Criar o banco (SQLite recomendado)
#Criar as tabelas
#Criar uma função para inserir dados da tabela PAI
#Criar uma função para inserir dados da tabela FILHA
#Pelo menos 4 registros na tabela pai
#Pelo menos 10 registros na tabela filha
# Todos os filhos devem ter um pai_id válido
# genero tam
def inserir_serie():
    with Session() as session:
        try:
            nova_serie = input("Digite o nome da série: ").capitalize()
            novo_genero = input("Digite o gênero da série: ").capitalize()
            novas_temporadas = int(input("Digite o número de temporadas: "))
            novos_episodios = float(input("Digite o número de episódios: "))

            serie = Serie(
                nome=nova_serie, 
                genero=novo_genero, 
                temporadas=novas_temporadas, 
                quantidade_episodios=novos_episodios
            )
            
            session.add(serie)
            session.commit()
            print("Série inserida com sucesso!")
        except Exception as erro:
            print(f"Erro ao inserir série: {erro}")
            session.rollback()
# inserir_serie()

def inserir_episodio():
    with Session() as session:
        try:
            nome_episodio = input("Digite o nome do episódio: ").capitalize()
            duracao_episodio = float(input("Digite a duração do episódio (em minutos): "))
            lancamento_episodio = input("Digite a data de lançamento do episódio (dd/mm/aaaa): ")
            serie_id = int(input("Digite o ID da série a qual o episódio pertence: "))

            episodio = Episodio(
                nome=nome_episodio,
                duracao=duracao_episodio,
                lancamento=lancamento_episodio,
                serie_id=serie_id
            )

            session.add(episodio)
            session.commit()
            print("Episódio inserido com sucesso!")
        except Exception as erro:
            print(f"Erro ao inserir episódio: {erro}")
            session.rollback()
# inserir_episodio()

# Criar funções para consultas:
# 1. Listar todos os filhos com dados do pai
# 2. Filtrar filhos de um pai específico
# 3. Listar apenas pais que possuem filhos

def listar_ep_com_series():
    with Session() as session:
        try:
            episodios = session.query(Episodio).all()
            for ep in episodios:
                print(f"Episódio: {ep.nome}, Série: {ep.serie.nome}")
        except Exception as erro:
            print(f"Erro ao listar episódios com séries: {erro}")
# listar_ep_com_series()

def filtrar_ep_por_serie():
    with Session() as session:
        try:
            serie_id = int(input("Digite o ID da série para filtrar os episódios: "))
            episodios = session.query(Episodio).filter(Episodio.serie_id == serie_id).all()
            for ep in episodios:
                print(f"Episódio: {ep.nome}, Série: {ep.serie.nome}")
        except Exception as erro:
            print(f"Erro ao filtrar episódios por série: {erro}")
# filtrar_ep_por_serie()

def listar_series_com_episodios():
    with Session() as session:
        try:
            series = session.query(Serie).join(Episodio).all()
            for serie in series:
                print(f"Série: {serie.nome}, Gênero: {serie.genero}, Temporadas: {serie.temporadas}, Quantidade de Episódios: {serie.quantidade_episodios}")
        except Exception as erro:
            print(f"Erro ao listar séries com episódios: {erro}")

# listar_series_com_episodios()

# Atualização de Dados (UPDATE)
# Criar funções para atualizar informações no banco
# 1. Atualizar dados de um pai
# 2. Atualizar dados de um filho

def atualizar_serie():
    with Session() as session:
        try:
            serie_id = int(input("Digite o ID da série que deseja atualizar: "))
            serie = session.query(Serie).filter(Serie.id == serie_id).first()
            if serie:
                novo_nome = input("Digite o novo nome da série: ").capitalize()
                novo_genero = input("Digite o novo gênero da série: ").capitalize()
                novas_temporadas = int(input("Digite o novo número de temporadas: "))
                novos_episodios = float(input("Digite o novo número de episódios: "))

                serie.nome = novo_nome
                serie.genero = novo_genero
                serie.temporadas = novas_temporadas
                serie.quantidade_episodios = novos_episodios

                session.commit()
                print("Série atualizada com sucesso!")
            else:
                print("Série não encontrada.")
        except Exception as erro:
            print(f"Erro ao atualizar série: {erro}")
            session.rollback()
# atualizar_serie()

def atualizar_episodio():
    with Session() as session:
        try:
            episodio_id = int(input("Digite o ID do episódio que deseja atualizar: "))
            episodio = session.query(Episodio).filter(Episodio.id == episodio_id).first()
            if episodio:
                novo_nome = input("Digite o novo nome do episódio: ").capitalize()
                nova_duracao = float(input("Digite a nova duração do episódio (em minutos): "))
                nova_data_lancamento = input("Digite a nova data de lançamento do episódio (dd/mm/aaaa): ")

                episodio.nome = novo_nome
                episodio.duracao = nova_duracao
                episodio.lancamento = nova_data_lancamento

                session.commit()
                print("Episódio atualizado com sucesso!")
            else:
                print("Episódio não encontrado.")
        except Exception as erro:
            print(f"Erro ao atualizar episódio: {erro}")
            session.rollback()
# atualizar_episodio()

# Remoção de Dados (DELETE)
# Criar funções para deletar registros:
# 1. Deletar um filho
# 2. Deletar um pai
# 3. Tratar relacionamento (ex: evitar erro ao deletar pai
# com filhos)

def deletar_episodio():
    with Session() as session:
        try:
            episodio_id = int(input("Digite o ID do episódio que deseja deletar: "))
            episodio = session.query(Episodio).filter(Episodio.id == episodio_id).first()
            if episodio:
                session.delete(episodio)
                session.commit()
                print("Episódio deletado com sucesso!")
            else:
                print("Episódio não encontrado.")
        except Exception as erro:
            print(f"Erro ao deletar episódio: {erro}")
            session.rollback()
# deletar_episodio()

# Deletar um pai mesmo que possua filhos associados, utilizando cascade
def deletar_serie():
    with Session() as session:
        try:
            serie_id = int(input("Digite o ID da série que deseja deletar: "))
            serie = session.query(Serie).filter(Serie.id == serie_id).first()
            if serie:
                serie.cascade = "all, delete-orphan"
                session.delete(serie)
                session.commit()
                print("Série deletada com sucesso!")
            else:
                print("Série não encontrada.")
        except Exception as erro:
            print(f"Erro ao deletar série: {erro}")
            session.rollback()
deletar_serie()