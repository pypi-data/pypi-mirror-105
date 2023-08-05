import asyncio
from typing import List
from unittest.mock import AsyncMock
import pytest
import mock
from datetime import datetime
from quotesaggregator.utils import Candlestick, logger
from quotesaggregator.aggregator import Aggregator

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@pytest.fixture(scope='session')
def aggregator_stateful():
    return Aggregator(asyncio.get_event_loop())


@pytest.fixture(scope='function')
def aggregator_stateless():
    return Aggregator(asyncio.get_event_loop())


@mock.patch.object(logger, 'info', new=AsyncMock())
async def test_process_ticker_when_value_is_the_highest(aggregator_stateless: Aggregator):
    """ Checks if it identifies the highest value """
    await aggregator_stateless.process_ticker([1, 1], datetime(2021, 5, 1, 1, 1))
    await aggregator_stateless.process_ticker([1, 3], datetime(2021, 5, 1, 1, 1))
    # As currencies is a private attribute, it must be accessed in this way to be able to test it
    currency_frequencies: List[Candlestick] = aggregator_stateless._Aggregator__currencies.get(1)
    for candle in currency_frequencies:
        assert candle.high == 3.0


@mock.patch.object(logger, 'info', new=AsyncMock())
async def test_process_ticker_when_value_is_the_lowest(aggregator_stateless):
    """ Checks if it identifies the lowest value """
    await aggregator_stateless.process_ticker([1, 2], datetime(2021, 5, 1, 1, 1))
    await aggregator_stateless.process_ticker([1, 3], datetime(2021, 5, 1, 1, 1))
    # As currencies is a private attribute, it must be accessed in this way to be able to test it
    currency_frequencies: List[Candlestick] = aggregator_stateless._Aggregator__currencies.get(1)
    for candle in currency_frequencies:
        assert candle.low == 2.0


@mock.patch.object(logger, 'info', new=AsyncMock())
@mock.patch.object(Aggregator, 'save_in_db', new=AsyncMock())
async def test_process_ticker_when_a_single_value_was_sent_to_the_function(aggregator_stateless: Aggregator):
    """ Checks whether the candle is created and added to currencies """
    await aggregator_stateless.process_ticker([1, 2], datetime(2021, 5, 1, 1, 1))
    # As currencies is a private attribute, it must be accessed in this way to be able to test it
    currency_frequencies = aggregator_stateless._Aggregator__currencies.get(1)
    assert currency_frequencies[0].to_dict() == Candlestick(frequency=1, date_time=datetime(2021, 5, 1, 1, 1),
                                                            open=2, close=2, low=2, high=2).to_dict()
    assert currency_frequencies[1].to_dict() == Candlestick(frequency=5, date_time=datetime(2021, 5, 1, 1, 1),
                                                            open=2, close=2, low=2, high=2).to_dict()
    assert currency_frequencies[2].to_dict() == Candlestick(frequency=10, date_time=datetime(2021, 5, 1, 1, 1),
                                                            open=2, close=2, low=2, high=2).to_dict()


@mock.patch.object(logger, 'info', new=AsyncMock())
@mock.patch.object(Aggregator, 'save_in_db', new=AsyncMock())
@pytest.mark.parametrize("value, date_time", [
    ([0, 2], datetime(year=2021, month=5, day=1, hour=1, minute=0)),
    ([0, 1], datetime(year=2021, month=5, day=1, hour=1, minute=0)),
    ([0, 4], datetime(year=2021, month=5, day=1, hour=1, minute=0)),
    ([0, 3], datetime(year=2021, month=5, day=1, hour=1, minute=0)),
    ([0, 1], datetime(year=2021, month=5, day=1, hour=1, minute=1)),
])
async def test_process_ticker_forming_a_one_minute_candle(value: list, date_time: datetime,
                                                          aggregator_stateful: Aggregator):
    """ Checks whether the one-minute candle is valid and sent to be saved """
    await aggregator_stateful.process_ticker(value, date_time)
    aggregator_stateful.save_in_db: AsyncMock
    if aggregator_stateful.save_in_db.called:
        aggregator_stateful.save_in_db.assert_called_with(
            Candlestick(frequency=1, date_time=datetime(year=2021, month=5, day=1, hour=1, minute=0), open=2, close=3,
                        low=1, high=4), 0)


@mock.patch.object(logger, 'info', new=AsyncMock())
@mock.patch.object(Aggregator, 'save_in_db', new=AsyncMock())
@pytest.mark.parametrize("value, date_time", [
    ([2, 2], datetime(year=2021, month=5, day=1, hour=1, minute=0)),
    ([2, 2], datetime(year=2021, month=5, day=1, hour=1, minute=1)),
    ([2, 1], datetime(year=2021, month=5, day=1, hour=1, minute=2)),
    ([2, 4], datetime(year=2021, month=5, day=1, hour=1, minute=3)),
    ([2, 3], datetime(year=2021, month=5, day=1, hour=1, minute=4)),
    ([2, 1], datetime(year=2021, month=5, day=1, hour=1, minute=5)),
])
async def test_process_ticker_forming_a_five_minute_candle(value: list, date_time: datetime,
                                                           aggregator_stateful: Aggregator):
    """ Checks whether the five minute candle is valid and sent to be saved """
    await aggregator_stateful.process_ticker(value, date_time)
    aggregator_stateful.save_in_db: AsyncMock
    if aggregator_stateful.save_in_db.called:
        # there are calls from other cycles that we are not interested in for the test
        if aggregator_stateful.save_in_db.call_count % 5 == 0:
            aggregator_stateful.save_in_db.assert_called_with(
                Candlestick(frequency=5, date_time=datetime(year=2021, month=5, day=1, hour=1, minute=0), open=2,
                            close=3,
                            low=1, high=4), 1)


@mock.patch.object(logger, 'info', new=AsyncMock())
@mock.patch.object(Aggregator, 'save_in_db', new=AsyncMock())
@pytest.mark.parametrize("value, date_time", [
    ([3, 2], datetime(year=2021, month=5, day=1, hour=1, minute=0)),
    ([3, 2], datetime(year=2021, month=5, day=1, hour=1, minute=1)),
    ([3, 1], datetime(year=2021, month=5, day=1, hour=1, minute=2)),
    ([3, 4], datetime(year=2021, month=5, day=1, hour=1, minute=3)),
    ([3, 3], datetime(year=2021, month=5, day=1, hour=1, minute=4)),
    ([3, 3], datetime(year=2021, month=5, day=1, hour=1, minute=6)),
    ([3, 3], datetime(year=2021, month=5, day=1, hour=1, minute=7)),
    ([3, 3], datetime(year=2021, month=5, day=1, hour=1, minute=8)),
    ([3, 3], datetime(year=2021, month=5, day=1, hour=1, minute=9)),
    ([3, 3], datetime(year=2021, month=5, day=1, hour=1, minute=10)),
])
async def test_process_ticker_forming_a_ten_minute_candle(value: list, date_time: datetime,
                                                          aggregator_stateful: Aggregator):
    """ Checks whether the ten minute candle is valid and sent to be saved """
    await aggregator_stateful.process_ticker(value, date_time)
    aggregator_stateful.save_in_db: AsyncMock
    if aggregator_stateful.save_in_db.called:
        # there are calls from other cycles that we are not interested in for the test
        if aggregator_stateful.save_in_db.call_count % 10 == 0:
            aggregator_stateful.save_in_db.assert_called_with(
                Candlestick(frequency=10, date_time=datetime(year=2021, month=5, day=1, hour=1, minute=0), open=2,
                            close=3,
                            low=1, high=4), 3)


@mock.patch.object(logger, 'info', new=AsyncMock())
@mock.patch.object(Aggregator, 'save_in_db', new=AsyncMock())
@pytest.mark.parametrize("value, date_time", [
    ([4, 2], datetime(year=2021, month=5, day=1, hour=1, minute=51)),
    ([4, 2], datetime(year=2021, month=5, day=1, hour=1, minute=52)),
    ([4, 1], datetime(year=2021, month=5, day=1, hour=1, minute=53)),
    ([4, 4], datetime(year=2021, month=5, day=1, hour=1, minute=54)),
    ([4, 3], datetime(year=2021, month=5, day=1, hour=1, minute=55)),
    ([4, 3], datetime(year=2021, month=5, day=1, hour=1, minute=56)),
    ([4, 3], datetime(year=2021, month=5, day=1, hour=1, minute=57)),
    ([4, 3], datetime(year=2021, month=5, day=1, hour=1, minute=58)),
    ([4, 3], datetime(year=2021, month=5, day=1, hour=1, minute=59)),
    ([4, 3], datetime(year=2021, month=5, day=1, hour=1, minute=0)),
])
async def test_process_ticker_forming_a_multiple_candles(value: list, date_time: datetime,
                                                         aggregator_stateful: Aggregator):
    """ Checks whether the ten minute candle is valid and sent to be saved """
    await aggregator_stateful.process_ticker(value, date_time)
    aggregator_stateful.save_in_db: AsyncMock
    if aggregator_stateful.save_in_db.called:
        if aggregator_stateful.save_in_db.call_args.args[0].frequency == 1:
            pass
        elif aggregator_stateful.save_in_db.call_count % 5 == 0:
            assert aggregator_stateful.save_in_db.call_args.args[0].frequency == 5
        elif aggregator_stateful.save_in_db.call_count % 10 == 0:
            aggregator_stateful.save_in_db.assert_called_with(
                Candlestick(frequency=10, date_time=datetime(year=2021, month=5, day=1, hour=1, minute=0), open=2,
                            close=3,
                            low=1, high=4), 3)


if __name__ == '__main__':
    pytest.main()


def run():
    pytest.main()
