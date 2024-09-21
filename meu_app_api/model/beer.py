from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from  model import Base


class Beer(Base):
    __tablename__ = 'beer'

    id = Column("pk_beer", Integer, primary_key=True)
    name = Column(String(140), unique=True)
    type = Column(String(140))
    ibu = Column(Float)
    value = Column(Float)
    note = Column(Float)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, name:str, type:str, ibu:float, value:float, note:float,
                 date:Union[DateTime, None] = None):
        """
        Cria uma Cerveja

        Arguments:
            name: nome da cerveja
            type: tipo da cerveja
            ibu: valor do IBU da cerveja
            value: valor pago na cerveja
            note: nota da cervea 
            date: data de quando a cerveja foi inserida na base
        """
        self.name = name
        self.type = type
        self.ibu = ibu
        self.value = value
        self.note = note  
        self.date = date


