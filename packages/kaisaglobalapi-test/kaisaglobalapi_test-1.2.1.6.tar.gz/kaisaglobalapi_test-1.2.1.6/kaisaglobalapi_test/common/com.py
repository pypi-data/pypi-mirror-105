# -*- coding:utf-8 -*-

# ===================================================================
# This file is used to store all paths and URLs in the interface document
# KaisaGlobal rights are reserved.
# ===================================================================


"""
This code provide utils function for KaisaGlobal-Open.
developed by KaisaGlobal quant team.
2021.03.02
"""
appendIpAddress = "192.168.1.1"
# appendIpAddress = None

# REAL ENV.
KAISA_ROOT_URL = "kgl.jt00000.com"
KAISA_ROOT_URL_SIM = "sit-kgl.jt00000.com"
# KAISA_ROOT_URL = KAISA_ROOT_URL_SIM
KAISA_ROOT_URL_API = "openapi.jt00000.com"
#
CRYPTO_RSA_URL = "https://__kaisarooturl__/kgl-third-authorization/crypto/key/RSA"
AUTHENTICA_URL = "https://__kaisarooturl__/kgl-third-authorization/oauth/token"
# AUTHENTICA_URL = "https://openapi.jt00000.com"
QUOTE_URL = "https://kgl.jt00000.com/hq"

# WEBSOCKET_DATA_HOST = "ws://__kaisarooturl__/dz_app_ws/ws"
WEBSOCKET_DATA_HOST = "ws://sit-kgl.jt00000.com/dz_app_ws/ws"
REST_DATA_HOST = "https://__kaisarooturl__/dzApp/dzHttpApi"

TRADE_CRYPTO_RSA_URL = "https://__kaisarooturl__/kgl-trade-service/crypto/key/RSA"
ClientByMobile_URL = "https://__kaisarooturl__/kgl-user-center/userOaccAccount/selectClientIdByMobile"
REST_HOST = "https://__kaisarooturl__/kgl-trade-service"
WEBSOCKET_TRADE_HOST = "wss://__kaisarooturl__/kgl-trade-push-service/ws"

openapi_scope = "wthk"
openapi_scope = "read"
# < 2120-04-07 => "https://sit-kgl.jt00000.com/kgl-stock-push-provider"
# > 2120-04-07 => https://sit-kgl.jt00000.com/kgl-stock-support-provider
#
MARKET_POST_URL = "https://sit-kgl.jt00000.com/kgl-stock-support-provider"
# 实时行情接口URL
MARKET_WS_URL = "ws://sit-stock-gateway.jt00000.com/stock-front/stock"   #"ws://uat-stock.jt00000.com/stock"

# 港股tick历史数据URL
HK_STOCK_TICK_POST_URL = 'https://sit-kgl.jt00000.com/kgl-stock-support-provider/stock/quote/tickHistory/v2'
# 港股KLine历史数据URL
HK_STOCK_KLINE_POST_URL = 'https://sit-kgl.jt00000.com/kgl-stock-support-provider/quoteInfo/kLineHistory/v2'
# 港股盘口十档历史数据URL
HK_STOCK_LEVEL2_10_ORDER_URL = 'https://sit-kgl.jt00000.com/kgl-stock-support-provider/quoteInfo/orderBuySellHisList/v2'
# 港股经纪人历史数据URL
HK_STOCK_BROKER_URL = 'https://sit-kgl.jt00000.com/kgl-stock-support-provider/quoteInfo/brokerHisList/v2'


# 基础财务指标URL, Post
BASIC_FIN_POST_URL = "https://sit-kgl.jt00000.com/kgl-glidata-center/stockReport/finReport"
# 衍生财务指标URL，Post
EX_FIN_POST_URL = "http://sit-kgl.jt00000.com/kgl-stock-front-stoacq/openapi/financial/factor"
# 基础/衍生技术面因子URL，Post
BE_TECH_POST_URL = "http://sit-kgl.jt00000.com/kgl-stock-front-stoacq/openapi/stock/techindex"

START_PUSH = 200
STOP_PUSH = 201
SYNCHRONIZE_PUSH = 250
QUERY_HISTORY = 36
QUERY_CONTRACT = 52
ON_TICK = 251
ON_MARKETDATA = 153
PING = 2
PONG = 3
LOGIN = 10
HKSE_MARKET = 2002

CREATION = 101
UPDATE = 102
TRADE = 103
CANCELLATION = 104
ACCOUT = 106
POSITION = 105

