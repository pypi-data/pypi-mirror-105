import asyncio
from quotesaggregator import aggregator


def run_forever_async():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aggregator.Aggregator(loop).run())


if __name__ == '__main__':
    run_forever_async()
