# -*- coding: utf-8 -*-

from datetime import datetime
from cached_property import cached_property
import pandas as Series
import numpy as np
import tushare as ts

from rrfuncat.data.backend import DataBackend
from rrfuncat.utils import lru_cache, get_str_date_from_int, get_int_date, get_date_from_int
from rrfuncat.utils import setting


class TushareDataBackend(DataBackend):
    """ 
    目前仅支持日数据
    """
    @cached_property
    def pro(self):
        try:
            token = setting['TSPRO_TOKEN']
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
        code =  order_book_id.split(".")[0]
        ts_code = code + ".SH" if code.startswith("6") else code + ".SZ"
        return ts_code


    @lru_cache(maxsize=4096)
    def get_price(self, order_book_id, start, end, freq, **kwargs):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start_date = get_str_date_from_int(start)
        end_date = get_str_date_from_int(end)
        tscode = self.convert_tscode(order_book_id)
        print(start, end, tscode)
        asset= "E"
        if ((order_book_id.startswith("000") and order_book_id.endswith(".XSHG")) or
            (order_book_id.startswith("399") and order_book_id.endswith(".XSHE"))    #?????
            ):
            asset = "I" 
        #print(asset, freq)
        #order_book_id_list = [code + ".XSHG" if code.startswith("6") else code + ".XSHE" for code in code_list]
        #dates = map(lambda x: str(x)[:4] + '-' + str(x)[4:6] + '-' + str(x)[6:], dates)
        df = ts.pro_bar(ts_code=tscode, start_date=start_date, end_date=end_date, freq=freq, asset=asset)

        df.sort_values(by='trade_date', inplace=True)
        df['date'] = df['trade_date'].apply(lambda x : str(x)[:4] + '-' + str(x)[4:6] + '-' + str(x)[6:])
        df["datetime"] = df["date"].apply(lambda x: int(x.replace("-", "")) * 1000000)
        df['volume'] = df['vol']
        df = df[['date', 'open', 'close', 'high', 'low', 'volume','datetime']]
        print(df)
        arr = df.to_records()
        #print(df.columns)
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


    @lru_cache(maxsize=4096)
    def get_shares(self, order_book_id, start_date, end_date, fields=None):
        """
        获取某只股票在一段时间内的流通情况
        :param order_book_id: 需要查询的资产代码
        :param start_date: 查询的起始日期 20180504
        :param end_date: 查询的截止日期 20180601
        :param fields: total 总股本；circulation_a 流通A股；management_circulation 已流通高管持股；
        non_circulation_a 非流通A股合计；total_a A股总股本
        :return: pd.Series
        """
        dates = self.trading_dates[self.trading_dates >= start_date]
        dates = dates[dates <= end_date]
        dates = map(lambda x: str(x)[:4] + '-' + str(x)[4:6] + '-' + str(x)[6:], dates)
        if fields == 'total_a':
            col_name = 'totals'
        else:
            col_name = 'outstanding'
        code = self.convert_code(order_book_id)
        result_series = Series()
        for date in dates:
            try:
                temp = self.ts.get_stock_basics(date)[col_name][code]
            except:
                temp = np.nan
            result_series[date] = temp
        return result_series


if __name__ == "__main__":
    fc = TushareDataBackend()

    #print(fc.pro)
    #print(fc.stock_basics)
    
    print(fc.get_price(order_book_id='399001.XSHE',start='20210501',end='20210512', freq="D")) 
    #print(fc.get_order_book_id_list())
    #print(fc.get_trading_dates(20210101,20210508))
    #print(fc.symbol('300146.XSHE'))
    #print(ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011', freq='D'))
