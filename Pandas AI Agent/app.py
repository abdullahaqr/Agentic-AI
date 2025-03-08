import os
import pandas as pd
from langchain_ollama import ChatOllama
from flask import Flask, request, jsonify
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv
load_dotenv()

BASE_URL_OF_SQL_AGENT_MODEL = os.environ.get('BASE_URL_OF_SQL_AGENT_MODEL')

llm = ChatOllama(
    # model="deepseek-coder:1.3b",
    # model="llama3.2:1b",
    # model="llama3.2",
    model="llama3.1",
    # model="hf.co/defog/sqlcoder-7b-2:latest",
    base_url=BASE_URL_OF_SQL_AGENT_MODEL,
    temperature=0
)


df = pd.read_csv("carc.csv")


agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    # verbose=False,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    allow_dangerous_code=True
)


# question ="Summarize the data?"
# response=agent.invoke(question)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def test():
    return "Pandas AI Agent App is running successfully......"

@app.route("/query", methods=["POST"])
def query():
    user_question = request.json.get("question")
    # response = qa_chain.run(user_question)
    print("I am here")
    response = agent.invoke(user_question)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(port=5555, debug=True)