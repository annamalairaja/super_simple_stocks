from datetime import datetime

from super_simple_stocks import (TickerSymbol,
                                 BuySellIndicator,
                                 Trade,
                                 Stock,
                                 CommonStock,
                                 PreferredStock)

STOCKS = (
    (TickerSymbol.TEA, CommonStock, 0.0, None, 100.0),
    (TickerSymbol.POP, CommonStock, 8.0, None, 100.0),
    (TickerSymbol.ALE, CommonStock, 23.0, None, 60.0),
    (TickerSymbol.GIN, PreferredStock, 8.0, 0.02, 100.0),
    (TickerSymbol.JOE, CommonStock, 13.0, None, 250.0)
)

TRADES = (
    (TickerSymbol.TEA, '1929-10-24T09:30:01', 500, 80.0, BuySellIndicator.BUY),
    (TickerSymbol.TEA, '1929-10-24T09:35:00', 2560, 72.0, BuySellIndicator.BUY),
    (TickerSymbol.TEA, '1929-10-24T09:41:23', 750, 78.0, BuySellIndicator.BUY),
    (TickerSymbol.TEA, '1929-10-24T09:53:40', 1750, 77.5, BuySellIndicator.BUY),
    (TickerSymbol.TEA, '1929-10-24T10:22:38', 250, 81.0, BuySellIndicator.BUY),
    (TickerSymbol.GIN, '1929-10-24T09:45:13', 170, 102.0, BuySellIndicator.BUY),
    (TickerSymbol.GIN, '1929-10-24T10:10:10', 220, 101.0, BuySellIndicator.BUY),
    (TickerSymbol.GIN, '1929-10-24T10:12:30', 350, 98.0, BuySellIndicator.BUY),
    (TickerSymbol.GIN, '1929-10-24T10:13:05', 80, 100.0, BuySellIndicator.BUY),
)


class TradeFactory:

    @staticmethod
    def get_trades(n: int = len(TRADES) - 1) -> [Trade]:
        trades = []
        for trade_data in TRADES[0:n + 1]:
            trade = TradeFactory.from_tuple(trade_data)
            trades.append(trade)

        return trades

    @staticmethod
    def get_trade() -> Trade:
        return next(iter(TradeFactory.get_trades(1)))

    @staticmethod
    def get_trades_for_stock(ticker_symbol: TickerSymbol,
                             n: int = len(TRADES) - 1):
        return [trade for trade in TradeFactory.get_trades()
                if trade.ticker_symbol is ticker_symbol][:n + 1]

    @staticmethod
    def get_trade_for_stock(ticker_symbol: TickerSymbol):
        return next(iter(TradeFactory.get_trades_for_stock(ticker_symbol)))

    @staticmethod
    def from_tuple(trade_data: tuple) -> Trade:
        datetime_str_format = '%Y-%m-%dT%H:%M:%S'
        return Trade(ticker_symbol=trade_data[0],
                     timestamp=datetime.strptime(trade_data[1],
                                                 datetime_str_format),
                     quantity=trade_data[2],
                     price_per_share=trade_data[3],
                     buy_sell_indicator=trade_data[4])


class StockFactory:

    @staticmethod
    def get_stocks(n: int = len(STOCKS) - 1) -> [Stock]:

        stocks = []
        for stock_data in STOCKS[0:n + 1]:

            ticker_symbol = TickerSymbol(stock_data[0])
            par_value = stock_data[4]
            cls = stock_data[1]

            if cls is CommonStock:
                dividend = stock_data[2]
            elif cls is PreferredStock:
                dividend = stock_data[3]
            else:
                raise ValueError()

            stock = cls(ticker_symbol,
                        par_value,
                        dividend)
            stocks.append(stock)

        return stocks

    @staticmethod
    def get_stock() -> Stock:
        return next(iter(StockFactory.get_stocks(1)))

    @staticmethod
    def get_stock_by_ticker_symbol(ticker_symbol: TickerSymbol):
        return next(stock for stock in StockFactory.get_stocks()
                    if stock.ticker_symbol is ticker_symbol)

    @staticmethod
    def get_zero_dividend_stock() -> Stock:
        return next(stock for stock in StockFactory.get_stocks()
                    if stock.dividend == 0)

    @staticmethod
    def get_common_stock() -> CommonStock:
        return next(stock for stock in StockFactory.get_stocks()
                    if isinstance(stock, CommonStock))

    @staticmethod
    def get_preferred_stock() -> PreferredStock:
        return next(stock for stock in StockFactory.get_stocks()
                    if isinstance(stock, PreferredStock))
