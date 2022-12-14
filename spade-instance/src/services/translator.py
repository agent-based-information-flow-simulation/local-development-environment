from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
import orjson

from src.exceptions.translator import TranslationException, TranslatorException
from src.models.translated_code import TranslatedCode
from src.services.base import BaseService
from src.settings.translator import translator_settings

if TYPE_CHECKING:
    from typing import List


class TranslatorService(BaseService):
    async def translate(code: List[str]) -> TranslatedCode:
        url = f"{translator_settings.url}/python/spade"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=orjson.dumps({"code_lines": code}),
                )
        except Exception as e:
            raise TranslatorException(str(e))

        if response.status_code != 200:
            raise TranslationException(response.text)

        body = orjson.loads(response.text)

        return TranslatedCode(
            agent_code_lines=body["agent_code_lines"],
            graph_code_lines=body["graph_code_lines"],
        )
