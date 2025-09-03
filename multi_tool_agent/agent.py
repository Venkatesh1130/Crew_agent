from acp_sdk import Annotations, MessagePart, Metadata, Link, LinkType, PlatformUIAnnotation
from acp_sdk.models.platform import PlatformUIType
from crewai import LLM
from acp_sdk.server import Server, Context
from acp_sdk.models import Message
from typing import Iterator, Any
from crewai.agents.parser import AgentAction, AgentFinish
from beeai_framework.adapters.a2a.agents import A2AAgent
from beeai_framework.memory.unconstrained_memory import UnconstrainedMemory
import os
from textwrap import dedent

server=Server()

@server.agent(
    metadata=Metadata(
        annotations=Annotations(
            beeai_ui=PlatformUIAnnotation(
                ui_type=PlatformUIType.HANDSOFF,
                user_greeting="What data query or insight do you want to generate from your database?",
                display_name="SQL Agent",
            ),
        ),
        programming_language="Python",
        framework="CrewAI",
        documentation=dedent(
            """\
            The SQL agent converts natural language into accurate and optimized SQL queries. It uses specialized sub-agents for parsing user input, analyzing the database schema, and optimizing the query for performance. Tasks are executed sequentially, with each sub-agent’s output feeding into the next. The process runs asynchronously for faster results. Simply provide a text description of the data you want to retrieve, and the agent generates the corresponding SQL query efficiently.
            """
        ),
        use_cases=[
            "**Convert Text to Sql** – Takes user query and response with SQL Query",
        ]
    )
)

async def sql_agent(input: list[Message], context: Context):
    """
    The agent converts user prompt to SQL query
    """

    try:
        input = {"project_description": input[-1].parts[-1].content}
        # result = create_marketing_crew(llm, step_callback).kickoff(inputs=input)
        
        agent=A2AAgent(url="http://127.0.0.1:9999", memory=UnconstrainedMemory())
        response=await agent.run(input["project_description"])
        # yield MessagePart(content=result.raw)
        # print(f"output:  {str(response.output)}")
        yield MessagePart(content=response.output[0].content[0].text)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def run():
    server.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))


if __name__ == "__main__":
    run()