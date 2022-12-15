from __future__ import annotations


class TranslatorException(Exception):
    def __init__(self, info: str):
        super().__init__(info)


class TranslationException(Exception):
    def __init__(self, info: str):
        super().__init__(info)
