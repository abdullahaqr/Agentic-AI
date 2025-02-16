from flask import Flask, request, jsonify
from edi_835_parser import EDI835Parser
import faiss
from langchain.embeddings import OpenAIEmbeddings  # Or use Ollama embeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA



#++++++++++++++++++++++++++++++++++++
with open("sample_835.txt", "r") as file:
    raw_edi_data = file.read()

parser = EDI835Parser(raw_edi_data)
parsed_data = parser.parse()
print(parsed_data)  # Extracted claims, payments, and adjustments


#++++++++++++++++++++++++++++++++++++
# Convert parsed 835 data into text format
documents = [" ".join(str(entry)) for entry in parsed_data]

# Use LangChain's FAISS integration
vectorstore = FAISS.from_texts(documents, embedding=OpenAIEmbeddings())

# Save FAISS index
vectorstore.save_local("faiss_index")


#++++++++++++++++++++++++++++++++++++
# Load FAISS index
vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings())

# Use Ollama as LLM
llm = Ollama(model="mistral")  # Or any other model

qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())


#++++++++++++++++++++++++++++++++++++
app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    user_question = request.json.get("question")
    response = qa_chain.run(user_question)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
