from abc import ABC, abstractmethod


class BaseData:

    def __init__(self, data):
        # the status of the response
        self.status = ResponseStatusData(data)


class WrapperDataInterface(ABC):

    @abstractmethod
    def __init__(self, data: dict, result: dict):
        pass


class ResponseStatusData:

    def __init__(self, data: dict):
        self.code: int = data.get('code', 0)
        self.error_list: [] = data.get('errorList', [])
        self.is_ko: bool = data.get('isKo', False)
        self.is_ok: bool = data.get('isOk', True)
        self.is_warn: bool = data.get('isWarn', False)
        self.message: bool = data.get('message', '')


class AddressData:
    """
    Address nested obj
    """
    def __init__(self, data: dict):
        self.cap: str = data.get('cap', '')
        self.city: str = data.get('city', '')
        self.city_code: str = data.get('cityCode', '')
        self.city_code_istat: str = data.get('cityCodeIstat')
        self.name: str = data.get('name')
        self.number: str = data.get('number')
        self.place_name: str = data.get('placeName')
        self.province: str = data.get('province')
        self.town: str = data.get('town')
