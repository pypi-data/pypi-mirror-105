# -*- coding: utf-8 -*-


import pkgutil

__version__ = pkgutil.get_data(__package__, 'VERSION.txt').decode('ascii').strip()

version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))

__main_version__ = "%s.%s.x" % (version_info[0], version_info[1])

del pkgutil

from rrfuncat.api import *
from rrfuncat.indicators import *

from rrfuncat.data.tushare_backend import TushareDataBackend
from rrfuncat.context import ExecutionContext as funcat_execution_context

funcat_execution_context(date=20190104,
                         order_book_id="000001.XSHG",
                         data_backend=TushareDataBackend())._push()


