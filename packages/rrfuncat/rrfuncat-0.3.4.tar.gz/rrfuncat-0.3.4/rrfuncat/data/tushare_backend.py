# -*- coding: utf-8 -*-

from cached_property import cached_property

import tushare as ts

from rrfuncat.data.backend import DataBackend
from rrfuncat.utils import lru_cache, get_str_date_from_int, get_int_date
from rrfuncat.utils import setting


class TushareDataBackend(DataBackend):

    @cached_property
    def pro(self):
        try:
            token = setting['TSORO_TOKEN']
            pro = ts.pro_api(token)
            return pro
        except ImportError:
            print("-" * 50)
            print(">>> Missing tushare. Please run `pip install tushare && set_token`")
            print("-" * 50)
            raise

    @cached_property
    def stock_basics(self):
        return self.pro.stock_basic()


    @cached_property
    def code_name_map(self):
        code_name_map = self.stock_basics.set_index('symbol')[["name"]].to_dict()["name"]
        return code_name_map


    def convert_code(self, order_book_id):
        return order_book_id.split(".")[0]

    def convert_tscode(self, order_book_id):
        ts_code =  order_book_id.replace(".XSHG",".SH") if order_book_id.endswith(".XSHG") else \
            order_book_id.replace(".XSHE", ".SZ")
        return ts_code

    @lru_cache(maxsize=4096)
    def get_price(self, order_book_id, start, end, freq='D'):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        tscode = self.convert_tscode(order_book_id)
        asset= "E"
        if ((order_book_id.startswith("0") and order_book_id.endswith(".XSHG")) or
            (order_book_id.startswith("3") and order_book_id.endswith(".XSHE"))
            ):
            asset = "I" 
        #print(asset, freq)
        df = ts.pro_bar(ts_code=tscode, start_date=start, end_date=end, freq=freq, asset=asset)
        del df["ts_code"]
        arr = df.to_records()

        return arr

    @lru_cache()
    def get_order_book_id_list(self):
        """获取所有的股票代码列表
        """
        info = self.pro.stock_basic().set_index('symbol')
        code_list = info.index.sort_values().tolist()
        order_book_id_list = [
            (code + ".XSHG" if code.startswith("6") else code + ".XSHE")
            for code in code_list
        ]
        return order_book_id_list

    @lru_cache()
    def get_trading_dates(self, start, end):
        """获取所有的交易日
        :param start: 20160101
        :param end: 20160201
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        df = ts.pro_bar(ts_code="000001.SH", asset="I", start_date=start, end_date=end)
        trading_dates = [get_int_date(date) for date in df.trade_date.tolist()]
        return trading_dates

    @lru_cache(maxsize=4096)
    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        code = self.convert_code(order_book_id)
        return "{}[{}]".format(order_book_id, self.code_name_map.get(code))


if __name__ == "__main__":
    fc = TushareDataBackend()

    print(fc.pro)
    print(fc.stock_basics)
    print(fc.get_price(order_book_id='000001.XSHE',start='20210101',end='20210507'))
     
    #print(fc.get_order_book_id_list())
    #print(fc.get_trading_dates(20210101,20210508))
    print(fc.symbol('300146.XSHE'))
    #print(ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011', freq='D'))
