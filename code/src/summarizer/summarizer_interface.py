from abc import ABC, abstractmethod
from typing import Dict, List


class SummarizerInterface(ABC):
    """
    Abstract interface for defining the contract for summarizer classes.

    This interface enforces the implementation of a `summarize` method in derived classes,
    ensuring they provide a consistent way to summarize data.
    """

    @abstractmethod
    def summarize(self, data: List[Dict]) -> List[Dict]:
        """
        Abstract method to summarize a collection of data.

        This method takes a list of dictionaries, processes or aggregates the data,
        and returns a summarized version as a list of dictionaries.

        Args:
            data (List[Dict]): A list of dictionaries representing the input data to summarize.

        Returns:
            List[Dict]: A list of dictionaries representing the summarized data.
        """
        pass
