"""
Application Dependency Container

Every shared service is created once and injected through this container.

No global singletons.

Python 3.13
"""

from __future__ import annotations

from typing import Any


class Container:

    def __init__(self):

        self._services: dict[str, Any] = {}

    def register(
        self,
        name: str,
        service: Any,
    ) -> None:

        if name in self._services:
            raise RuntimeError(
                f"{name} already registered."
            )

        self._services[name] = service

    def resolve(self, name: str):

        try:

            return self._services[name]

        except KeyError:

            raise RuntimeError(
                f"{name} is not registered."
            ) from None

    def has(self, name: str) -> bool:

        return name in self._services

    def clear(self):

        self._services.clear()