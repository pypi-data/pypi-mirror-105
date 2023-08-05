import websockets
import aiomysql
import json
import sys
from datetime import datetime
from typing import List, Mapping
from pymysql import OperationalError
from websockets.exceptions import WebSocketException
from quotesaggregator import settings
from quotesaggregator.utils import logger, Candlestick


class Aggregator:
    """Class responsible for aggregating the data received from the api, generating the candles
    and saving them in the database

    Attributes:

    - :class:`Mapping[int, List[Candlestick]]` __currencies:
    It is a key-value collection where the key is the currency id and the value is a list that has 3 candlesticks,
    the first of which records values every 1 minute, the second every 5 minutes and the last 10 in 10 minutes.
    After the end of each period, the candlestick is saved in the database and their values overwritten.
    """
    __currencies: Mapping[int, List[Candlestick]]

    def __init__(self, loop):
        self.__currencies = {}
        self.loop = loop

    async def save_in_db(self, candle: Candlestick, currency_id: int) -> None:
        """ Saves candlestick in the database

        :param candle: A candlestick with all attributes filled in
        :param currency_id: currency id according to the poloniex table
        """
        try:
            await logger.info("Saving candle")
            conn = await aiomysql.connect(host=settings.DB_HOST, port=int(settings.DB_PORT),
                                          user=settings.DB_USER, password=settings.DB_PASSWORD,
                                          db=settings.DB_NAME, loop=self.loop, autocommit=True)
            async with conn.cursor() as cur:
                # Make SQL query:
                statement = """INSERT INTO `candlestick` VALUES(default, {}, {}, '{}', 
                            {:10.8f}, {:10.8f}, {:10.8f}, {:10.8f})
                            """.format(currency_id, candle.frequency,
                                       candle.date_time.strftime('%Y-%m-%d %H:%M:%S'), candle.open,
                                       candle.low, candle.high, candle.close)
                await cur.execute(statement)
            conn.close()
            await logger.info("Candle saved")
        except TypeError:
            await logger.fatal("The database access configuration has not been defined. Add the environment variables.")
            sys.exit(1)
        except OperationalError as err:
            await logger.fatal(f"An error occurred while accessing the database\n{err.args[0]} - {err.args[1]}")
            exit(1)

    async def run(self) -> None:
        """ Run aggregator """
        logger.info("Program initialized")
        uri = settings.URI
        try:
            async with websockets.connect(uri) as websocket:
                command = settings.COMMAND
                # Send command to websocket to subscribe on channel:
                await websocket.send(command)
                while True:
                    data_str = await websocket.recv()
                    # Parse data:
                    ticker = json.loads(data_str)
                    # Verify if message is an updating a currency:
                    if len(ticker) == 3:
                        # Checks whether the update received is for a chosen currency:
                        if settings.currency_pair.get(ticker[2][0]) is not None:
                            await logger.info("Received value")
                            await self.process_ticker(ticker[2], datetime.now(settings.TIMEZONE))
        except WebSocketException:
            await logger.fatal("Unable to connect to the server, aborted")
            sys.exit(1)

    async def process_ticker(self, ticker: List[int], date_time: datetime) -> None:
        """ It takes the currency value instantly and processes it to be used in a candlestick.

        The value will be saved in the `currencies` attribute if it is a maximum, minimum, opening or closing
        value for a candle.

        :param ticker: An array received from Poloniex API
        :param date_time: Date and time the currency value was received
        """
        # To facilitate the reading and understanding of the code:
        currency_id = ticker[0]
        instant_value = float(ticker[1])
        await logger.info(f"Processing candle, candle {self.__currencies.get(currency_id, None)}")
        # Initially, there will be no candles for the currencies variable, so it will be created:
        if self.__currencies.get(currency_id) is None:
            self.__currencies[currency_id] = [
                # Values are added at the beginning to ensure that all fields are completed and comparable
                # (eg, high, low):
                Candlestick(frequency=1, date_time=date_time, open=instant_value, close=instant_value,
                            low=instant_value, high=instant_value),
                Candlestick(frequency=5, date_time=date_time, open=instant_value, close=instant_value,
                            low=instant_value, high=instant_value),
                Candlestick(frequency=10, date_time=date_time, open=instant_value, close=instant_value,
                            low=instant_value, high=instant_value),
            ]
        candles_frequencies_list = self.__currencies.get(currency_id)
        # Takes the candles of 1, 5, and 10 minutes respectively of the currency received
        for candle in candles_frequencies_list:
            # The candle will only be saved when the cycle ends. Then the rest of the module of the ticker with
            # frequency received must be equal to zero, in addition the minutes cannot be the same.
            # They are not saved before the cycle is closed.
            if date_time.minute != candle.date_time.minute and date_time.minute % candle.frequency == 0:
                minute = candle.date_time.minute - (candle.date_time.minute % candle.frequency)
                candle.date_time = datetime(candle.date_time.year, candle.date_time.month, candle.date_time.day,
                                            candle.date_time.hour, minute)
                frequency = candle.frequency
                open_value = candle.close
                # Creates a copy, this is necessary because copy() method returns a dict, not a Candlestick,
                # in addition, if it is not copied the value is changed before being saved in the database
                await self.save_in_db(Candlestick.from_dict(candle.to_dict()), currency_id)
                # Clean the candle and add close value of the previous candle
                candle.overwrite(frequency, date_time, open_value, open_value, open_value, open_value)

            if candle.high < instant_value:
                candle.high = instant_value
            elif candle.low > instant_value:
                candle.low = instant_value
            # It will be considered the last value of the period
            candle.close = instant_value
