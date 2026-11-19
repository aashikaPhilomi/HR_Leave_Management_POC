
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


BASE_DIR = Path(__file__).parent

# Load embedding model 
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load HR documents
documents = []

for file_path in (BASE_DIR / "documents").glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")

    documents.append(
        Document(
            page_content=text,
            metadata={"source": file_path.name}
        )
    )

# Create persistent ChromaDB
vector_db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="hr_policies",
    persist_directory=str(BASE_DIR / "chroma_db")
)


def search_policy(query):

    results = vector_db.similarity_search(
        query,
        k=2
    )

    return results


if __name__ == "__main__":

    result = search_policy(
        "What is the leave policy for 5 days?"
    )

    for doc in result:
        print("\nRetrieved Document:")
        print(doc.page_content)
        print("Source:", doc.metadata["source"])
