import os
import pandas as pd
from langchain_ollama import ChatOllama
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv
load_dotenv()

BASE_URL_OF_SQL_AGENT_MODEL = os.environ.get('BASE_URL_OF_SQL_AGENT_MODEL')

llm = ChatOllama(
    # model="deepseek-coder:1.3b",
    # model="llama3.2:1b",
    # model="llama3.2",
    # model="llama3.1",
    model="hf.co/defog/sqlcoder-7b-2:latest",
    base_url=BASE_URL_OF_SQL_AGENT_MODEL,
    temperature=0
)


df = pd.read_csv("titanic.csv")
api_key=os.getenv("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(    
            google_api_key=api_key, 
            model="gemini-1.5-pro"
            )


agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )


question ="Summarize the data?"
response=agent.invoke(question)