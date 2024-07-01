import json
from dataclasses import asdict

from ...config import JSON_DATABASE_NAME
from ...currency_converter import ConvertedPricePLN


class JsonFileDatabaseConnector:
    def __init__(self):
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_DATABASE_NAME) as file:
            return json.load(file)

    def save(self, entity: ConvertedPricePLN) -> int:
        """
        Save or update an entity in the JSON file.
        :param entity: Dictionary with entity data.
        :return: The ID of the saved or updated entity.
        """
        entity.id = self._get_next_id()
        self._data[str(entity.id)] = asdict(entity)
        self._write_data()
        return entity.id

    def get_all(self) -> list[ConvertedPricePLN]:
        """
        Return a list of all entities in the database.
        """
        return [ConvertedPricePLN(**item) for item in self._data.values()]

    def get_by_id(self, entity_id: int) -> ConvertedPricePLN:
        """
        Return a single entity by its ID.
        :param entity_id: ID of the entity to fetch.
        """
        return ConvertedPricePLN(**self._data.get(str(entity_id)))

    def _write_data(self) -> None:
        """
        Write the current data back to the JSON file.
        """
        with open(JSON_DATABASE_NAME, "w") as file:
            json.dump(self._data, file, indent=4)

    def _get_next_id(self):
        """
        Return the next ID.
        :return:
        """
        self._data = self._read_data()
        max_id = max(self._data.keys(), default=0, key=int)
        return int(max_id) + 1
