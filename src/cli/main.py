# cli/main.py - Main entry point for the CLI application
# Document Processing and Search System

import sys
import os
from colorama import Fore, Style, init
from ..core.document_processor import process_document, search_documents

init(autoreset=True)

def show_menu():
    print("\n" + Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + "Document Processing and Search System" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.YELLOW + "1. Process Document" + Style.RESET_ALL)
    print(Fore.YELLOW + "2. Search Documents" + Style.RESET_ALL)
    print(Fore.YELLOW + "3. Exit" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

def main():
    if len(sys.argv) != 2:
        print(Fore.RED + "Usage: python main.py <pdf_file>" + Style.RESET_ALL)
        return

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(Fore.RED + f"Error: File '{file_path}' not found" + Style.RESET_ALL)
        return

    while True:
        show_menu()
        choice = input(Fore.GREEN + "Enter your choice (1-3): " + Style.RESET_ALL).strip()

        if choice == '1':
            print(Fore.GREEN + "\nProcessing document..." + Style.RESET_ALL)
            if process_document(file_path):
                print(Fore.GREEN + "\nDocument processed successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "\nError processing document" + Style.RESET_ALL)

        elif choice == '2':
            print(Fore.GREEN + "\nEntering search mode..." + Style.RESET_ALL)
            while True:
                query = input(Fore.GREEN + "Enter your search query (or 'exit'): " + Style.RESET_ALL).strip()
                if query.lower() == 'exit':
                    break
                if not query:
                    print(Fore.RED + "Please enter a valid query" + Style.RESET_ALL)
                    continue
                results = search_documents(query)
                print(Fore.BLUE + f"\nFound {len(results)} results:" + Style.RESET_ALL)
                for i, result in enumerate(results, 1):
                    print(Fore.MAGENTA + f"\nResult {i}:" + Style.RESET_ALL)
                    print(Fore.WHITE + "Content:" + Style.RESET_ALL)
                    print("-" * 40)
                    print(result['content'])
                    print(Fore.WHITE + "\nContext:" + Style.RESET_ALL)
                    print("-" * 40)
                    print(result['context'])
                    print(Fore.WHITE + f"Score: {result['score']:.4f}" + Style.RESET_ALL)
                    print("-" * 40)

        elif choice == '3':
            print(Fore.GREEN + "\nExiting program..." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "\nInvalid choice. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
