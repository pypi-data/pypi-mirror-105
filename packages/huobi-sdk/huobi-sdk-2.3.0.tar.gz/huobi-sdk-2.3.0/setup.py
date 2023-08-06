#!/usr/bin/env python3
from setuptools import setup

setup(
    name="huobi-sdk",
    version="2.3.0",
    description="forked from https://github.com/HuobiRDCenter/huobi_Python",
    license='Apache',
    packages=['huobi',
              'huobi.exception', 'huobi.constant',
              'huobi.utils',
              'huobi.client',
              'huobi.service', 'huobi.service.account', 'huobi.service.margin', 'huobi.service.market',
              'huobi.service.trade', 'huobi.service.wallet', 'huobi.service.generic', 'huobi.service.etf',
              'huobi.service.subuser', 'huobi.service.algo',
              'huobi.model', 'huobi.model.account', 'huobi.model.margin', 'huobi.model.market', 'huobi.model.trade',
              'huobi.model.wallet', 'huobi.model.generic', 'huobi.model.etf', 'huobi.model.subuser', 'huobi.model.algo',
              'huobi.connection', 'huobi.connection.impl', "performance", "tests"
              ],
    install_requires=[
        'requests == 2.20.1',
        'apscheduler == 3.6.3',
        'websocket-client == 0.57.0',
        'aiohttp == 3.6.2',
        'urllib3'
    ]
)
