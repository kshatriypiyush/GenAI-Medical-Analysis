from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_documents(folder_path):
    """Load PDF documents from a folder."""
    documents = []
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            file_path = os.path.join(folder_path, file)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    return documents

def preprocess_documents(doc_texts):
    """Preprocess documents by chunking them."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = []
    for text in doc_texts:
        split_docs.extend(splitter.split_text(text))
    return split_docs

if __name__ == "__main__":
    folder_path = "./data/sample_medical_reports/"
    docs = load_documents(folder_path)
    doc_texts = [doc.page_content for doc in docs]
    processed_docs = preprocess_documents(doc_texts)
    print(f"Loaded {len(docs)} documents.")
    print(f"Preprocessed into {len(processed_docs)} chunks.")
