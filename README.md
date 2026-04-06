# Entretenimento - Relacionamento 1:N (Séries e Episódios)

Projeto de exemplo que modela um relacionamento 1 para N entre séries (pai) e episódios (filho) usando SQLAlchemy e SQLite.

Equipe: Jackelyne, Yasmin e Kaylan

## Estrutura principal
- Arquivo principal: `entretenimento.py`
- Banco de dados SQLite: `Rede_entretenimento.db`

## Modelos
- Classe `Serie` (tabela `series`) — atributos:
  - `id` (Int, Primary key, autoincrement)
  - `nome` (String, único)
  - `genero` (String)
  - `temporadas` (Int)
  - `quantidade_episodios` (Int)
  - relacionamento: `episodios` (relationship para `Episodio`, cascade="all, delete-orphan")

- Classe `Episodio` (tabela `episodios`) — atributos:
  - `id` (Int, Primary key, autoincrement)
  - `nome` (String)
  - `duracao` (Float)
  - `lancamento` (String)
  - `serie_id` (Int, Foreignkey para `series.id`)

O relacionamento 1:N é feito via `relationship`/`ForeignKey`. O cascade definido em `Serie` faz com que, ao deletar uma instância `Serie` pelo ORM, os `Episodio`s associados também sejam removidos (delete-orphan) no contexto da sessão.

## Funções disponíveis em `entretenimento.py`
- inserir_serie(): insere uma nova série (entrada via input)
- inserir_episodio(): insere um episódio associado a uma série pelo `serie_id`
- listar_ep_com_series(): lista todos os episódios mostrando o nome da série
- filtrar_ep_por_serie(): pede um `serie_id` e lista episódios dessa série
- listar_series_com_episodios(): lista séries que possuem episódios
- atualizar_serie(): atualiza os dados de uma série
- atualizar_episodio(): atualiza os dados de um episódio
- deletar_episodio(): deleta um episódio por id
- deletar_serie(): deleta uma série (os episódios associados são removidos pelo cascade do ORM)

Cada função trata exceções e faz commit/rollback conforme necessário.

Instalação:

```powershell
pip install sqlalchemy
```

O script pede entradas via terminal para executar as operações CRUD.

## Observações sobre o banco de dados
- O arquivo `Rede_entretenimento.db` será criado automaticamente na primeira execução.
- Se você alterar os modelos (atributos/colunas) e quiser recriar o esquema do zero, remova `Rede_entretenimento.db` e execute novamente o script para que as tabelas sejam criadas conforme os modelos atuais.
- Atenção: alterações no esquema em bases já existentes podem requerer migração manual. Uma abordagem simples é remover o arquivo `.db` em ambiente de desenvolvimento.
