# YourCarbonFootprint - RAG-Enhanced AI Carbon Accounting Tool

![Carbon Footprint](https://img.shields.io/badge/Carbon-Footprint-green)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-AI%20Agents-blue)
![Groq](https://img.shields.io/badge/Groq-LLM-purple)
![RAG](https://img.shields.io/badge/RAG-Enabled-orange)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-red)

A lightweight, multilingual carbon accounting and reporting tool for SMEs in Asia, powered by **Retrieval-Augmented Generation (RAG)** and specialized AI agents for intelligent, context-aware carbon accounting assistance.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [AI Agents](#-ai-agents)
- [Data Structure](#-data-structure)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Features
- **Enterprise-Grade Data Entry**: Comprehensive form with business unit tracking, project categorization, facility details, and data quality indicators
- **Dashboard Visualization**: Interactive charts and graphs for emissions data analysis
- **AI-Powered Insights**: Specialized AI agents for various carbon accounting tasks
- **Data Management**: CSV import/export, robust error handling, and automatic backups
- **Multilingual Support**: Available in multiple languages

### AI Agent Features
| Agent | Role |
|-------|------|
| **RAG Knowledge Base** | Answer questions using retrieval-augmented generation from comprehensive carbon accounting knowledge base |
| Data Entry Assistant | Helps users classify emissions, map to scopes, and validate data entries (RAG-enhanced) |
| Report Summary Generator | Converts emission data into human-readable summaries |
| Carbon Offset Advisor | Suggests verified offset options based on user profile and location (RAG-enhanced) |
| Regulation Radar | Notifies users of upcoming compliance needs (RAG-enhanced) |
| Emission Optimizer | Uses historical data to suggest reductions and savings (RAG-enhanced) |

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       YourCarbonFootprint App                           │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                ┌─────────────────────────────────────┐
                │                                     │
┌───────────────▼───────────────┐       ┌─────────────▼─────────────┐
│      Frontend (Streamlit)     │       │      Backend Services     │
│                               │       │                           │
│  ┌─────────────────────────┐  │       │  ┌─────────────────────┐  │
│  │    Navigation System    │  │       │  │   Data Management   │  │
│  │  - Dashboard            │  │       │  │  - JSON Storage     │  │
│  │  - Data Entry           │  │       │  │  - CSV Import       │  │
│  │  - AI Insights          │  │       │  │  - Backup System    │  │
│  │  - Settings             │  │       │  └─────────────────────┘  │
│  └─────────────────────────┘  │       │                           │
│                               │       │  ┌─────────────────────┐  │
│  ┌─────────────────────────┐  │       │  │  AI Agent System    │  │
│  │   Data Entry Module     │  │       │  │  - CrewAI Framework │  │
│  │  - Enterprise Form      │◄─┼───────┼──┤  - Groq LLM         │  │
│  │  - Validation           │  │       │  │  - Specialized      │  │
│  │  - AI Suggestions       │  │       │  │    Agent Roles      │  │
│  └─────────────────────────┘  │       │  └─────────────────────┘  │
│                               │       │                           │
│  ┌─────────────────────────┐  │       │  ┌─────────────────────┐  │
│  │   Dashboard Module      │  │       │  │  Analytics Engine   │  │
│  │  - Emissions Overview   │◄─┼───────┼──┤  - Data Processing  │  │
│  │  - Charts & Graphs      │  │       │  │  - Calculations     │  │
│  │  - Filtering            │  │       │  │  - Visualization    │  │
│  └─────────────────────────┘  │       │  └─────────────────────┘  │
└───────────────────────────────┘       └───────────────────────────┘
```

## 🚀 Installation

### Prerequisites
- Python 3.9+
- Groq API key (for AI features)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AIAnytime/Your-Carbon-Footprint/tree/main.git
cd Your-Carbon-Footprint/
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Initialize the RAG system (first time only):
```bash
python setup_rag.py
```

This will:
- Load knowledge base documents
- Create embeddings using HuggingFace sentence-transformers
- Build FAISS vector store for semantic search
- Run a test query to verify setup

## ⚙️ Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key for AI agent functionality

### Data Storage
- Emissions data is stored in `data/emissions.json`
- Company settings are stored in `data/settings.json`
- Automatic backups are created for corrupted files with timestamped filenames

### RAG System Storage
- Knowledge base documents: `knowledge_base/*.txt`
- FAISS vector store: `knowledge_base/faiss_index/`
- Embedding model: Downloaded automatically to cache (HuggingFace sentence-transformers)

## 📊 Usage

### Running the Application

```bash
streamlit run app.py
```

### Navigation
- **AI Insights**: Access RAG knowledge base and specialized AI agents
  - **RAG Knowledge Base**: Ask questions with context-aware answers and source citations
  - **Data Assistant**: Get help classifying emissions (RAG-enhanced)
  - **Report Summary**: Generate summaries from emissions data
  - **Offset Advisor**: Get carbon offset recommendations (RAG-enhanced)
  - **Regulation Radar**: Check compliance requirements (RAG-enhanced)
  - **Emission Optimizer**: Get reduction strategies (RAG-enhanced)
- **Data Entry**: Add new emission entries with enterprise-grade form
- **Dashboard**: View emissions data visualizations and analytics
- **Settings**: Configure company information and preferences

### Data Entry Form
The enhanced enterprise-grade data entry form includes:
- Business unit and project tracking
- Facility location and responsible person fields
- Data quality indicators and verification status
- AI-powered emission factor suggestions
- Financial impact tracking (optional)

### CSV Import/Export
- Upload CSV files with emissions data
- Download sample CSV template
- Export emissions data as CSV or PDF reports

## 🤖 AI Agents with RAG

YourCarbonFootprint integrates **Retrieval-Augmented Generation (RAG)** with specialized AI agents using CrewAI and Groq LLM:

### RAG Knowledge Base
- **Comprehensive Knowledge Base**: 4 curated documents covering GHG Protocol, regulations, reduction strategies, and offset markets
- **Vector Store**: FAISS-based semantic search with HuggingFace embeddings
- **Context-Aware Responses**: AI agents augmented with relevant knowledge base context
- **Direct Query Interface**: Ask questions and get answers with source citations

### AI Agents (RAG-Enhanced)
1. **Data Entry Assistant**: Helps classify emissions and validate data entries (uses GHG Protocol knowledge)
2. **Report Summary Generator**: Creates human-readable summaries from emissions data
3. **Carbon Offset Advisor**: Recommends verified carbon offset options (uses offset market knowledge)
4. **Regulation Radar**: Provides updates on compliance requirements (uses regulation knowledge)
5. **Emission Optimizer**: Suggests ways to reduce emissions based on historical data (uses reduction strategies knowledge)

### RAG System Usage

```python
from rag_system import get_rag_system

# Initialize RAG system
rag = get_rag_system()

# Load or create vector store
rag.load_vector_store()

# Query the knowledge base
result = rag.query("What are the differences between Scope 1, 2, and 3 emissions?")
print(result['answer'])

# View source documents
for doc in result['source_documents']:
    print(doc.page_content)

# Get context for AI agents
context = rag.get_context_for_agent("GHG Protocol emission scopes")
```

### AI Agent Implementation with RAG

```python
from ai_agents import CarbonFootprintAgents

# Initialize agents with RAG enabled (default)
agents = CarbonFootprintAgents(use_rag=True)

# Run data entry assistant (automatically uses RAG context)
result = agents.run_data_entry_crew("Diesel fuel used in company vehicles")

# Run regulation check (automatically uses RAG context)
result = agents.run_regulation_check_crew(
    location="Jakarta, Indonesia",
    industry="Manufacturing",
    export_markets="European Union, Japan"
)
```

## 📚 Knowledge Base Content

The RAG system includes comprehensive documentation on:

### 1. GHG Protocol & Emission Scopes (`ghg_protocol_scopes.txt`)
- Detailed definitions of Scope 1, 2, and 3 emissions
- Calculation methodologies and emission factors
- Organizational boundary approaches
- Reporting requirements and best practices

### 2. Carbon Regulations (`carbon_regulations.txt`)
- **EU CBAM**: Timeline, covered sectors, requirements, penalties
- **Japan GX League**: Carbon pricing, trading mechanisms, targets
- **Indonesia ETS/ETP**: Emissions trading, energy transition programs
- **Other Major Regulations**: California, UK, China, Korea, New Zealand
- Compliance best practices and upcoming trends

### 3. Emission Reduction Strategies (`emission_reduction_strategies.txt`)
- Energy efficiency improvements (lighting, HVAC, industrial processes)
- Renewable energy adoption (solar, wind, biomass)
- Transportation optimization (fleet electrification, route optimization)
- Supply chain optimization and circular economy
- Sector-specific strategies and implementation roadmaps

### 4. Carbon Offset Markets (`carbon_offset_markets.txt`)
- Types of carbon markets (compliance vs voluntary)
- Offset project types and pricing
- Verification standards (VCS, Gold Standard, CAR, ACR)
- Regional offset options for Asia-Pacific
- Best practices for offset purchasing

## 📁 Data Structure

### Emissions Data Format

```json
{
  "date": "2025-01-15",
  "business_unit": "Corporate",
  "project": "Carbon Reduction Initiative",
  "scope": "Scope 2",
  "category": "Electricity",
  "activity": "Office Electricity",
  "country": "India",
  "facility": "Mumbai HQ",
  "responsible_person": "Rahul Sharma",
  "quantity": 1000.0,
  "unit": "kWh",
  "emission_factor": 0.82,
  "emissions_kgCO2e": 820.0,
  "data_quality": "High",
  "verification_status": "Internally Verified",
  "notes": "Monthly electricity bill"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built by AI Anytime with ❤️ for a sustainable future
