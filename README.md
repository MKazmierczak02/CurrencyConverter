# CurrencyConverter

CurrencyConverter is a project that allows you to convert currency to PLN using different data sources.

## Requirements

- Python 3.8+
- pip

## Installation
To install the required dependencies, run:
```sh
pip install -r requirements/base.txt
```
For tests:
```sh
pip install -r requirements/test.txt
```
## Usage
You can run the script using the following command:
```sh
python -m task --currency USD --amount 100 --source api
```
For development mode:
```sh
python -m task --currency USD --amount 100 --source api --dev
```
For more info about parameters use:
```sh
python -m task --help
```

## Extra params
- --currency: Currency to convert from. In ISO4217 format
- --amount: Amount that should be converted
- --source: Source of Data. Choose from [local, api]
- --dev: Run in development mode. (Use local json db)
  
## Tests
To run tests, use:
```sh
pytest tests
```

