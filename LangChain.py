from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import OllamaLLM
from langchain_community.utilities import SQLDatabase
from langchain.agents import initialize_agent
from dotenv import load_dotenv
from dbConnection.DbConnection import DbPostgres

# Load environment variables
load_dotenv()

# ✅ Initialize Database Connection
database = DbPostgres()
db_engine = database.connect_to_db()
db = SQLDatabase(db_engine)

# ✅ Extract available table names
table_names = db.get_usable_table_names()
table_names_str = ", ".join(table_names)

# ✅ Fix: Provide correct table names in system prompt
system_prompt = f"""
You are an AI that generates SQL queries for a PostgreSQL database.

- Always use the tool named **"PostgreSQL Query Tool"** to execute queries.
- **Do NOT create or assume other tool names.**
- **Ensure queries match the exact case-sensitive table names.**
- **DO NOT use single quotes (`'`) around queries before sending them.**
- **If the user asks for a table that does not exist, return an error.**

✅ Example valid query: `SELECT * FROM "Employees" LIMIT 10;`

Available Tables:
{table_names_str}

If a user asks a question, generate a valid SQL query using these table names.
"""

# ✅ Fix: Remove unnecessary quotes before execution
def execute_sql_query(query):
    """Executes SQL queries and removes unnecessary quotes."""
    cleaned_query = query.strip("'")  # ✅ Remove leading/trailing single quotes
    try:
        return db.run(cleaned_query)
    except Exception as e:
        return f"Error executing query: {str(e)}"

# ✅ Fix: Ensure the agent registers the correct tool
sql_query_tool = Tool(
    name="PostgreSQL Query Tool",  # ✅ Must exactly match the system prompt
    func=execute_sql_query,
    description=f"Executes SQL queries on PostgreSQL. Available tables: {table_names_str}"
)

# ✅ Load LLM Model
model = OllamaLLM(model="llama3-groq-tool-use:latest")

# ✅ Initialize the Agent
agent_executor = initialize_agent(
    tools=[sql_query_tool],  # ✅ Ensure the correct tool is passed
    llm=model,
    agent="zero-shot-react-description",
    verbose=True,
)

# ✅ Example Query
example_query = 'give me the first 5 employees'

response = agent_executor.invoke(example_query)

print("\n✅ Agent Response:")
print(response)

# ✅ Debugging Info
print("\n✅ Registered Tool Names:", [tool.name for tool in [sql_query_tool]])
print("\n✅ Database Dialect:", db.dialect)
print("\n✅ Available Tables:", db.get_usable_table_names())
print("\n✅ Sample Query Output:")
print(db.run('SELECT * FROM "Employees" LIMIT 10;'))
