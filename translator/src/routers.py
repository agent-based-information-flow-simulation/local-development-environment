from __future__ import annotations

from aasm import PanicException, __version__, get_spade_code, get_modules_for_target
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from .models import AgentsAssemblyCode, PythonSpadeCode

router = APIRouter(default_response_class=ORJSONResponse)


@router.post("/python/spade", response_model=PythonSpadeCode, status_code=200)
async def translate_aasm(agent_assembly_code: AgentsAssemblyCode):
    try:
        modules = get_modules_for_target(agent_assembly_code.module_lines, "spade")
        spade_code = get_spade_code(agent_assembly_code.code_lines, modules=modules)
        return PythonSpadeCode(
            agent_code_lines=spade_code.agent_code_lines,
            graph_code_lines=spade_code.graph_code_lines,
            module_code_lines=spade_code.module_code_lines,
        )
    except PanicException as e:
        return ORJSONResponse(
            status_code=400,
            content={
                "translator_version": __version__,
                "place": e.place,
                "reason": e.reason,
                "suggestion": e.suggestion,
            },
        )
    except Exception as e:
        return ORJSONResponse(
            status_code=500,
            content={
                "translator_version": __version__,
                "unexpected_reason": str(e),
            },
        )
