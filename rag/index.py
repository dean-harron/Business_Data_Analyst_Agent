"""Index and search the project's local knowledge-base documents."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


def embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)


def get_store() -> Chroma:
    return Chroma(
        collection_name=settings.rag_collection,
        embedding_function=embeddings(),
        persist_directory=settings.chroma_dir,
    )


def index_directory(directory: str = "knowledge") -> int:
    """Split supported knowledge files and add their chunks to Chroma."""
    base_path = Path(directory)
    paths = sorted(
        path
        for pattern in ("*.md", "*.txt")
        for path in base_path.rglob(pattern)
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
    documents: list[Document] = []

    for path in paths:
        chunks = splitter.split_text(path.read_text(encoding="utf-8"))
        documents.extend(
            Document(page_content=chunk, metadata={"source": str(path)})
            for chunk in chunks
        )

    if not documents:
        return 0

    get_store().add_documents(documents)
    return len(documents)


def search(query: str, k: int = 5):
    """Return the closest knowledge-base chunks and their similarity scores."""
    return get_store().similarity_search_with_score(query, k=k)
