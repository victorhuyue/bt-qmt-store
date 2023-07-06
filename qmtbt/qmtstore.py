import random

import backtrader as bt
from backtrader.metabase import MetaParams

from xtquant.xttype import StockAccount
from xtquant.xttrader import XtQuantTrader
from xtquant import xtdata


class MetaSingleton(MetaParams):
    '''Metaclass to make a metaclassed class a singleton'''

    def __init__(cls, name, bases, dct):
        super(MetaSingleton, cls).__init__(name, bases, dct)
        cls._singleton = None

    def __call__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = (
                super(MetaSingleton, cls).__call__(*args, **kwargs))

        return cls._singleton


class QMTStore(object, metaclass=MetaSingleton):
    
    @classmethod
    def getdata(cls, *args, **kwargs):
        '''Returns ``DataCls`` with args, kwargs'''
        return cls.DataCls(*args, **kwargs)

    @classmethod
    def getbroker(cls, *args, **kwargs):
        '''Returns broker with *args, **kwargs from registered ``BrokerCls``'''
        return cls.BrokerCls(*args, **kwargs)
    
    def __init__(self, mini_qmt_path, account):

        self.mini_qmt_path = mini_qmt_path
        self.account = account

        session_id = int(random.randint(100000, 999999))
        xt_trader = XtQuantTrader(self.mini_qmt_path, session_id)

        xt_trader.start()

        connect_result = xt_trader.connect()


        if connect_result == 0:
            print('连接成功')

        acc = StockAccount(account)

        xt_trader.subscribe(acc)

        self.xt_trader = xt_trader

    def _fetch_history(self, symbol, period, start_time='', end_time=''):
        xtdata.download_history_data2(stock_list=[symbol], period=period, start_time=start_time, end_time=end_time)
        df = xtdata.get_market_data(stock_list=[symbol], period=period, start_time=start_time, end_time=end_time)
        return df
    
    def _subscribe_live(self, symbol, period, callback):

        return xtdata.subscribe_quote(stock_code=symbol, period=period, count=0, callback=callback)
    
    def _unsubscribe_live(self, seq):
        xtdata.unsubscribe_quote(seq)
