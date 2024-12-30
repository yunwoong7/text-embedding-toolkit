# src/document_processor.py
# Description: Main script for text processing and search

import sys
import os
import PyPDF2
from src.core.chunker import TextChunker
from src.core.context_generator import ContextGenerator
from src.core.opensearch_client import OpenSearchHandler
from src.core.embedding_models import get_embedding_model


def read_pdf(file_path: str) -> str:
    """Read text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
            return text
    except Exception as e:
        print(f"Error reading PDF file: {str(e)}")
        return None


def process_document(file_path: str) -> bool:
    """Process document and store in OpenSearch"""
    try:
        # Read document
        print("\nReading document...")
        text = read_pdf(file_path)
        if not text:
            return False

        # Initialize components
        print("Initializing components...")
        chunker = TextChunker()
        context_gen = ContextGenerator()
        opensearch = OpenSearchHandler()
        embedding_model = get_embedding_model()

        # Create chunks
        print("\nChunking text...")
        chunks = chunker.chunk_text(text)
        print(f"Created {len(chunks)} chunks")

        # Index documents
        print("\nIndexing documents...")
        opensearch.create_index(recreate=True)  # Reset index
        opensearch.index_documents(
            [chunk["text"] for chunk in chunks],
            text,
            context_gen,
            embedding_model
        )

        return True

    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return False


def search_documents(query):
    try:
        opensearch = OpenSearchHandler()
        embedding_model = get_embedding_model()

        if not query:
            print("Please enter a valid query")
            return []

        results = opensearch.search(query, embedding_model)
        return results  # 결과를 반환한다.
    except Exception as e:
        print(f"Error during search: {str(e)}")
        return []


def show_menu() -> None:
    """Display main menu"""
    print("\n" + "=" * 50)
    print("Document Processing and Search System")
    print("=" * 50)
    print("1. Process Document")
    print("2. Search Documents")
    print("3. Exit")
    print("=" * 50)


def main():
    if len(sys.argv) != 2:
        print("Usage: python document_processor.py <pdf_file>")
        return

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        return

    while True:
        show_menu()
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            print("\nProcessing document...")
            if process_document(file_path):
                print("\nDocument processed successfully!")
            else:
                print("\nError processing document")

        elif choice == '2':
            print("\nEntering search mode...")
            search_documents()

        elif choice == '3':
            print("\nExiting program...")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()