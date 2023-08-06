class MalformedUUIDException(Exception):
    """Exception for malformed UUID"""
    pass


class InvalidApiKeyException(Exception):
    """Exception for invalid API keys"""
    pass


class NoContentException(Exception):
    """Exception for HTTP Code 204 (No Content)"""
    pass
