# StudyDesk - AI Learning & Study Assistant

A lightweight educational study companion built with Streamlit, Google Gemini, Sentence Transformers, and FAISS. Upload lecture PDFs, ask questions grounded in your notes with page citations, generate multiple-choice quizzes, track weak topics over time, and create day-by-day exam study plans.

---

## Key Features

1. **Dashboard with Quick PDF Upload**
   - Real-time overview of indexed PDFs, questions asked, quizzes completed, average score, and topics to revisit.
   - Upload and index PDFs directly from the Dashboard or from the Study Materials page.

2. **PDF Ingestion & Vector Search**
   - Page-by-page text extraction using `pypdf` with empty/scanned PDF detection.
   - Overlapping passage chunking (`700` characters, `100` overlap) and `all-MiniLM-L6-v2` embeddings stored in a persistent FAISS `IndexFlatIP` index.

3. **Grounded RAG Q&A ("Ask AI")**
   - Retrieves top matching passages and formats strict grounded prompts for Google Gemini.
   - Displays source document names, page numbers, similarity scores, and retrieval steps.
   - Supports both direct RAG Q&A and an intent router (`src/tools.py`) for quiz, progress, and study plan requests.

4. **Interactive Practice Quiz**
   - Generates 5 or 10 MCQs (Easy, Medium, Hard) from your uploaded materials or a custom topic.
   - One-question-at-a-time navigation, instant grading, explanations, and weak-area logging.

5. **Learning Progress & Memory**
   - Persists studied topics, recent questions, quiz history, and weak areas in `data/memory.json`.
   - Flags topics below `70%` and resolves topics scoring `85%` or higher.

6. **Personalized Study Plan**
   - Builds a day-by-day checklist based on target exam date, daily hours, comfort level, and weak areas, with Markdown export.

---

## Project Structure

```text
intellistudy/
├── app.py                        # Streamlit entry point and page routing
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore rules (.venv, myenv, .env, data)
├── .streamlit/
│   └── config.toml               # Streamlit server and client configuration
├── src/                          # Core application package
│   ├── __init__.py
│   ├── config.py                 # Paths, env loading, Gemini API client & error handling
│   ├── memory.py                 # Persistent student memory (data/memory.json)
│   ├── rag.py                    # PDF extraction, chunking, embeddings & FAISS search
│   ├── quiz.py                   # MCQ generation, fallback quiz & grading
│   ├── study_plan.py             # Study plan generation & day-by-day markdown parser
│   ├── tools.py                  # Modular tools & deterministic keyword intent router
│   └── ui_components.py          # Editorial UI CSS, SVG icons & HTML-escaped cards
├── docs/                         # Team guides and reference documents
│   ├── TEAM_WORK_DIVISION_AND_STUDY_GUIDE.md
│   └── IntelliStudy_Work_Division_and_Soft_Computing_Guide.pdf
├── data/
│   └── vector_store/
│       └── .gitkeep
└── uploads/
    └── .gitkeep
```

---

## Installation & Setup

### Prerequisites
- **Python 3.11 or 3.12 (64-bit)** (recommended on Windows for `torch` and `faiss-cpu` wheel support)
- **Windows only:** Microsoft Visual C++ 2015-2022 Redistributable (x64)
- A **Google Gemini API Key**

### 1. Create & Activate a Virtual Environment

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:

**Windows:**
```cmd
copy .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 4. Run the Application
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.
