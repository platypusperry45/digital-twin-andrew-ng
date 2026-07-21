# 🤖 Digital Twin of Andrew Ng

An AI agent that emulates **Andrew Ng**—reproducing not just his domain expertise in Machine Learning, but his warm pedagogical style, intuition-first reasoning, signature expressions, and career timeline milestones.

---

## 🏗 System Architecture

```mermaid
graph TD
    User([User Request]) --> Router[FastAPI Router /api/chat]
    Router --> ConvService[Conversation Service]
    
    subgraph Context Assembly
        ConvService --> STMemory[Short-Term Memory Buffer]
        ConvService --> RAG[RAG Retriever / ChromaStore]
        ConvService --> Timeline[Timeline Engine]
        ConvService --> Persona[Andrew Ng Profile]
    end

    STMemory --> PromptBuilder[Prompt Builder]
    RAG --> PromptBuilder
    Timeline --> PromptBuilder
    Persona --> PromptBuilder

    PromptBuilder --> LLMClient[Gemini Client]
    
    subgraph Resilient LLM Layer
        LLMClient --> KeyManager[Round-Robin Key Manager]
        KeyManager --> GeminiAPI[Gemini 2.5 Flash API]
    end

    GeminiAPI --> Response[Chat Response + Citations]
    Response --> ConvService
    ConvService --> User
    
    subgraph Bonus Features
        ConvService --> LTMemory[Long-Term Vector Store]
        ConvService --> Voice[Voice Service / TTS Engine]
        ConvService --> Dashboard[Memory Graph Endpoint]
    end
🚀 Quickstart & Setup1. PrerequisitesPython 3.10+Gemini API Key(s)2. Environment SetupBash# Clone the repository
git clone [https://github.com/your-username/digital-twin-andrew-ng.git](https://github.com/your-username/digital-twin-andrew-ng.git)
cd digital-twin-andrew-ng

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
3. Environment VariablesCreate a .env file in the project root:Code snippetGEMINI_API_KEYS=["your-gemini-api-key-1", "your-gemini-api-key-2"]
PRIMARY_MODEL=gemini-2.5-flash
FALLBACK_MODEL=gemini-3.1-flash-lite
4. Build Knowledge Base & Run ServerBash# 1. Populate all 11 corpus directories and index into ChromaDB
python -m backend.knowledge.auto_ingest

# 2. Launch FastAPI backend server
uvicorn backend.main:app --port 8000 --reload
💡 Key Features & Design DecisionsIntuition-First Prompt Engineering: Enforces Andrew Ng's pedagogical style—building real-world analogies first before introducing mathematical formulations ($J(\theta)$, gradient descent).Resilient Key Manager: Supports multi-key rotation with automatic backoff and cooldown tracking during rate limits (429 errors).Hybrid RAG & Memory: Integrates sliding session buffers with persistent ChromaDB vector embeddings for long-term recall across sessions.Native Voice & Visualization: Incorporates native Gemini TTS voice synthesis and a visualizable memory graph (/api/memory/visualization/{session_id}).