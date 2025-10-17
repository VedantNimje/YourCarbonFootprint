"""
Setup script to initialize the RAG system and create the vector store.
Run this once after installing dependencies.
"""

import os
from rag_system import CarbonFootprintRAG

def main():
    print("=" * 60)
    print("YourCarbonFootprint - RAG System Setup")
    print("=" * 60)
    print()
    
    # Check if knowledge base directory exists
    if not os.path.exists("knowledge_base"):
        print("[ERROR] knowledge_base directory not found!")
        print("Please ensure the knowledge base documents are in the 'knowledge_base' folder.")
        return
    
    # Check for knowledge base files
    kb_files = [
        "ghg_protocol_scopes.txt",
        "carbon_regulations.txt",
        "emission_reduction_strategies.txt",
        "carbon_offset_markets.txt"
    ]
    
    missing_files = []
    for file in kb_files:
        if not os.path.exists(os.path.join("knowledge_base", file)):
            missing_files.append(file)
    
    if missing_files:
        print("[WARNING] Some knowledge base files are missing:")
        for file in missing_files:
            print(f"   - {file}")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    print("[OK] Knowledge base files found")
    print()
    
    # Initialize RAG system
    print("Initializing RAG system...")
    rag = CarbonFootprintRAG()
    
    # Load documents
    print("Loading documents from knowledge_base/...")
    documents = rag.load_documents()
    
    if not documents:
        print("[ERROR] No documents loaded!")
        print("Please check that the knowledge base files contain text content.")
        return
    
    print(f"[OK] Loaded {len(documents)} document chunks")
    print()
    
    # Create vector store
    print("Creating FAISS vector store...")
    print("(This may take a minute - downloading embedding model if needed)")
    rag.create_vector_store(documents)
    
    print()
    print("=" * 60)
    print("[SUCCESS] RAG System Setup Complete!")
    print("=" * 60)
    print()
    print("The vector store has been created at: knowledge_base/faiss_index/")
    print()
    print("You can now run the application with: streamlit run app.py")
    print()
    
    # Test query
    print("Running test query...")
    try:
        result = rag.query("What is Scope 1 emissions?")
        print()
        print("Test Query: 'What is Scope 1 emissions?'")
        print("-" * 60)
        print(result['answer'][:300] + "..." if len(result['answer']) > 300 else result['answer'])
        print("-" * 60)
        print()
        print("[OK] RAG system is working correctly!")
    except Exception as e:
        print(f"[WARNING] Test query failed: {str(e)}")
        print("The vector store was created, but there may be an issue with the LLM.")
        print("Please check your GROQ_API_KEY in the .env file.")
    
    print()

if __name__ == "__main__":
    main()
