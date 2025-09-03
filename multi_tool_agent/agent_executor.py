from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    InvalidParamsError,
    Task,
    UnsupportedOperationError,
)
from a2a.utils import (
    completed_task,
    new_artifact,
    new_agent_text_message
)
from a2a.utils.errors import ServerError
from crew_agent import SqlAgent


class SqlAgentExecutor(AgentExecutor):
    """Reimbursement AgentExecutor Example."""

    def __init__(self) -> None:
        self.agent = SqlAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())

        query = context.get_user_input()
        try:
            result = await self.agent.invoke(query)
            print(f'Final Result ===> {result}')
            
        except Exception as e:
            print('Error invoking agent: %s', e)
            raise ServerError(
                error=ValueError(f'Error invoking agent: {e}')
            ) from e

        await event_queue.enqueue_event(new_agent_text_message(str(result)))

    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())

    def _validate_request(self, context: RequestContext) -> bool:
        return False