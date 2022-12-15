from __future__ import annotations

import copy
import logging
import os
from typing import TYPE_CHECKING

from spade.behaviour import FSMBehaviour

if TYPE_CHECKING:  # pragma: no cover
    from typing import Dict, List

    from aioxmpp.structs import JID
    from spade.agent import Agent
    from spade.behaviour import CyclicBehaviour as Behaviour

logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL_SIMULATION_INITIALIZATION", "INFO"))


# https://github.com/agent-based-information-flow-simulation/spade/blob/6a857c2ae0a86b3bdfd20ccfcd28a11e1c6db81e/spade/agent.py#L137
def setup_agent(agent: Agent) -> List[Behaviour]:
    agent.setup()
    agent._alive.set()
    behaviours = copy.copy(agent.behaviours)

    logger.debug(f"Agent {agent.jid} behaviours: {behaviours}")

    for behaviour in agent.behaviours:  # pragma: no cover
        if not behaviour.is_running:
            behaviour.set_agent(agent)
            if issubclass(type(behaviour), FSMBehaviour):
                for _, state in behaviour.get_states().items():
                    state.set_agent(agent)
            behaviour.start()

    return behaviours


def setup_agents(agents: List[Agent]) -> Dict[JID, List[Behaviour]]:
    agent_behaviours = {}
    for agent in agents:
        agent_behaviours[agent.jid] = setup_agent(agent)

    logger.debug(f"Agent behaviours: {agent_behaviours}")

    return agent_behaviours
