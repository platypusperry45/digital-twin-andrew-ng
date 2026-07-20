"""
Base parser interface.

Every parser returns plain text from a document.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseParser(ABC):
    """
    Abstract parser.
    """

    @abstractmethod
    def parse(
        self,
        path: Path,
    ) -> str:
        """
        Extract plain text from a document.
        """
        raise NotImplementedError