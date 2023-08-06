from huobi.service.base import BaseService
from huobi.connection.restapi_sync_client import RestApiSyncClient
from huobi.constant.system import HttpMethod


class GetContractAccountInfoService(BaseService):
    def request(self, **kwargs):
        channel = "/api/v1/contract_account_info"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, self.parse)
