"""
StudyDesk - AI Learning & Study Assistant.
Humanized Streamlit application powered by:
- Google Gemini API
- FAISS Vector Store + Sentence Transformers
- PDF Ingestion & Semantic Chunking
- Interactive Quiz Generator & Grading
- Persistent Student Memory & Progress Tracking
- Dynamic Study Plan Generator with Completion Checklist
"""

import html as _html
import time
from datetime import date, timedelta
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="AI Learning & Study Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src import config
from src import rag
from src import quiz
from src import memory
from src import study_plan
from src import tools
from src import ui_components as ui

ui.inject_custom_css()

# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
PAGES = [
    "Dashboard",
    "Study Materials",
    "Ask AI",
    "Quiz",
    "My Progress",
    "Study Plan",
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prefilled_prompt" not in st.session_state:
    st.session_state.prefilled_prompt = ""
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = None
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""
if "quiz_current_index" not in st.session_state:
    st.session_state.quiz_current_index = 0
if "quiz_run_id" not in st.session_state:
    st.session_state.quiz_run_id = 0
if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = None
if "completed_study_days" not in st.session_state:
    st.session_state.completed_study_days = set()
if "last_uploaded_docs" not in st.session_state:
    st.session_state.last_uploaded_docs = []


def navigate_to(page_name: str):
    """Safely switches pages and triggers a clean rerun."""
    st.session_state.current_page = page_name
    st.rerun()


def on_nav_change():
    """Callback when sidebar radio selection changes."""
    st.session_state.current_page = st.session_state.nav_radio_selection


def _lookup_topic_score(topic_name: str, quiz_history: list) -> float:
    """Returns the most recent recorded quiz percentage for a weak topic, or 45.0."""
    matched = [
        q.get("percentage", 50.0)
        for q in quiz_history
        if q.get("topic") == topic_name or topic_name in q.get("weak_areas", [])
    ]
    return matched[0] if matched else 45.0


def render_pdf_upload_panel(key_prefix: str, button_label: str = "Process and Add to Library"):
    """Shared PDF upload and indexing widget used on both Dashboard and Study Materials."""
    uploaded_files = st.file_uploader(
        "Drop lecture notes, chapters, or study PDFs here",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"{key_prefix}_pdf_uploader",
        help="Upload PDFs that contain selectable text (not scanned image-only pages).",
    )

    stepper_placeholder = st.empty()

    if uploaded_files:
        st.info(f"{len(uploaded_files)} file(s) ready to index.")
        process_btn = st.button(
            button_label,
            type="primary",
            use_container_width=True,
            key=f"{key_prefix}_process_btn",
        )

        if process_btn:
            indexed_batch = []
            for uploaded_file in uploaded_files:
                safe_name = Path(uploaded_file.name).name
                file_path = config.UPLOADS_DIR / safe_name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                with st.spinner(f"Reading and indexing '{safe_name}'..."):
                    stepper_placeholder.markdown(ui.render_stepper(0), unsafe_allow_html=True)
                    time.sleep(0.15)
                    stepper_placeholder.markdown(ui.render_stepper(1), unsafe_allow_html=True)
                    time.sleep(0.15)
                    stepper_placeholder.markdown(ui.render_stepper(2), unsafe_allow_html=True)

                    try:
                        stepper_placeholder.markdown(ui.render_stepper(3), unsafe_allow_html=True)
                        result = rag.process_and_index_pdf(file_path, safe_name)
                        stepper_placeholder.markdown(ui.render_stepper(4), unsafe_allow_html=True)
                        time.sleep(0.1)
                        stepper_placeholder.markdown(ui.render_stepper(5), unsafe_allow_html=True)
                        indexed_batch.append(result)
                    except ValueError as ve:
                        st.error(f"Could not read '{safe_name}': {ve}")
                    except Exception as ex:
                        st.error(f"Error indexing '{safe_name}': {ex}")

            if indexed_batch:
                st.session_state.last_uploaded_docs = indexed_batch
                st.rerun()

    elif key_prefix == "materials":
        ui.render_empty_state(
            "upload",
            "No PDF selected yet",
            "Choose one or more PDF files above to extract text and make them searchable.",
        )

    if st.session_state.last_uploaded_docs:
        for res in st.session_state.last_uploaded_docs:
            safe_fname = _html.escape(str(res.get("file_name", "Document")))
            st.markdown(
                f"""
                <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:12px; padding:1rem 1.2rem; margin:0.75rem 0;">
                    <div style="color:#15803D; font-weight:700; font-size:0.96rem;">
                        Added "{safe_fname}" to your library
                    </div>
                    <div style="color:#166534; font-size:0.84rem; margin-top:0.2rem;">
                        {int(res.get("total_pages", 0))} pages indexed into {int(res.get("total_chunks", 0))} searchable passages.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.4rem;">
            <div style="width: 38px; height: 38px; border-radius: 10px; background: #1C1917; color: #FAF7F2; display: flex; align-items: center; justify-content: center;">
                {ui.svg_icon("book", size=19)}
            </div>
            <div>
                <div style="font-weight: 700; font-size: 1.08rem; color: #1C1917; line-height: 1.15;">StudyAssistant</div>
                <div style="font-size: 0.75rem; color: #57534E;">AI Learning Companion</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Notes, practice quizzes, and revision in one place.")
    st.markdown("<hr style='margin: 0.75rem 0; border: none; border-top: 1px solid #E6DFD3;'>", unsafe_allow_html=True)

    _nav_index = PAGES.index(st.session_state.current_page) if st.session_state.current_page in PAGES else 0

    st.radio(
        "Navigation",
        PAGES,
        index=_nav_index,
        key="nav_radio_selection",
        on_change=on_nav_change,
        label_visibility="collapsed",
    )

    st.markdown("<hr style='margin: 1.1rem 0 0.8rem 0; border: none; border-top: 1px solid #E6DFD3;'>", unsafe_allow_html=True)
    v_status = rag.get_vector_store_status()
    dot_color = "#15803D" if v_status["is_ready"] else "#B45309"
    st.markdown(
        f"""
        <div style="background: #FFFDF9; border: 1px solid #E6DFD3; border-radius: 10px; padding: 0.85rem; font-size: 0.82rem;">
            <div style="font-weight: 700; color: #1C1917; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem;">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:{dot_color};"></span>
                Library Status
            </div>
            <div style="color: #57534E; line-height: 1.5;">
                Passages indexed: <strong>{int(v_status["total_chunks"])}</strong><br>
                PDFs uploaded: <strong>{len(v_status["indexed_files"])}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 1.4rem; font-size: 0.76rem; color: #78716C;">
            Model: <code>{_html.escape(config.GEMINI_MODEL_NAME)}</code>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 1. DASHBOARD
# ==============================================================================
if st.session_state.current_page == "Dashboard":
    ui.render_hero_header(
        title="AI Learning & Study Assistant",
        subtitle="Upload your study materials, ask grounded questions, take practice quizzes, and track your learning progress.",
        badge="Dashboard",
    )

    v_status = rag.get_vector_store_status()
    ui.render_ai_status_card(
        is_ready=v_status["is_ready"],
        model_name=config.GEMINI_MODEL_NAME,
        total_chunks=v_status["total_chunks"],
        total_files=len(v_status["indexed_files"]),
    )

    progress = memory.get_progress_summary()
    total_materials = len(v_status["indexed_files"])
    total_questions = progress.get("total_questions_asked", 0)
    total_quizzes = progress.get("total_quizzes_taken", 0)
    avg_score = progress.get("average_quiz_score", 0.0)
    weak_count = len(progress.get("weak_topics", []))

    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        ui.render_metric_card("book", "Study PDFs", total_materials, f"{v_status['total_chunks']} passages")
    with m_col2:
        ui.render_metric_card("chat", "Questions", total_questions, "Asked from notes")
    with m_col3:
        ui.render_metric_card("quiz", "Quizzes", total_quizzes, "Practice sessions")
    with m_col4:
        ui.render_metric_card("target", "Avg Score", f"{avg_score}%", "Across all quizzes")
    with m_col5:
        ui.render_metric_card(
            "alert",
            "To Revisit",
            weak_count,
            "Needs review" if weak_count > 0 else "On track",
        )

    # Direct PDF Upload right on the Dashboard
    st.markdown(
        """
        <div class="desk-section-card">
            <div class="desk-section-eyebrow">Upload Material</div>
            <h3 class="desk-section-title">Upload Study PDF</h3>
            <p class="desk-section-desc">Upload lecture notes, textbooks, or study PDFs here to index them for Q&amp;A and quizzes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    dash_up_col, dash_lib_col = st.columns([1.45, 1.05])
    with dash_up_col:
        render_pdf_upload_panel(key_prefix="dash", button_label="Process & Index PDF")
    with dash_lib_col:
        st.markdown("##### Indexed Materials")
        dash_docs = rag.get_indexed_files_details()
        if dash_docs:
            for doc in dash_docs[:4]:
                ui.render_document_card(doc)
            if len(dash_docs) > 4:
                st.caption(f"+ {len(dash_docs) - 4} more document(s) in Study Materials.")
            if st.button("Manage All Materials", key="btn_dash_manage_docs", use_container_width=True):
                navigate_to("Study Materials")
        else:
            ui.render_empty_state(
                "book",
                "Your shelf is empty",
                "Upload a PDF on the left to build your searchable study library.",
            )

    # Quick Actions
    st.markdown('<div class="quick-action-header">Quick Actions</div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.markdown(
            f"""
            <div class="action-card">
                <div class="action-title">{ui.svg_icon("chat", 17)} Ask a Question</div>
                <div class="action-desc">Get clear answers with page citations drawn directly from your uploaded PDFs.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start Asking", key="btn_dash_ask", use_container_width=True):
            navigate_to("Ask AI")

    with q2:
        st.markdown(
            f"""
            <div class="action-card">
                <div class="action-title">{ui.svg_icon("quiz", 17)} Practice Quiz</div>
                <div class="action-desc">Test recall with 5 or 10 multiple-choice questions and read why each answer works.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Take a Quiz", key="btn_dash_quiz", use_container_width=True):
            navigate_to("Quiz")

    with q3:
        st.markdown(
            f"""
            <div class="action-card">
                <div class="action-title">{ui.svg_icon("chart", 17)} View Progress</div>
                <div class="action-desc">Check your quiz trend over time and see which topics deserve extra attention.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Analytics", key="btn_dash_prog", use_container_width=True):
            navigate_to("My Progress")

    with q4:
        st.markdown(
            f"""
            <div class="action-card">
                <div class="action-title">{ui.svg_icon("calendar", 17)} Study Schedule</div>
                <div class="action-desc">Plan a realistic day-by-day revision checklist tailored to your exam date.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Create Plan", key="btn_dash_plan", use_container_width=True):
            navigate_to("Study Plan")

    # Recent Activity Snapshot
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    c_left, c_right = st.columns([1.2, 1])

    with c_left:
        st.markdown("#### Recent Questions")
        recent_q = progress.get("recent_questions", [])
        if recent_q:
            for item in recent_q[:4]:
                ui.render_recent_question_card(item)
        else:
            ui.render_empty_state(
                "chat",
                "No questions asked yet",
                "Ask your first question in Ask AI to start building your study log.",
            )

    with c_right:
        st.markdown("#### Weak Topics")
        weak_topics = progress.get("weak_topics", [])
        quiz_history = progress.get("quiz_history", [])
        if weak_topics:
            for wt in weak_topics[:4]:
                ui.render_weak_topic_bar(wt, _lookup_topic_score(wt, quiz_history))
        else:
            st.markdown(
                """
                <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:12px; padding:1.4rem; text-align:center;">
                    <div style="font-weight:700; color:#15803D; font-size:0.96rem;">No weak areas flagged yet</div>
                    <div style="font-size:0.84rem; color:#166534; margin-top:0.25rem;">
                        Complete a practice quiz to spot concepts that need a second pass.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==============================================================================
# 2. STUDY MATERIALS
# ==============================================================================
elif st.session_state.current_page == "Study Materials":
    ui.render_hero_header(
        title="Study Materials",
        subtitle="Upload your notes, textbooks, or lecture slides so your study desk can cite them accurately.",
        badge="Document Library",
    )

    col_up, col_idx = st.columns([1.55, 1.2])

    with col_up:
        st.markdown("#### Upload Study PDF")
        render_pdf_upload_panel(key_prefix="materials", button_label="Process & Index Materials")

    with col_idx:
        st.markdown("#### Indexed Library")
        details = rag.get_indexed_files_details()

        if details:
            for doc in details:
                ui.render_document_card(doc)

            st.markdown("<hr style='margin: 1.2rem 0; border: none; border-top: 1px solid #E6DFD3;'>", unsafe_allow_html=True)
            if st.button("Clear Vector Index", help="Removes all indexed passages so you can start fresh"):
                rag.clear_vector_store()
                st.session_state.last_uploaded_docs = []
                st.success("Library index cleared.")
                st.rerun()
        else:
            ui.render_empty_state(
                "book",
                "No study material yet",
                "Upload a PDF on the left to add it to your searchable library.",
            )


# ==============================================================================
# 3. ASK AI
# ==============================================================================
elif st.session_state.current_page == "Ask AI":
    ui.render_hero_header(
        title="Ask AI",
        subtitle="Ask questions about your uploaded study materials with page citations.",
        badge="Study Q&A",
    )

    col_mode, col_clear = st.columns([3, 1])
    with col_mode:
        interaction_mode = st.radio(
            "Mode",
            ["Direct Study Q&A (RAG)", "AI Agent (Intent Router)"],
            horizontal=True,
            help="Direct Q&A answers strictly from uploaded PDFs. AI Agent can also route quiz, progress, or study plan requests.",
        )
    with col_clear:
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.prefilled_prompt = ""
            st.rerun()

    st.markdown(
        "<div style='font-size:0.78rem; font-weight:700; color:#57534E; text-transform:uppercase; letter-spacing:0.06em; margin: 0.5rem 0 0.35rem 0;'>Try asking:</div>",
        unsafe_allow_html=True,
    )
    chip1, chip2, chip3, chip4, chip5 = st.columns(5)
    selected_chip = None

    with chip1:
        if st.button("Topic overview", use_container_width=True):
            selected_chip = "What is this topic about?"
    with chip2:
        if st.button("Simple terms", use_container_width=True):
            selected_chip = "Explain this in simple terms"
    with chip3:
        if st.button("Give an example", use_container_width=True):
            selected_chip = "Give me an example"
    with chip4:
        if st.button("Summarize chapter", use_container_width=True):
            selected_chip = "Summarize this chapter"
    with chip5:
        if st.button("Exam points", use_container_width=True):
            selected_chip = "What are the important exam points?"

    if not st.session_state.chat_history:
        ui.render_empty_state(
            "chat",
            "Start a conversation with your notes",
            "Type a question below or pick one of the quick prompts above.",
        )

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-bubble-user">{_html.escape(str(msg["content"]))}</div>',
                unsafe_allow_html=True,
            )
        else:
            with st.container(border=True):
                if msg.get("tool"):
                    ui.render_agent_status_banner(msg["tool"], step_status="Completed")
                else:
                    st.markdown(
                        '<div class="chat-ai-header"><span class="chat-ai-label">AI Answer</span></div>',
                        unsafe_allow_html=True,
                    )
                st.markdown(msg["content"])
                if msg.get("sources"):
                    ui.render_source_chips(msg["sources"])

            if msg.get("rag_flow"):
                with st.expander("How this answer was found", expanded=False):
                    flow = msg["rag_flow"]
                    ui.render_rag_pipeline_flow(
                        query=flow.get("query", ""),
                        chunk_count=flow.get("chunk_count", 0),
                        top_score=flow.get("top_score", 0.0),
                    )

    chat_input_val = st.chat_input("Ask anything about your uploaded study material...")
    prompt_to_run = selected_chip or chat_input_val or st.session_state.prefilled_prompt
    if selected_chip or st.session_state.prefilled_prompt:
        st.session_state.prefilled_prompt = ""

    if prompt_to_run:
        if not config.is_gemini_configured():
            st.error("Gemini API key is not configured. Please set GEMINI_API_KEY in .env or the environment.")
            st.stop()

        st.session_state.chat_history.append({"role": "user", "content": prompt_to_run})

        with st.spinner("Reading your notes and preparing an answer..."):
            try:
                if interaction_mode == "AI Agent (Intent Router)":
                    agent_res = tools.route_and_execute(prompt_to_run)
                    tool_selected = agent_res.get("tool_selected", "search_study_material")
                    resp_text = agent_res.get("response", "")
                    sources = agent_res.get("sources", [])

                    if tool_selected == "generate_quiz" and agent_res.get("tool_output"):
                        st.session_state.current_quiz = agent_res["tool_output"]
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_results = None
                        st.session_state.quiz_topic = agent_res.get("tool_input", {}).get("topic", "General Study")
                        st.session_state.quiz_current_index = 0
                        st.session_state.quiz_run_id += 1
                    elif tool_selected == "create_study_plan" and agent_res.get("tool_output"):
                        st.session_state.generated_plan = agent_res["tool_output"]
                        st.session_state.completed_study_days = set()

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": resp_text,
                            "tool": tool_selected,
                            "sources": sources,
                            "rag_flow": {
                                "query": prompt_to_run,
                                "chunk_count": len(sources),
                                "top_score": sources[0]["score"] if sources else 0.0,
                            }
                            if sources
                            else None,
                        }
                    )
                else:
                    rag_res = rag.answer_question(prompt_to_run)
                    resp_text = rag_res.get("answer", "")
                    sources = rag_res.get("sources", [])

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": resp_text,
                            "sources": sources,
                            "rag_flow": {
                                "query": prompt_to_run,
                                "chunk_count": len(sources),
                                "top_score": sources[0]["score"] if sources else 0.0,
                            }
                            if sources
                            else None,
                        }
                    )

                st.rerun()

            except Exception as err:
                st.error(f"AI service error: {err}")


# ==============================================================================
# 4. QUIZ
# ==============================================================================
elif st.session_state.current_page == "Quiz":
    ui.render_hero_header(
        title="AI Quiz Generator",
        subtitle="Test your knowledge with multiple-choice questions and explanations.",
        badge="Quiz",
    )

    mem_data = memory.load_memory()
    indexed_topics = [
        d.get("file_name", "").replace(".pdf", "").replace("_", " ")
        for d in rag.get_indexed_files_details()
        if d.get("file_name")
    ]
    available_topics = list(dict.fromkeys(mem_data.get("topics_studied", []) + indexed_topics))
    if not available_topics:
        available_topics = ["Cloud Computing", "Computer Networks", "Database Systems"]

    with st.expander(
        "Quiz Settings",
        expanded=(st.session_state.current_quiz is None and st.session_state.quiz_results is None),
    ):
        qc1, qc2, qc3 = st.columns([2, 1, 1])
        with qc1:
            quiz_topic = st.selectbox("Select Topic or Material", options=available_topics, index=0)
            custom_topic = st.text_input("Or enter a custom topic (optional):", placeholder="e.g., Virtualization, Normalization")
            active_topic = custom_topic.strip() if custom_topic.strip() else quiz_topic
        with qc2:
            num_q = st.selectbox("Questions", [5, 10], index=0)
        with qc3:
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)

        gen_quiz_btn = st.button("Generate Quiz", type="primary", use_container_width=True)

    if gen_quiz_btn:
        if not config.is_gemini_configured():
            st.error("Gemini API key is not configured. Please set GEMINI_API_KEY.")
        else:
            with st.spinner(f"Writing your quiz on '{active_topic}'..."):
                try:
                    context_chunks = rag.search_study_material(active_topic, top_k=3)
                    context_str = "\n\n".join([c["text"] for c in context_chunks]) if context_chunks else ""

                    questions = quiz.generate_quiz_questions(
                        topic=active_topic,
                        num_questions=num_q,
                        difficulty=difficulty,
                        context=context_str,
                    )
                    st.session_state.current_quiz = questions
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_results = None
                    st.session_state.quiz_topic = active_topic
                    st.session_state.quiz_current_index = 0
                    st.session_state.quiz_run_id += 1
                    st.rerun()
                except Exception as ex:
                    st.error(f"Error generating quiz: {ex}")

    if st.session_state.quiz_results:
        res = st.session_state.quiz_results
        ui.render_performance_card(
            score=res["score"],
            total=res["total"],
            percentage=res["percentage"],
        )

        ra1, ra2 = st.columns(2)
        with ra1:
            if st.button("Retry Quiz", use_container_width=True):
                st.session_state.quiz_answers = {}
                st.session_state.quiz_results = None
                st.session_state.quiz_current_index = 0
                st.session_state.quiz_run_id += 1
                st.rerun()
        with ra2:
            if res.get("weak_areas"):
                weak_target = res["weak_areas"][0]
                if st.button(f"Review Weak Topic ({weak_target})", type="primary", use_container_width=True):
                    st.session_state.prefilled_prompt = f"Help me understand and master this weak area: {weak_target}"
                    navigate_to("Ask AI")
            else:
                if st.button("Build Study Plan", type="primary", use_container_width=True):
                    navigate_to("Study Plan")

        st.markdown("#### Question-by-Question Review")
        for item in res["details"]:
            ui.render_question_review_card(item)

    elif st.session_state.current_quiz:
        questions = st.session_state.current_quiz
        total_q = len(questions)
        curr_idx = st.session_state.quiz_current_index
        q = questions[curr_idx]

        st.markdown(
            f"""
            <div class="quiz-header-bar">
                <span class="quiz-q-counter">Question {curr_idx + 1} of {total_q}</span>
                <span class="quiz-subtopic-tag">{_html.escape(str(q.get('subtopic', st.session_state.quiz_topic)))}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress((curr_idx + 1) / total_q)

        st.markdown(
            f"""
            <div class="quiz-box">
                <div class="quiz-question-text">{int(q['id'])}. {_html.escape(str(q['question']))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        options_list = [f"{k}. {v}" for k, v in q["options"].items()]
        prev_ans = st.session_state.quiz_answers.get(q["id"], None)
        selected_index = None
        if prev_ans:
            for idx_opt, opt_str in enumerate(options_list):
                if opt_str.startswith(prev_ans):
                    selected_index = idx_opt
                    break

        user_choice = st.radio(
            "Options",
            options_list,
            index=selected_index,
            key=f"radio_quiz_q_{st.session_state.quiz_run_id}_{q['id']}",
            label_visibility="collapsed",
        )

        if user_choice:
            st.session_state.quiz_answers[q["id"]] = user_choice[0]

        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
        nav_prev_col, nav_pills_col, nav_next_col = st.columns([1, 2, 1])

        with nav_prev_col:
            if curr_idx > 0:
                if st.button("Previous", use_container_width=True):
                    st.session_state.quiz_current_index -= 1
                    st.rerun()

        with nav_pills_col:
            pill_cols = st.columns(total_q)
            for p_idx in range(total_q):
                is_answered = questions[p_idx]["id"] in st.session_state.quiz_answers
                is_active = p_idx == curr_idx
                label = f"{p_idx + 1}*" if is_answered else f"{p_idx + 1}"
                with pill_cols[p_idx]:
                    if st.button(
                        label,
                        key=f"btn_jump_{p_idx}",
                        type="primary" if is_active else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state.quiz_current_index = p_idx
                        st.rerun()

        with nav_next_col:
            if curr_idx < total_q - 1:
                if st.button("Next", type="primary", use_container_width=True):
                    st.session_state.quiz_current_index += 1
                    st.rerun()
            else:
                if st.button("Submit Quiz", type="primary", use_container_width=True):
                    with st.spinner("Grading your answers..."):
                        results = quiz.calculate_quiz_score(
                            questions=st.session_state.current_quiz,
                            user_answers=st.session_state.quiz_answers,
                            topic=st.session_state.quiz_topic,
                        )
                        st.session_state.quiz_results = results
                        st.rerun()

    else:
        ui.render_empty_state(
            "quiz",
            "No active quiz yet",
            "Open Quiz Settings above and click Generate Quiz whenever you want to practice.",
        )


# ==============================================================================
# 5. MY PROGRESS
# ==============================================================================
elif st.session_state.current_page == "My Progress":
    ui.render_hero_header(
        title="My Learning Progress",
        subtitle="See how your scores are trending, which topics you have covered, and what deserves a second look.",
        badge="Study History",
    )

    summary = memory.get_progress_summary()
    total_q = summary.get("total_questions_asked", 0)
    total_quizzes = summary.get("total_quizzes_taken", 0)
    avg_score = summary.get("average_quiz_score", 0.0)
    topics_studied = summary.get("topics_studied", [])
    quiz_history = summary.get("quiz_history", [])
    weak_topics = summary.get("weak_topics", [])

    pm1, pm2, pm3, pm4 = st.columns(4)
    with pm1:
        ui.render_metric_card("chat", "Total Questions", total_q, "Asked across sessions")
    with pm2:
        ui.render_metric_card("quiz", "Quizzes Completed", total_quizzes, "Practice evaluations")
    with pm3:
        ui.render_metric_card("target", "Average Score", f"{avg_score}%", "Cumulative accuracy")
    with pm4:
        ui.render_metric_card("book", "Topics Studied", len(topics_studied), "Covered so far")

    if total_quizzes == 0 and total_q == 0:
        ui.render_empty_state(
            "chart",
            "No learning activity yet",
            "Ask a question or finish a practice quiz to start seeing your progress here.",
        )
    else:
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        col_charts, col_weak = st.columns([1.4, 1])

        with col_charts:
            st.markdown("#### Quiz Score Trend")
            if quiz_history:
                timeline_scores = [q.get("percentage", 0.0) for q in reversed(quiz_history)]
                st.line_chart({"Score (%)": timeline_scores})
            else:
                st.info("Take a quiz in the Quiz tab to plot your score trend.")

            st.markdown("#### Topics Studied")
            if topics_studied:
                pill_htmls = [
                    f'<span class="source-badge" style="background:#FFF1E6; color:#C2410C; border-color:#FDBA74; font-size:0.82rem; padding:0.3rem 0.75rem;">{_html.escape(str(t))}</span>'
                    for t in topics_studied
                ]
                st.markdown(
                    f'<div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:1.4rem;">{" ".join(pill_htmls)}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.caption("No topics recorded yet.")

        with col_weak:
            st.markdown("#### Topics to Revisit")
            if weak_topics:
                for wt in weak_topics:
                    ui.render_weak_topic_bar(wt, _lookup_topic_score(wt, quiz_history))
            else:
                st.markdown(
                    """
                    <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:12px; padding:1.2rem; text-align:center;">
                        <div style="font-weight:700; color:#15803D;">All topics looking strong</div>
                        <div style="font-size:0.84rem; color:#166534; margin-top:0.2rem;">
                            No weak areas are currently flagged from your recent quizzes.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("#### Recent Questions")
            recent_q = summary.get("recent_questions", [])
            if recent_q:
                for rq in recent_q[:5]:
                    st.markdown(f'- *"{rq["question"]}"* ({rq.get("topic", "General")})')
            else:
                st.caption("No questions asked yet.")

        st.markdown("<hr style='margin: 1.8rem 0; border: none; border-top: 1px solid #E6DFD3;'>", unsafe_allow_html=True)
        with st.expander("Saved Learning Memory (data/memory.json)", expanded=False):
            c_mem1, c_mem2 = st.columns([3, 1])
            with c_mem1:
                st.json(summary)
            with c_mem2:
                if st.button("Reset Learning Memory", help="Clears stored questions, quiz history, and weak topics"):
                    memory.clear_memory()
                    st.success("Learning memory cleared.")
                    st.rerun()


# ==============================================================================
# 6. STUDY PLAN
# ==============================================================================
elif st.session_state.current_page == "Study Plan":
    ui.render_hero_header(
        title="Personalized Study Plan",
        subtitle="Turn your exam date and daily schedule into a clear day-by-day checklist.",
        badge="Revision Schedule",
    )

    mem_data = memory.load_memory()
    default_sub = mem_data["topics_studied"][-1] if mem_data["topics_studied"] else "Cloud Computing"

    with st.container():
        sp_col1, sp_col2 = st.columns([1, 1])

        with sp_col1:
            subject = st.text_input("Subject or Course Name", value=default_sub)
            exam_date = st.date_input("Target Exam Date", value=date.today() + timedelta(days=7), min_value=date.today())
            daily_hours = st.slider("Daily Study Hours Available", min_value=1.0, max_value=8.0, value=2.5, step=0.5)

        with sp_col2:
            knowledge_level = st.selectbox("Current Comfort Level", ["Beginner", "Intermediate", "Advanced"], index=1)
            suggested_weak = mem_data.get("weak_topics", [])
            selected_weak = st.multiselect(
                "Priority Focus Areas",
                options=list(dict.fromkeys(suggested_weak + ["Core Theory", "Exam Review"])),
                default=suggested_weak if suggested_weak else [],
            )

        gen_plan_btn = st.button("Generate Study Plan", type="primary", use_container_width=True)

    if gen_plan_btn:
        if not config.is_gemini_configured():
            st.error("Gemini API key is not configured. Please set GEMINI_API_KEY.")
        else:
            with st.spinner(f"Building your study plan for '{subject}'..."):
                try:
                    plan = study_plan.generate_study_plan(
                        subject=subject,
                        exam_date=str(exam_date),
                        daily_hours=daily_hours,
                        knowledge_level=knowledge_level,
                        weak_topics=selected_weak,
                    )
                    st.session_state.generated_plan = plan
                    st.session_state.completed_study_days = set()
                    st.success("Study plan ready.")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Error generating plan: {ex}")

    if st.session_state.generated_plan:
        plan = st.session_state.generated_plan
        days_structured = study_plan.parse_study_plan_to_days(plan["plan_markdown"], plan.get("weak_topics", []))
        total_days = len(days_structured)
        completed_count = len(st.session_state.completed_study_days)

        st.markdown("<hr style='margin: 1.4rem 0; border: none; border-top: 1px solid #E6DFD3;'>", unsafe_allow_html=True)
        st.markdown(f"### {plan['subject']} Study Roadmap")

        sm1, sm2, sm3, sm4 = st.columns(4)
        with sm1:
            ui.render_metric_card("calendar", "Days Left", f"{plan['days_remaining']} days", f"Exam: {plan['exam_date']}")
        with sm2:
            ui.render_metric_card("clock", "Daily Time", f"{plan['daily_hours']} hrs", f"Level: {plan['knowledge_level']}")
        with sm3:
            ui.render_metric_card("target", "Plan Length", f"{total_days} days", "Focused sessions")
        with sm4:
            pct_done = int(completed_count / total_days * 100) if total_days > 0 else 0
            ui.render_metric_card("check", "Completed", f"{completed_count} / {total_days}", f"{pct_done}% finished")

        if total_days > 0:
            st.progress(completed_count / total_days)

        st.markdown("#### Day-by-Day Checklist")

        for idx, day in enumerate(days_structured):
            d_num = day["day_number"]
            is_done = d_num in st.session_state.completed_study_days
            ui.render_timeline_day_card_header(
                day_number=d_num,
                title=day["title"],
                is_completed=is_done,
                is_weak=day.get("is_weak_topic", False),
                weak_label=day.get("weak_topic_label"),
            )

            if day.get("bullets"):
                for b in day["bullets"]:
                    st.markdown(f"- {b}")
            else:
                st.markdown(day.get("content", ""))

            checked = st.checkbox(
                f"Mark Day {d_num} as Completed",
                value=is_done,
                key=f"check_day_{idx}_{d_num}",
            )
            if checked and d_num not in st.session_state.completed_study_days:
                st.session_state.completed_study_days.add(d_num)
                st.rerun()
            elif not checked and d_num in st.session_state.completed_study_days:
                st.session_state.completed_study_days.remove(d_num)
                st.rerun()

            st.markdown("<div style='margin-bottom:0.85rem;'></div>", unsafe_allow_html=True)

        st.download_button(
            label="Download Study Plan (.md)",
            data=plan["plan_markdown"],
            file_name=f"Study_Plan_{plan['subject'].replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    else:
        ui.render_empty_state(
            "calendar",
            "No study plan yet",
            "Fill in your subject and exam date above to create a personalized schedule.",
        )
