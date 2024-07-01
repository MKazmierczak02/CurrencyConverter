from sqlalchemy import Column, Integer, String, Float
from sqlalchemy_mixins import AllFeaturesMixin
from dataclasses import dataclass
from sqlalchemy.orm import declarative_base


Base = declarative_base()


@dataclass
class ConvertedPricePLN(Base, AllFeaturesMixin):
    """
    Converted price PLN
    """

    __tablename__ = "converted_price"

    id: int = Column(Integer, primary_key=True)
    currency: str = Column(String)
    rate: float = Column(Float)
    price_in_pln: float = Column(Float)
    date: str = Column(String)
