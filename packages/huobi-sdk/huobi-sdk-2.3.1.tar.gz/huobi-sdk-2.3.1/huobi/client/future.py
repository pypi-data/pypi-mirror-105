from huobi.constant.system import HUOBI_FUTURE_URL
from huobi.service.future.get_contract_info import GetContractInfoService
from huobi.service.future.get_contract_balance_valuation import GetContractBalanceValuationService
from huobi.service.future.get_contract_account_info import GetContractAccountInfoService
from huobi.service.future.get_contract_position_info import GetContractPositionInfoService
from huobi.utils.dict_util import remove_key


class FutureClient:
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

    def get_contract_info(self, symbol=None, contract_type=None, contract_code=None):
        """
        symbol	string	false	支持大小写，"BTC","ETH"...
        contract_type	string	false	合约类型: （this_week:当周 next_week:下周 quarter:当季 next_quarter:次季）
        contract_code	string	false	BTC180914
        如果不填，默认查询所有所有合约信息;
        如果contract_code填了值，那就按照contract_code去查询;
        如果contract_code没有填值，则按照symbol+contract_type去查询;
        """
        params = locals()
        return GetContractInfoService(remove_key(params)).request(**self.__kwargs)

    def get_contract_balance_valuation(self, valuation_asset=None):
        """
        获取账户总资产估值
        valuation_asset	false	string	资产估值币种，即按该币种为单位进行估值，不填默认"BTC"	"BTC","USD","CNY","EUR","GBP","VND","HKD","TWD","MYR","SGD","KRW","RUB","TRY"
        """
        params = locals()
        return GetContractBalanceValuationService(remove_key(params)).request(**self.__kwargs)

    def get_contract_account_info(self, symbol=None):
        """
        获取用户账户信息
        symbol	false	string	品种代码		支持大小写,"BTC","ETH"...如果缺省，默认返回所有品种
        """
        params = locals()
        return GetContractAccountInfoService(remove_key(params)).request(**self.__kwargs)

    def get_contract_position_info(self, symbol=None):
        """
        获取账户持仓信息
        symbol	false	string	品种代码		支持大小写,""BTC","ETH"...如果缺省，默认返回所有品种
        备注:
        如果有某个品种在结算中，不带请求参数去查询持仓，
        会返回错误码1080(1080 In settlement or delivery. Unable to get positions of some contracts. )。
        建议您带上请求参数去查询持仓，避免报错查询不到持仓。
        """
        params = locals()
        return GetContractPositionInfoService(remove_key(params)).request(**self.__kwargs)

