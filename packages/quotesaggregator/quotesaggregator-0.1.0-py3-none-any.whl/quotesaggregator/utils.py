from prodict import Prodict
from datetime import datetime
import aiologger


class Candlestick(Prodict):
    """ An object similar to a dictionary to make it easier to read the code """
    frequency: int
    date_time: datetime
    open: float
    close: float
    low: float
    high: float

    def overwrite(self, frequency: int, date_time: datetime, open: float, close: float, low: float, high: float):
        """ Overwrite attributes """
        self.frequency = frequency
        self.date_time = date_time
        self.open = open
        self.close = close
        self.low = low
        self.high = high


# Logger
logger = aiologger.Logger.with_default_handlers(level=10)
