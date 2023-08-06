from huobi.service.coin_margined_swap.get_balance_valuation import GetBalanceValuationService
from huobi.service.coin_margined_swap.get_swap_account_info import GetSwapAccountInfoService
from huobi.service.coin_margined_swap.get_swap_position_info import GetSwapPositionInfoService
from huobi.constant.system import HUOBI_FUTURE_URL
from huobi.utils.dict_util import remove_key


class CoinMarginedSwapClient:
    def __init__(self, **kwargs):
        """
        Create the request client instance.
        :param kwargs: The option of request connection.
            api_key: The public key applied from Huobi.
            secret_key: The private key applied from Huobi.
            url: The URL name like "https://api.huobi.pro".
            init_log: Init logger, default is False, True will init logger handler
        """
        kwargs.update({
            "url": HUOBI_FUTURE_URL
        })
        self.__kwargs = kwargs

    def get_balance_valuation(self, valuation_asset: str):
        """
        获取账户总资产估值
        :param valuation_asset: 资产估值币种，即按该币种为单位进行估值，不填默认"BTC"
        """
        return GetBalanceValuationService(remove_key(locals())).request(**self.__kwargs)

    def get_swap_account_info(self, contract_code: str):
        """
        contract_code	false	string	支持大小写, "BTC-USD"... ,如果缺省，默认返回所有合约
        """
        return GetSwapAccountInfoService(remove_key(locals())).request(**self.__kwargs)

    def get_swap_position_info(self, contract_code: str):
        """
        contract_code	false	string	合约代码		支持大小写，"BTC-USD"... ,如果缺省，默认返回所有合约
        """
        return GetSwapPositionInfoService(remove_key(locals())).request(**self.__kwargs)








