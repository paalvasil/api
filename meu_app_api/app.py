from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from model import Session, Beer
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
beer_tag = Tag(name="Cerveja", description="Adição, visualização e remoção cervejas à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/beer', tags=[beer_tag],
          responses={"200": BeerViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_beer(form: BeerSchema):
    """Adiciona uma nova cerveja à base de dados
    Retorna uma representação das cervejas.
    """
    beer = Beer(
        name=form.name,
        type=form.type,
        ibu=form.ibu,
        value=form.value,
        note=form.note,
        )

    logger.debug(f"Adicionando cerveja: '{beer.name}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando cerveja
        session.add(beer)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cerveja: '{beer.name}'")
        return view_beer(beer), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cerveja de mesmo nome já salva na base :/"
        logger.warning(f"Erro ao adicionar cerveja '{beer.name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cerveja '{beer.name}', {error_msg}")
        return {"message": error_msg}, 400
    

@app.get('/beers', tags=[beer_tag],
         responses={"200": BeerListSchema, "404": ErrorSchema})
def get_beers():
    """Faz a busca por todas as cervejas cadastradas

    Retorna uma representação da listagem de cervejas.
    """
    logger.debug(f"Coletando cervejas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    beers = session.query(Beer).all()

    if not beers:
        # se não há cervejas cadastradas
        return {"cervejas": []}, 200
    else:
        logger.debug(f"%d cervejas econtradas" % len(beers))
        # retorna a representação de cerveja
        print(beers)
        return view_beers(beers), 200
    
@app.get('/beer', tags=[beer_tag],
         responses={"200": BeerViewSchema, "404": ErrorSchema})
def get_beer(query: FindBeerSchema):
    """Faz a busca por uma cerveja a partir do seu nome

    Retorna uma representação de cerveja.
    """
    name_beer = query.name
    logger.debug(f"Coletando dados sobre cerveja #{name_beer}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    beer = session.query(Beer).filter(func.lower(Beer.name) == func.lower(name_beer)).first()

    if not beer:
        # se cerveja não foi encontrada
        error_msg = "Cerveja não encontrada na base :/"
        logger.warning(f"Erro ao buscar cerveja '{name_beer}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Cerveja econtrado: '{beer.name}'")
        # retorna a representação de cerveja
        return view_beer(beer), 200

    

@app.delete('/beer', tags=[beer_tag],
            responses={"200": BeerDelSchema, "404": ErrorSchema})
def del_beer(query: FindBeerSchema):
    """Deleta uma cerveja a partir de seu nome

    Retorna uma mensagem de confirmação da remoção.
    """
    name_beer= unquote(unquote(query.name))
    print(name_beer)
    logger.debug(f"Deletando dados sobre a cerveja #{name_beer}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Beer).filter(func.lower(Beer.name) == func.lower(name_beer)).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada cerveja #{name_beer}")
        return {"message": "Cerveja removida", "name": name_beer}
    else:
        # se a cerveja não foi encontrada
        error_msg = "Cerveja não encontrada na base :/"
        logger.warning(f"Erro ao deletar cerveja #'{name_beer}', {error_msg}")
        return {"message": error_msg}, 404
