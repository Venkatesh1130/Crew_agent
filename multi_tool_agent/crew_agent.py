from crewai import Agent, Crew, Task, LLM
import os
from langfuse import Langfuse
from openinference.instrumentation.crewai import CrewAIInstrumentor
from openinference.instrumentation.litellm import LiteLLMInstrumentor
from dotenv import load_dotenv

load_dotenv("../.env")

llm = LLM(model=os.getenv("MODEL", "openai/gpt4-o-AI_Team"))

langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)
if langfuse_client.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

CrewAIInstrumentor().instrument(skip_dep_check=True)
LiteLLMInstrumentor().instrument()

class SqlAgent:
    
    text_to_sql_agent = Agent(
        role="Text-to-SQL Converter",
        goal="Convert natural language questions into valid SQL queries",
        backstory=langfuse_client.get_prompt(name = "Agent Prompt", label = "production").compile(),
        llm=llm,
        verbose=True
    )

    sql_task = Task(
        description=langfuse_client.get_prompt(name = "sql_task", label = "production").compile(),
        agent=text_to_sql_agent,
        expected_output="A valid SQL query string"
    )

    crew = Crew(
        agents=[text_to_sql_agent],
        tasks=[sql_task],
        verbose=True
    )
    
    async def invoke(self,query) -> str:
        result = None
        with langfuse_client.start_as_current_span(name="chubb") as span:
            result=await self.crew.kickoff_async(inputs={"query": query})
            span.update_trace(
                input=query,
                output=str(result),
                user_id="user_123",
                session_id="session_abc",
                tags=["dev", "crewai"],
                metadata={"email": "kny3558@gmail.com"},
                version="1.0.0"
            )
        return result


# if __name__ == "__main__":
#     # Example user query
#     agent = SqlAgent()

#     user_query = "Show me the names of all employees in the Sales department."
#     result = agent.invoke(user_query)
    
#     print("\n=== RESULT ===")
#     print(result)
