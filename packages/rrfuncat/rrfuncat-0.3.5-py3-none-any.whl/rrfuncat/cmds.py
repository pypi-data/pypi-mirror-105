import click

from rrfuncat import *

@click.group()
def cli():
    """
    rrfuncat -h --help
    rrfuncat version
    rrfuncat  indicator --code '000001' / --index '000001'
    """
    pass

@cli.command()
def version():
    from .get_version import version
    click.echo(version())


@cli.command()
def indicator():

    from rrfuncat.data.tushare_backend import TushareDataBackend
    set_data_backend(TushareDataBackend())
    set_start_date("2015-01-01")
    
    S("000001.XSHE")  # 设置当前关注股票
    T("2016-06-01")   # 设置当前观察日期        

    click.echo(C)
    click.echo(f" pct_chg: {C / C[1]}")
    click.echo(MA(C,120))


cli()
