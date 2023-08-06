# -*- coding: utf-8 -*-

# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# KaisaGlobal rights are reserved.
# Quote data
# ===================================================================

import sys
from os.path import dirname, abspath
import requests, datetime
import pandas as pd
import numpy as np
import json, time
from com import *
from pub_cls_com import *

def to_get_all_data(body, URL, all_pages):
    # 统一获取数据的接口
    __ = pd.DataFrame()
    for p in range(1, all_pages + 1):
        body['pageNum'] = p
        _values_ = total_handle_hist_data_req(body, URL=URL)
        _t_df_ = pd.DataFrame(_values_)
        __ = pd.concat([__, _t_df_])

    return __

# def only_month_dt_get(start, end, data_tip=''):
#     # 限制一个月
#     day_count = (end - start).days
#     if day_count > 30 * 1: return '您好,{}, 接口一次最多只能提供1个月的数据哟,如果需要更多的数据,请分段获取!'.format(data_tip)


def __handle_hist_data_ex_ret(code_list=['00700'],
                              start_date=None,
                              end_date=None,
                              unit='1d',
                              market=100,
                              page=1,
                              fre='',
                              data_type=None):
    # 获取历史历史K线数据
    try:
        ori_data_type_lsit = ['Kline', 'ticker', 'broker', 'level10']
        if data_type is None or data_type not in ori_data_type_lsit: return "您好, 请正确填写您要提取数据的参数, 如: data_type='Kline'"
        market_dict = {1: ['.SH', '.SZ'], 2: ['.HK'], 3: ['NS', 'QS', 'PS', 'AS', 'BS']}
        #if unit not in ['1d', '1m']: return '您好,接口暂时不提供日级别和1分钟以外的K线数据哟,我们会马不停蹄的加班,尽快把其他频率的数据补全!'

        if market in [3, 1]: return '您好,接口暂时不提供美股/A股的数据哟,我们会马不停蹄的加班,尽快把数据补全!'
        if start_date is None and end_date is None: return '您好,检测到end_date比start_date都是None,请修正后重新请求数据!'
        if start_date is not None and end_date is None:
            end_date = start_date
        if start_date is None and end_date is not None:
            start_date = end_date
        if start_date is not None and end_date is not None:
            if start_date > end_date: return '您好,检测到end_date比start_date要小哟,请修正后重新请求数据!'

        if len(code_list) == 0:return '您好, 请填写您要获取数据的合约代码!'
        code_market_types = market_dict[market]
        tip_codes = [code for code in code_list if code[-3:] not in code_market_types]
        if len(tip_codes) > 0: return '您好, 检测到您填入的合约列表中存在不规范的股票代码,请修改(如: 00700.HK, 000001.SZ, AAPL.QS)后重新请求数据!'
        quote_type_dict = {"1m": 1, "1d": 10}

        s_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        e_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        if data_type == 'Kline':

            if len(code_list) == 1:
                day_count = (e_dt - s_dt).days
                if day_count > 365 * 10: return '您好,单只股票,接口一次最多只能提供10年的数据哟,如果需要更多的数据,请分段获取!'

            if len(code_list) > 1:
                day_count = (e_dt - s_dt).days
                if day_count > 30 * 1: return '您好,多只股票,接口一次最多只能提供1个月的数据哟,如果需要更多的数据,请分段获取!'
            code_list = [code.upper() for code in code_list]

            quote_type_dict_ori = {"1m": 1, "3m": 2, "5m": 3, "10m": 4, "15m": 5, "30m": 6,
                                   "1h": 7, "2h": 8, "4h": 9, "1d": 10, "5d": 11, "1w": 12, "1M": 13, "1q": 14, "1y": 15}

            if unit not in quote_type_dict.keys(): return "您好, 检测到您填写的unit参数不在允许范围内,参考:unit: '1m' or '1d' !"
            pre_dic = {'pre': '1', 'post': '2', 'None': '0'}
            if fre not in pre_dic.keys():return "您好, 请正确填写是否复权参数, 如: fre='pre'"
            fre = pre_dic[fre]
            body_hist = {
                "assetIds": code_list,
                "quoteType": quote_type_dict[unit],
                "startDate": start_date,
                "endDate": end_date,
                "adjFactorType": fre,
                "pageNum": page,
                "pageSize": 1000
            }
            #body_hist['adjFactorType'] = fre
            print('body:{}'.format(body_hist))
            _pages_ = handle_hist_data_req_pages(body=body_hist, URL=HK_STOCK_KLINE_POST_URL)
            print('Kline_hist_data:_pages_:{}'.format(_pages_))
            __ = pd.DataFrame()
            __ = to_get_all_data(body_hist, HK_STOCK_KLINE_POST_URL, _pages_)
            print('Kline返回数据的行数:{}'.format(len(__)))
            __ = __.sort_values(by=['assetId'])
            ori_cols = ['assetId', 'open', 'low', 'high', 'close', 'volume', 'amount', 'timestamp']
            __ = __[ori_cols]
            __['timestamp'] = [change_timestamp(dtt) for dtt in __['timestamp']]
            __.columns = ['code', 'open', 'high', 'low', 'close', 'volume', 'money', 'trading_day']
        else:
            body_any = {
                "assetIds": code_list,
                "startDate": start_date,
                "endDate": end_date,
                "pageNum": page,
                "pageSize": 1000
            }
            if len(code_list) > 1: return "您好, ticker接口限定每次只能拉取一个合约的数据, 请修改(如: code_list=['00700.HK'])参数后重新请求!"
            if data_type == 'ticker':
                URL = HK_STOCK_TICK_POST_URL
                ori_cols = ['assetId', 'now', 'curVolume', 'amount', 'tickFlag', 'tickVi', 'quoteTime']    # 'marketName', 'greyFlag',
                cols = ['code', 'last_price', 'volume', 'money', 'tick_order_type', 'tick_trade_type', 'quote_time']
            elif data_type == 'broker':
                URL = HK_STOCK_BROKER_URL
                ori_cols = ['assetId', 'brokerIdList', 'flag', 'level', 'brokerTime']
                cols = ['code', 'broker_id_list', 'direction', 'level', 'broker_time']
            elif data_type == 'level10':
                URL = HK_STOCK_LEVEL2_10_ORDER_URL
                ori_cols = ['assetId', 'price', 'flag', 'volume', 'brokerCount', 'level', 'quoteTime']
                cols = ['code', 'price', 'direction', 'volume', 'broker_count', 'level', 'quote_time']
            else:
                URL = ''
                ori_cols = []
                cols = []
            day_count = (e_dt - s_dt).days
            if day_count > 30 * 1:
                return '您好,{}数据, 接口一次最多只能提供1个月的数据哟,如果需要更多的数据,请分段获取!'.format(data_type)

            print('body:{}'.format(body_any))
            print('URL:{}'.format(URL))
            _pages_ = handle_hist_data_req_pages(body=body_any, URL=URL)
            print('_pages_:{}'.format(_pages_))
            __ = to_get_all_data(body_any, URL, _pages_)
            print('{}返回数据的行数:{}'.format(data_type, len(__)))
            __ = __.sort_values(by=['assetId'])
            __ = __[ori_cols]
            __.columns = cols
        return __
    except Exception as xp:
        return '您好, 您填入的参数有误:{}, 请检查后重新请求!'.format(xp)




def get_history_kline_data(code_list=['00700.HK'], start_date=None, end_date=None, unit='', market=2, fre='pre'):
    '''
    # 获取合约代码历史区间K线数据
    '''

    __ = __handle_hist_data_ex_ret(code_list,
                                   start_date,
                                   end_date,
                                   unit=unit,
                                   market=market,
                                   page=1,
                                   fre=fre,
                                   data_type='Kline')
    print('获取到的K线数据:{}'.format(__))
    return __

def get_history_ticker_data(code_list=['00700.HK'], start_date=None, end_date=None, market=2):
    '''
    # 获取历史逐笔数据
    '''

    __ = __handle_hist_data_ex_ret(code_list, start_date, end_date, market=market, data_type='ticker')

    print('获取到的ticker数据:{}'.format(__))
    return __

def get_history_broker_data(code_list=['00700.HK'], start_date=None, end_date=None, market=2):
    '''
    # 获取历史经纪商数据
    '''
    __ = __handle_hist_data_ex_ret(code_list, start_date, end_date, market=market, data_type='broker')

    print('获取到的broker数据:{}'.format(__))
    return __

def get_history_level10_data(code_list=['00700.HK'], start_date=None, end_date=None, market=2):
    '''
    # 获取历史Level10档盘口数据
    '''
    __ = __handle_hist_data_ex_ret(code_list, start_date, end_date, market=market, data_type='level10')

    print('获取到的level10数据:{}'.format(__))
    return __

if __name__ == '__main__':
    pass




