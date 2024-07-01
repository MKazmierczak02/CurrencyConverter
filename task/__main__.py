import logging
import argparse

from .currency_converter import PriceCurrencyConverterToPLN


logger = logging.getLogger(__name__)


def configure_parser():
    """Configuration of the parser."""
    parser = argparse.ArgumentParser(description="Currency exchange converter.")
    parser.add_argument(
        "-C",
        "--currency",
        type=str,
        required=True,
        help="Currency to convert from. In ISO4217 format",
    )

    parser.add_argument(
        "-A",
        "--amount",
        type=float,
        default=0.0,
        help="Amount that should be converted.",
    )
    parser.add_argument(
        "-S",
        "--source",
        type=str,
        required=True,
        choices=["local", "api"],
        help="Source of Data. Choose from [local, api]",
    )
    parser.add_argument("--dev", action="store_true", help="Run in development mode.")
    return parser


def init_logger(dev_mode=False):
    """Initialize the logger."""
    if dev_mode:
        logging.basicConfig(
            filename="dev_logs.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
    else:
        logging.basicConfig(
            filename="app_logs.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logging.getLogger().addHandler(console_handler)


def init_script():
    """Initialize the arguments."""
    parser = configure_parser()
    script_args = parser.parse_args()
    script_args.currency = script_args.currency.lower()
    init_logger(script_args.dev)
    if script_args.dev:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.debug(f"Running with args: {script_args.__dict__}")
    return script_args


try:
    args = init_script()
    price_currency_converter = PriceCurrencyConverterToPLN(args.source)
    if args.dev:
        from .connectors.database.json import JsonFileDatabaseConnector

        database_connector = JsonFileDatabaseConnector()
    else:
        from .connectors.database.sqlite import SQLiteConnector

        database_connector = SQLiteConnector()

    converted_price = price_currency_converter.convert_to_pln(
        currency=args.currency, price=args.amount
    )
    database_connector.save(converted_price)
    print(f"*** Converted price: {converted_price} ***")
    print(f"*** The rate of currency is: {converted_price.rate} "
          f"The price in pln is: {round(converted_price.price_in_pln, 2)} ***")
except Exception as err:
    raise err
