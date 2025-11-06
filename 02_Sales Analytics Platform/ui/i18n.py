from __future__ import annotations
import json
import os
from typing import Dict, Any


class I18N:
    def __init__(self, data: Dict[str, Dict[str, str]], default_lang: str = "en"):
        self.data = data or {}
        self.default_lang = default_lang

    @classmethod
    def load(cls, path: str | None, default_lang: str = "en") -> "I18N":
        data: Dict[str, Dict[str, str]] = {}
        if path and os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        return cls(data, default_lang)

    def t(self, key: str, lang: str | None = None, default: str | None = None, **kwargs: Any) -> str:
        lang = lang or self.default_lang
        value = self.data.get(lang, {}).get(key)
        if value is None:
            value = self.data.get(self.default_lang, {}).get(key, default if default is not None else key)
        try:
            return value.format(**kwargs) if kwargs else value
        except Exception:
            return value
