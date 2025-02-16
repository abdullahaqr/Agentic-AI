import os
import faiss
import numpy as np
from flask import Flask, request, jsonify
from edi_835_parser import EDI835Parser
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Directory to store FAISS index
# FAISS_INDEX_DIR = "faiss_index"
FAISS_INDEX_DIR = os.environ.get('FAISS_INDEX_DIR')
EDI_835_DIR = "835_files"


# Initialize Ollama Embeddings
# embedding_model = OllamaEmbeddings(model="nomic-embed-text")  # Use an appropriate Ollama embedding model
embedding_model = OllamaEmbeddings(model="mxbai-embed-large:latest")  # 335M Parameters

def load_faiss_index():
    """Load or create a FAISS index."""
    if os.path.exists(FAISS_INDEX_DIR):
        print("Loading existing FAISS index...")
        return FAISS.load_local(FAISS_INDEX_DIR, embedding_model)
    else:
        print("Creating a new FAISS index...")
        return FAISS.from_texts([], embedding_model)  # Empty FAISS store

# Load FAISS index
vectorstore = load_faiss_index()

@app.route("/upload", methods=["POST"])
def upload_835():
    """Handles 835 file upload, parses it, and stores embeddings in FAISS."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Read and parse 835 file
        raw_edi_data = file.read().decode("utf-8")
        parser = EDI835Parser(raw_edi_data)
        parsed_data = parser.parse()
        
        # Convert parsed data to text format
        documents = [" ".join(str(entry)) for entry in parsed_data]
        
        # Store embeddings in FAISS
        new_vectorstore = FAISS.from_texts(documents, embedding_model)
        vectorstore.merge_from(new_vectorstore)  # Merge new vectors
        
        # Save updated FAISS index
        vectorstore.save_local(FAISS_INDEX_DIR)
        
        return jsonify({"message": "835 file processed and stored in FAISS"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
