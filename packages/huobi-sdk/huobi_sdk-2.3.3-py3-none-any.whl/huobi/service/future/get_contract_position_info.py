from huobi.service.base import BaseService
from huobi.connection.restapi_sync_client import RestApiSyncClient
from huobi.constant.system import HttpMethod


class GetContractPositionInfoService(BaseService):
    def request(self, **kwargs):
        channel = "/api/v1/contract_position_info"

        return RestApiSyncClient(**kwargs).request_process(HttpMethod.POST_SIGN, channel, self.params, self.parse)
