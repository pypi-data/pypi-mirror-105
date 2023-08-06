import io
from typing import Union, List, Tuple
from xmlrpc.client import ServerProxy

import pandas as pd

server = ServerProxy("http://192.168.2.179:8999", allow_none=True)


def from_string_to_dataframe(df, list_name):
    df = pd.read_fwf(io.StringIO(df))
    df.to_csv('data.csv')
    result_df = pd.read_csv('data.csv')
    result_df = result_df.iloc[:, 2:].set_index(list_name)
    return result_df


def get_stock_universe(start_date: str, end_date: str, name: str = 'TOP2000'):
    df = server.get_stock_universe1(start_date, end_date, name)
    return from_string_to_dataframe(df, ['ds'])


def get_stock_suspend(start_date: str, end_date: str, source='file'):
    df = server.get_stock_suspend1(start_date, end_date, source)
    return from_string_to_dataframe(df, ['ds'])


def get_st_universe(start_date: str, end_date: str):
    df = server.get_st_universe1(start_date, end_date)
    return from_string_to_dataframe(df, ['ds'])


def get_stock_daily(start_date: str, end_date: str, code: list = None, field: list = None, n_jobs=False,
                    source='file'):
    df = server.get_stock_daily1(start_date, end_date, code, field, n_jobs, source)
    return from_string_to_dataframe(df, ['ds', 'code', 'time'])


def get_stock_bar(start_date: str, end_date: str, freq: str = '1min', code: list = None, field: list = None,
                  n_jobs=False, source='file'):
    df = server.get_stock_bar1(start_date, end_date, freq, code, field, n_jobs, source)
    return from_string_to_dataframe(df, ['ds', 'code', 'time'])


def get_stock_moneyflow(start_date: str, end_date: str, code: list = None, field: list = None, n_jobs=False):
    df = server.get_stock_moneyflow1(start_date, end_date, code, field, n_jobs)
    return from_string_to_dataframe(df, ['ds', 'code', 'time'])


def get_stock_snapshot(date: str, code: list = None, field: list = None, source: str = 'default', fillna: str = None,
                       tick_sample: str = None, remove_auction: bool = False, remove_invalid_code: bool = False,
                       trade_disorder_fix: bool = False, remove_suspend: bool = False,
                       remove_invalid_time: bool = True):
    df = server.get_stock_snapshot1(date, code, field, source, fillna, tick_sample, remove_auction, remove_invalid_code,
                                    trade_disorder_fix, remove_suspend, remove_invalid_time)
    return from_string_to_dataframe(df, ['ds', 'code', 'time'])


def get_stock_transaction(date: str, code: list = None, field: list = None, source='default', remove_invalid_code=True):
    df = server.get_stock_transaction1(date, code, field, source, remove_invalid_code)
    return from_string_to_dataframe(df, ['ds', 'code', 'time'])


def get_stock_order(date: str, code: list = None, field: list = None, source='default', remove_invalid_code=True):
    df = server.get_stock_order1(date, code, field, source, remove_invalid_code)
    return from_string_to_dataframe(df, ['ds', 'code', 'time'])


def get_stock_finindicator(start_date: str, end_date: str, code: list = None, field: list = None, n_jobs=False):
    df = server.get_stock_finindicator1(start_date, end_date, code, field, n_jobs)
    return from_string_to_dataframe(df, ['ds', 'code'])


def get_stock_shares(start_date: str, end_date: str, code: list = None, field: list = None, n_jobs=False):
    df = server.get_stock_shares1(start_date, end_date, code, field, n_jobs)
    return from_string_to_dataframe(df, ['ds', 'code'])


def get_future_basic():
    df = server.get_future_basic1()
    return from_string_to_dataframe(df, ['code'])


def get_future_daily(start_date: str, end_date: str, code: list = None, field: list = None):
    df = server.get_future_daily1(start_date, end_date, code, field)
    return from_string_to_dataframe(df, ['ds', 'code'])


def get_future_snapshot(date: str, codes: Union[str, Tuple, List[str], None] = None,
                        field: [str, Tuple[str], List[str]] = None,
                        fillna: str = None, sample_freq: Union[str, None] = "3s",
                        keep_trading_hours: bool = True, remove_abnormal: bool = True,
                        invalid_contract: str = "skip"):
    df = server.get_future_snapshot1(date, codes, field, fillna, sample_freq, keep_trading_hours, remove_abnormal,
                                     invalid_contract)
    return from_string_to_dataframe(df, ['ds', 'code', 'time'])


def get_future_bar(start_date: str, end_date: str, code: list = None,
                   freq: str = '5min', field: list = None, n_jobs=False):
    df = server.get_future_bar1(start_date, end_date, code, freq, field, n_jobs)
    return from_string_to_dataframe(df, ['ds', 'code', 'time'])


def get_index_contituents(start_date: str, end_date: str, index_name: list = None, version='v1'):
    df = server.get_index_contituents1(start_date, end_date, index_name, version)
    return from_string_to_dataframe(df, ['index_name', 'ds'])


def get_index_constituents(start_date: str, end_date: str, index_name: list = None, version='v1'):
    df = server.get_index_constituents1(start_date, end_date, index_name, version)
    return from_string_to_dataframe(df, ['index_name', 'ds'])


def get_index_daily(start_date: str, end_date: str, index_name: list = None, field: list = None):
    df = server.get_index_daily1(start_date, end_date, index_name, field)
    return from_string_to_dataframe(df, ['ds', 'index_name'])


def get_stock_industry(start_date: str, end_date: str, industry_name: str = None):
    df = server.get_stock_industry1(start_date, end_date, industry_name)
    return from_string_to_dataframe(df, ['industry_name', 'ds'])

