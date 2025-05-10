from abc import ABC

from src.config.configuration_manager import ConfigurationManager


class AbstractPromptBuilder(ABC):
    """ """

    def __init__(self):
        """ """
        self.configuration_manager = ConfigurationManager()
