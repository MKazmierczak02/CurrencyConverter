from typing import Type
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ...entity.converted_price_pln import ConvertedPricePLN, Base


class SQLiteConnector:
    def __init__(self, db_url="sqlite:///sqlite.db"):
        self.engine = create_engine(db_url, echo=True)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)

    def save(self, entity: ConvertedPricePLN) -> int:
        """
        Save a ConvertedPricePLN object to the database
        :param entity:
        :return:
        """
        session = self.Session()
        session.add(entity)
        session.commit()
        return entity.id

    def get_all(self):
        """
        Get all ConvertedPricePLN objects from the database
        :return:
        """
        session = self.Session()
        result = session.query(ConvertedPricePLN).all()
        session.close()
        return result

    def get_by_id(self, entity_id: int) -> Type[ConvertedPricePLN] | None:
        """
        Get a ConvertedPricePLN object from the database
        :param entity_id:
        :return:
        """
        session = self.Session()
        result = session.query(ConvertedPricePLN).filter_by(id=entity_id).first()
        session.close()
        return result

    def __del__(self):
        self.Session.remove()
