from huobi.connection.restapi_sync_client import RestApiSyncClient
from huobi.constant.system import HttpMethod
from huobi.service.base import BaseService


class GetBalanceValuationService(BaseService):
    def request(self, **kwargs):
        channel = "/swap-api/v1/swap_balance_valuation"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, self.parse)
