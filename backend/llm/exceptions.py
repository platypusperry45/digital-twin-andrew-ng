"""
LLM specific exceptions.
"""


class LLMException(Exception):
    """
    Base LLM exception.
    """
    pass



class AllKeysExhaustedError(
    LLMException
):
    """
    Raised when all API keys fail.
    """

    pass



class ModelUnavailableError(
    LLMException
):
    """
    Raised when model fallback fails.
    """

    pass