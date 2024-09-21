from pydantic import BaseModel
from typing import Optional, List
from model.beer import Beer


class BeerSchema(BaseModel):  
    """ Define como uma nova cerveja a ser inserida deve ser representada
    """
    name: str = "Lagunitas"
    type: Optional[str] = "IPA"
    ibu: Optional[float] = 51.5
    value: Optional[float] = 15.50
    note: float = 8.5

class FindBeerSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da cerveja.
    """
    name: str = "Teste"


class BeerListSchema(BaseModel): 
    """ Define como uma listagem de cervejas será retornada.
    """
    beers:List[BeerSchema]


def view_beers(beers: List[Beer]): 
    """ Retorna uma representação de cerveja seguindo o schema definido em
        BeerSchema.
    """
    result = []
    for beer in beers:
        result.append({
            "name": beer.name,
            "type": beer.type,
            "ibu": beer.ibu,
            "value": beer.value,
            "note": beer.note,
            "date": beer.date,
        })

    return {"beers": result}


class BeerViewSchema(BaseModel): 
    """ Define como uma cerveja será retornada
    """
    id: int = 1
    name: str = "Lagunitas"
    type: Optional[str] = "IPA"
    ibu: Optional[float] = 51.5
    value: Optional[float] = 13.50
    note: float = 8.5
   

class BeerDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    name: str

def view_beer(beer: Beer): 
    """ Retorna uma representação da cerveja seguindo o schema definido em
        BeerViewSchema.
    """
    return {
        "id": beer.id,
        "name": beer.name,
        "type": beer.type,
        "ibu": beer.ibu,
        "value": beer.value,
        "note": beer.note,
        "date": beer.date,
       
    }
