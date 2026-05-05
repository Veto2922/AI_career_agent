
#  AI Career Agent 🤖💼

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Abdelrahman2922/Abdelrahman_AI_Career_Agent)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/Veto2922/Abdelrahman_AI_Career_Agent.git)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=flat&logo=gradio)](https://gradio.app/)

Welcome to ** AI Career Agent** — a cutting-edge interactive AI agent designed to act as a highly intelligent, 24/7 personal recruiter and interactive CV. It accurately and naturally answers conversational questions about  (AI/ML Engineer) experience, skills, projects, and certifications.

<img width="1511" height="903" alt="image" src="https://github.com/user-attachments/assets/6268b3e5-79a6-400f-8007-a487cf9d8a1e" />


---

## 🌟 Project Highlights & Achievements

- **True Agentic Workflow**: Built with **LangGraph**, the application doesn't just passively answer questions using **Vectorless RAG**; it actively reasons, decides which internal tools to execute, and formats responses based on user context.
- **Microservices-ready Architecture**: Decoupled backend (FastAPI) and frontend (Gradio) connected via internal networking.
- **Advanced Contextual Grounding**: Employs Tree Retrieval mechanisms, ensuring the agent *never* hallucinates skills or projects outside of the formally ingested CV context.
- **Multilingual Support**: Can intelligently converse naturally, including responding contextually in Egyptian Arabic if prompted in Arabic.
- **Modern UI/UX**: Features a highly customized, premium dark-mode Gradio interface injected with custom CSS for an extraordinary user experience.
- **Seamless Deployment**: Fully dockerized using the lightning-fast `uv` package manager and successfully deployed to a high-availability Hugging Face Docker Space.

---

## 🏗 Project Architecture & Structure

The codebase is organized following production-grade architectural patterns, ensuring maintainability, modularity, and scalability:

<img width="1780" height="527" alt="image" src="https://github.com/user-attachments/assets/ec587077-763e-4c07-90c3-902485bac950" />





```text
Abdelrahman_AI_Career_Agent/
├── __pycache__/            # Compiled Python files
├── data/                   # Initial data files and resources
├── logs/                   # Loguru runtime log output directory
├── notebooks/              # Jupyter notebooks for prototyping and experimentation
├── src/                    # 🚀 Core Application Source Code
│   ├── api_routes/         # FastAPI endpoints and route handlers
│   ├── Data_ingestion_block/ # Logic for parsing, vectorizing, and ingesting CVs
│   ├── graph_block/        # LangGraph Workflow definitions (Prompts, Nodes, Tools, State)
│   ├── retrieval_block/    # RAG/Tree Retrieval implementation details
│   └── Services/           # Shared backend services (e.g., PageIndexClient)
├── .env                    # Environment variables (Ignored in Git, managed securely)
├── .dockerignore           # Exclusions for Docker Image
├── Dockerfile              # Hugging Face Spaces ready Docker configuration
├── entrypoint.sh           # Shell script to concurrently start FastAPI & Gradio
├── gradio_app.py           # Premium, custom CSS injected Frontend UI
├── main_api.py             # FastAPI backend initialization
├── pyproject.toml          # Python project dependencies (managed via uv)
└── uv.lock                 # Lockfile for exact dependency reproducibility
```

<img width="374" height="595" alt="image" src="https://github.com/user-attachments/assets/5543532a-9214-4a48-843d-ceec286875d6" />

---

## 🚀 Live Demo

You can interact with the live agent right now! The application runs securely inside a Docker container orchestrated continuously via Hugging Face.

👉 **[Try the Agent on Hugging Face Spaces](https://huggingface.co/spaces/Abdelrahman2922/Abdelrahman_AI_Career_Agent)**

*(Clicking the link will take you to the interactive Gradio Chat UI powered by the FastAPI backend).*

---

## 💻 Local Installation & Usage

### Prerequisites
- Python 3.13+ installed.
- Docker installed (optional, but recommended).
- API Keys for Google GenAI/Langchain/PageIndex appropriately configured.

### Using Docker (Highly Recommended)
Because the project uses Docker and the modern `uv` package manager, reproducing the environment is extremely easy.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Veto2922/AI_Career_Agent.git
   cd AI_Career_Agent
   ```

2. **Configure Environment Variables:**
   Rename `.env.example` to `.env` (or create a new `.env` file) and securely add your keys:
   *Ensure there are NO trailing spaces or quotes around your variables if running with Docker!*
   ```env
   GOOGLE_API_KEY=AIza...
   GROQ_API_KEY=gsk_...
   Page_index_api=723f...
   # (Include any LangSmith configs if tracing is to be used)
   ```

3. **Build & Run:**
   ```bash
   # Build the Docker image
   docker build -t ai-career-agent .
   
   # Run the container (mapping both API and UI ports)
   docker run -p 8000:8000 -p 7860:7860 --env-file .env ai-career-agent
   ```

4. **Access the App:**
   - **Frontend UI:** `http://localhost:7860`
   - **FastAPI Swagger Docs:** `http://localhost:8000/docs`

### Native Local Installation (Without Docker)

1. **Install `uv` (the fast python package installer):**
   ```bash
   pip install uv
   ```

2. **Sync Dependencies:**
   ```bash
   uv sync --frozen --no-dev
   ```

3. **Run the Apps:**
   You will need to open two terminal windows:
   
   *Terminal 1 (Backend API):*
   ```bash
   uv run uvicorn main_api:app --host 0.0.0.0 --port 8000
   ```
   
   *Terminal 2 (Frontend App):*
   ```bash
   uv run python gradio_app.py
   ```

---

## 🛠 Top Technologies Under the Hood

* **[LangGraph](https://python.langchain.com/docs/langgraph):** For constructing stateful, multi-actor LLM applications.
* **[FastAPI](https://fastapi.tiangolo.com/):** High-performance backend API routing constraint validation.
* **[Gradio](https://gradio.app/):** To rapidly build highly-customizable Machine Learning UI components.
* **[uv (astral)](https://github.com/astral-sh/uv):** Used for microsecond-fast Python dependency syncing.
* **[Docker](https://www.docker.com/):** For guaranteed cross-environment compatibility.
* **[Loguru](https://github.com/Delgan/loguru):** For easy, beautiful, robust logging inside the application.

