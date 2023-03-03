# backend-python-creditcard

# Descrição

O problema proposto foi de criar uma API para cadastro de cartão de crédito e visualização dos dados. A api conta com 3 rotas:

- POST - ```/api/v1/credit-card```(cadastro de cartão de crédito);
- GET - ```/api/v1/credit-card``` (listar todos os cartoes de credito);
- GET - ```/api/v1/credit-card/{ID}``` (mostrar dados de cartão de crédito por ID);

# Rodando o projeto

Para rodar o projeto, as configurações usadas são:

- Python 3.10

Os passos para rodar o projeto são:

1. mude para o diretório raiz do projeto;
2. crie um ambiente virtual python;
3. rode ```pip install -r requirements.txt``` para instalar as dependências;
4. rode ```uvicorn app.main:app --reload```;


Os passos para rodar os testes são:

1. rode ```pytest``` no diretório raiz do projeto;

# Tecnologias escolhidas

- [Python](https://www.python.org/) - Linguagem de programação alto nivel interpretadas e altamente usada para desenvolvimento web;
- [FastAPI](https://fastapi.tiangolo.com/) - Framework python moderno para construção de web APIs;
- [Pydantic](https://docs.pydantic.dev/) - Biblioteca para validação de dados e criação e schemas;
- [SQLAlchemy](https://www.sqlalchemy.org/) - Biblioteca de ORM SQL para python;
- [Cryptography](https://cryptography.io/en/latest/) - Biblioteca para criptografia de dados;
- [Pytest](https://docs.pytest.org/en/7.2.x/) - Biblioteca de testes para python;
