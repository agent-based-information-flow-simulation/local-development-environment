from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any, Coroutine, Dict, List

from src.instance.status import Status

if TYPE_CHECKING:  # pragma: no cover
    from aioprocessing import AioQueue
    from aioxmpp.structs import JID
    from spade.agent import Agent
    from spade.behaviour import CyclicBehaviour as Behaviour

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_SIMULATION_STATUS", "INFO"))


def get_broken_agents(
    agents: List[Agent],
    agent_behaviours: Dict[JID, List[Behaviour]],
) -> List[str]:
    broken_agents = []

    for agent in agents:
        if agent is None or not agent.is_alive():
            broken_agents.append(str(agent.jid))
            continue

        for behaviour in agent_behaviours[agent.jid]:
            if behaviour._exit_code != 0:
                logger.error(f"[{agent.jid}] {behaviour}: KILLED")
                broken_agents.append(str(agent.jid))
                break

    return broken_agents


def get_instance_status(num_agents: int, broken_agents: List[str]) -> Dict[str, Any]:
    return {
        "status": Status.RUNNING,
        "num_agents": num_agents,
        "broken_agents": broken_agents,
    }


async def send_status(
    agents: List[Agent],
    agent_num_behaviours: Dict[JID, Behaviour],
    simulation_status_updates: AioQueue,
    ):
    broken_agents = get_broken_agents(agents, agent_num_behaviours)
    instance_status = get_instance_status(len(agents), broken_agents)
    logger.info(f"Sending status to spade api: {instance_status}")
    await simulation_status_updates.coro_put(instance_status)
