from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx
import orjson

from src.exceptions.translator import TranslationException, TranslatorException
from src.services.base import BaseService
from src.settings.translator import translator_settings

if TYPE_CHECKING:  # pragma: no cover
    from typing import List


@dataclass
class TranslatedCode:
    agent_code_lines: List[str]
    graph_code_lines: List[str]


class TranslatorService(BaseService):
    async def translate(
        self, aasm_code_lines: List[str], module_code_lines: List[List[str]]
    ) -> TranslatedCode:
        url = f"{translator_settings.url}/python/spade"

        joined_module_lines: List[str] = []
        for mcl in module_code_lines:
            joined_module_lines.extend(mcl)
            joined_module_lines.append("\n")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=orjson.dumps(
                        {
                            "code_lines": aasm_code_lines,
                            "module_lines": joined_module_lines,
                        }
                    ),
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
