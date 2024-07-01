import json
import pytest
from unittest.mock import patch, mock_open
from task.connectors.database.json import JsonFileDatabaseConnector
from task.currency_converter import ConvertedPricePLN


@pytest.fixture
def mock_json_db():
    return {
        "1": {
            "id": 1,
            "currency": "eur",
            "rate": 4.6285,
            "price_in_pln": 21.1,
            "date": "2010-01-01",
        },
        "3": {
            "id": 3,
            "currency": "eur",
            "rate": 4.985,
            "price_in_pln": 22.1,
            "date": "2012-01-01",
        },
    }


@pytest.fixture
def converted_price_instance():
    return ConvertedPricePLN(
        id=1, currency="eur", rate=4.6285, date="2023-01-02", price_in_pln=21.1
    )


def test_read_data(mock_json_db):
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_json_db))):
        with patch(
            "task.connectors.database.json.JSON_DATABASE_NAME",
            new_callable=lambda: "test_db.json",
        ):
            connector = JsonFileDatabaseConnector()
            data = connector._read_data()
            assert data == mock_json_db


def test_save(converted_price_instance, mock_json_db):
    mock_open_instance = mock_open(read_data=json.dumps(mock_json_db))
    with patch("builtins.open", mock_open_instance, create=True):
        with patch(
            "task.connectors.database.json.JSON_DATABASE_NAME",
            new_callable=lambda: "test_db.json",
        ):
            with patch("json.dump") as mock_json_dump:
                connector = JsonFileDatabaseConnector()
                entity_id = connector.save(converted_price_instance)
                mock_open_instance.assert_called_with("test_db.json", "w")
                mock_json_dump.assert_called_once()
                args, kwargs = mock_json_dump.call_args
                assert args[1].write
                assert entity_id == 4


def test_get_by_id(mock_json_db):
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_json_db))):
        with patch(
            "task.connectors.database.json.JSON_DATABASE_NAME",
                value="test_db.json"
        ):
            connector = JsonFileDatabaseConnector()
            entity = connector.get_by_id(1)
            assert entity.currency == "eur"
            assert entity.price_in_pln == 21.1


def test_get_all(mock_json_db):
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_json_db))):
        with patch(
            "task.connectors.database.json.JSON_DATABASE_NAME",
            new_callable=lambda: "test_db.json",
        ):
            connector = JsonFileDatabaseConnector()
            all_data = connector.get_all()
            assert len(all_data) == 2
            assert all_data[0].currency == "eur"
