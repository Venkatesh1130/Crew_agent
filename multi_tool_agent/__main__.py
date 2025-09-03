import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent_executor import (
    SqlAgentExecutor,  # type: ignore[import-untyped]
)
import os


if __name__ == '__main__':
    # --8<-- [start:AgentSkill]
    skill = AgentSkill(
        id='sql_agent',
        name='Returns sql query for text',
        description='returns sql query',
        tags=['sql'],
        examples=['select * from user;'],
    )
   

    public_agent_card = AgentCard(
        name='Sql Agent',
        description='Returns sql query for text',
        url=f'http://{os.getenv("HOST", "0.0.0.0")}:{os.getenv("PORT", "9999")}/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],  
    )
  
    

    request_handler = DefaultRequestHandler(
        agent_executor=SqlAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler
    )

    uvicorn.run(server.build(), host='0.0.0.0', port=9999)