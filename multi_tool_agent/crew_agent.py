from crewai import Agent, Crew, Task, LLM


llm = LLM(
    model="groq/deepseek-r1-distill-llama-70b",  
    api_key="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"  
)

class SqlAgent:
    text_to_sql_agent = Agent(
        role="Text-to-SQL Converter",
        goal="Convert natural language questions into valid SQL queries",
        backstory=(
            "You are an expert SQL generator. "
            "You take questions in plain English and write optimized SQL queries. "
            "You only output SQL, no explanations."
        ),
        llm=llm,
        verbose=True
    )

    sql_task = Task(
        description="Strictly Convert the user query into SQL. Respond with only SQL query nothing else.",
        agent=text_to_sql_agent,
        expected_output="A valid SQL query string"
    )

    crew = Crew(
        agents=[text_to_sql_agent],
        tasks=[sql_task],
        verbose=True
    )
    
    async def invoke(self,query) -> str:
        result=self.crew.kickoff(inputs={"description": query})
        return result


# if __name__ == "__main__":
#     # Example user query
#     user_query = "Show me the names of all employees in the Sales department."
#     result = crew.kickoff(inputs={"description": user_query})
    
#     print("\n=== RESULT ===")
#     print(result)
