

class DefaultException(Exception):

    def __init__(self, data):
        self.code: int = data.get('code', 0)
        self.error_list: [] = data.get('errorList', [])
        self.is_ko: bool = data.get('isKo', False)
        self.is_ok: bool = data.get('isOk', True)
        self.is_warn: bool = data.get('isWarn', False)
        self.message: bool = data.get('message', '')

    def __str__(self):
        return f'code: {self.code} message: {self.message}'


class NetworkError(Exception):
    pass


class InvalidLicenseError(Exception):

    def __init__(self, capabilities):
        self.capabilities = capabilities

    def __str__(self):
        return f'You are missing some capabilities to perform this action: {self.capabilities}'


class UnauthorizedError(DefaultException):
    pass


class InvalidParametersError(DefaultException):
    pass


class NotFoundError(DefaultException):
    pass


class MaxRequestsExceededError(DefaultException):
    pass


class GenericError(DefaultException):
    pass


class NotAvailableError(DefaultException):
    pass
