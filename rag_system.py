"""
RAG (Retrieval-Augmented Generation) System for Carbon Footprint Application.
Provides document retrieval and context augmentation for AI agents.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# Load environment variables
load_dotenv()


class CarbonFootprintRAG:
    """RAG system for carbon accounting knowledge base."""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base"):
        """
        Initialize the RAG system.
        
        Args:
            knowledge_base_path: Path to the directory containing knowledge base documents
        """
        self.knowledge_base_path = knowledge_base_path
        self.vector_store = None
        self.llm = None
        self.qa_chain = None
        
        # Create knowledge base directory if it doesn't exist
        os.makedirs(knowledge_base_path, exist_ok=True)
        
        # Initialize components
        self._initialize_llm()
        self._initialize_embeddings()
        
    def _initialize_llm(self):
        """Initialize the Groq LLM."""
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
    
    def _initialize_embeddings(self):
        """Initialize the embedding model."""
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def load_documents(self) -> List[Document]:
        """
        Load documents from the knowledge base directory.
        
        Returns:
            List of Document objects
        """
        try:
            # Load text files from knowledge base
            loader = DirectoryLoader(
                self.knowledge_base_path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            documents = loader.load()
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            splits = text_splitter.split_documents(documents)
            
            return splits
        except Exception as e:
            print(f"Error loading documents: {str(e)}")
            return []
    
    def create_vector_store(self, documents: List[Document] = None):
        """
        Create or update the FAISS vector store.
        
        Args:
            documents: Optional list of documents to add. If None, loads from knowledge base.
        """
        if documents is None:
            documents = self.load_documents()
        
        if not documents:
            print("No documents found to create vector store.")
            return
        
        # Create FAISS vector store
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        # Save vector store to disk
        vector_store_path = os.path.join(self.knowledge_base_path, "faiss_index")
        self.vector_store.save_local(vector_store_path)
        print(f"Vector store created with {len(documents)} document chunks.")
    
    def load_vector_store(self):
        """Load existing FAISS vector store from disk."""
        vector_store_path = os.path.join(self.knowledge_base_path, "faiss_index")
        
        if os.path.exists(vector_store_path):
            self.vector_store = FAISS.load_local(
                vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print("Vector store loaded successfully.")
        else:
            print("No existing vector store found. Creating new one...")
            self.create_vector_store()
    
    def add_documents(self, documents: List[Document]):
        """
        Add new documents to the existing vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if self.vector_store is None:
            self.load_vector_store()
        
        if documents:
            self.vector_store.add_documents(documents)
            # Save updated vector store
            vector_store_path = os.path.join(self.knowledge_base_path, "faiss_index")
            self.vector_store.save_local(vector_store_path)
            print(f"Added {len(documents)} documents to vector store.")
    
    def setup_qa_chain(self):
        """Set up the RetrievalQA chain."""
        if self.vector_store is None:
            self.load_vector_store()
        
        # Create custom prompt template
        prompt_template = """You are an expert in carbon accounting, emissions tracking, and environmental regulations.
Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always cite the relevant regulations or standards when applicable.

Context: {context}

Question: {question}

Answer: """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create RetrievalQA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system with a question.
        
        Args:
            question: The question to ask
            
        Returns:
            Dictionary containing the answer and source documents
        """
        if self.qa_chain is None:
            self.setup_qa_chain()
        
        try:
            result = self.qa_chain.invoke({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "source_documents": []
            }
    
    def retrieve_context(self, query: str, k: int = 4) -> List[Document]:
        """
        Retrieve relevant documents for a given query.
        
        Args:
            query: The search query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant Document objects
        """
        if self.vector_store is None:
            self.load_vector_store()
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return docs
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []
    
    def get_context_for_agent(self, query: str, max_length: int = 2000) -> str:
        """
        Get formatted context string for AI agents.
        
        Args:
            query: The search query
            max_length: Maximum length of context string
            
        Returns:
            Formatted context string
        """
        docs = self.retrieve_context(query)
        
        if not docs:
            return "No relevant context found in knowledge base."
        
        context_parts = []
        current_length = 0
        
        for i, doc in enumerate(docs, 1):
            doc_text = f"[Source {i}]: {doc.page_content}\n"
            if current_length + len(doc_text) > max_length:
                break
            context_parts.append(doc_text)
            current_length += len(doc_text)
        
        return "\n".join(context_parts)


# Singleton instance
_rag_instance = None


def get_rag_system() -> CarbonFootprintRAG:
    """Get or create the RAG system singleton instance."""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = CarbonFootprintRAG()
    return _rag_instance
