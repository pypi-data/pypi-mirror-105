# -*- coding: utf-8 -*-


from rrfuncat.api import *
from rrfuncat.indicators import *

from rrfuncat.data.tushare_backend import TushareDataBackend
from rrfuncat.context import ExecutionContext as funcat_execution_context

funcat_execution_context(date=20190104,
                         order_book_id="000001.XSHG",
                         data_backend=TushareDataBackend())._push()


