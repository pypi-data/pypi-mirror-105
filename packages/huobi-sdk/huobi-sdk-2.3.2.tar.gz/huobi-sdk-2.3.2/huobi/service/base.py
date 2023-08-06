class BaseService:
    def __init__(self, params):
        self.params = params

    @staticmethod
    def parse(dict_data):
        return dict_data.get("data", [])
