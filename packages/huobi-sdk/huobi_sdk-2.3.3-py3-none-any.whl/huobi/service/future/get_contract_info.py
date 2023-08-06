from huobi.service.base import BaseService
from huobi.connection.restapi_sync_client import RestApiSyncClient
from huobi.constant.system import HttpMethod


class GetContractInfoService(BaseService):
    def request(self, **kwargs):
        channel = "/api/v1/contract_contract_info"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.GET, channel, self.params, self.parse)
