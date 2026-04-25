import gradio as gr
import requests
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# ── Configuration ──────────────────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/graph/chat")


# ── Backend call ───────────────────────────────────────────────────────────────
def chat_with_agent(message: str, history: list):
    """Send a message to the FastAPI backend and stream back the reply."""
    payload = {
        "content": message,
        "thread_id": "gradio_session",
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response received from the agent.")
    except requests.exceptions.ConnectionError:
        return (
            "⚠️ **Cannot reach the backend server.**\n\n"
            f"Please make sure the FastAPI server is running at `{API_URL}`."
        )
    except requests.exceptions.Timeout:
        return "⏱️ **Request timed out.** The agent is taking too long to respond — please try again."
    except Exception as e:
        return f"❌ **Unexpected error:** `{str(e)}`"


# ── Premium CSS ────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
/* ── Google Font ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & base ────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container {
    font-family: 'Inter', sans-serif !important;
    background: #0d1117 !important;
    color: #e6edf3 !important;
}

/* hide default footer */
footer { display: none !important; }

/* ── Layout wrapper ──────────────────────────────────────── */
#main-row {
    gap: 0 !important;
    min-height: 94vh;
    align-items: stretch;
}

/* ── Sidebar ─────────────────────────────────────────────── */
#sidebar {
    background: linear-gradient(160deg, #161b22 0%, #0d1117 100%);
    border-right: 1px solid #21262d;
    padding: 32px 24px !important;
    border-radius: 16px 0 0 16px;
    min-height: 94vh;
}

/* Avatar */
#avatar-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 28px;
}

#avatar-img {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    border: 3px solid #58a6ff;
    box-shadow: 0 0 24px rgba(88, 166, 255, 0.35);
    object-fit: cover;
    margin-bottom: 14px;
}

#profile-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: #e6edf3;
    text-align: center;
    margin: 0 0 4px 0;
}

#profile-tagline {
    font-size: 0.78rem;
    color: #8b949e;
    text-align: center;
    margin: 0;
}

/* Status badge */
#status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(35, 134, 54, 0.18);
    border: 1px solid rgba(35, 134, 54, 0.4);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #3fb950;
    margin-top: 10px;
    letter-spacing: 0.3px;
}

#status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #3fb950;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* Divider */
.sidebar-divider {
    height: 1px;
    background: #21262d;
    margin: 20px 0;
}

/* Contact links */
.contact-section p { margin: 0 0 14px 0 !important; }

.contact-link {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #8b949e;
    font-size: 0.82rem;
    font-weight: 500;
    text-decoration: none;
    padding: 7px 10px;
    border-radius: 8px;
    transition: background 0.2s, color 0.2s;
}

.contact-link:hover { background: #21262d; color: #58a6ff; }

/* About card */
#about-card {
    background: rgba(88, 166, 255, 0.06);
    border: 1px solid rgba(88, 166, 255, 0.2);
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 8px;
}

#about-card p {
    font-size: 0.8rem !important;
    color: #8b949e !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}

/* ── Chat panel ──────────────────────────────────────────── */
#chat-panel {
    background: #0d1117;
    padding: 32px 28px 20px 28px !important;
    border-radius: 0 16px 16px 0;
    display: flex;
    flex-direction: column;
}

/* Headline */
#chat-headline {
    margin-bottom: 4px;
}

#chat-headline h1 {
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #58a6ff, #a371f7) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin: 0 0 6px 0 !important;
}

#chat-headline p {
    font-size: 0.85rem !important;
    color: #8b949e !important;
    margin: 0 !important;
}

/* Quick action chips */
#chips-row {
    margin-bottom: 12px !important;
}
.quick-chip {
    display: inline-block;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.78rem;
    color: #8b949e;
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s, background 0.2s;
    margin: 3px 4px 3px 0;
    user-select: none;
}
.quick-chip:hover {
    border-color: #58a6ff;
    color: #58a6ff;
    background: rgba(88, 166, 255, 0.08);
}

/* Chat box overrides */
.message-wrap { gap: 10px !important; }

.message.user {
    background: linear-gradient(135deg, #1f4068, #1b1b2f) !important;
    border-radius: 18px 18px 4px 18px !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    padding: 12px 16px !important;
    max-width: 78% !important;
    margin-left: auto !important;
}

.message.bot {
    background: #161b22 !important;
    border-radius: 18px 18px 18px 4px !important;
    border: 1px solid #21262d !important;
    color: #e6edf3 !important;
    padding: 12px 16px !important;
    max-width: 84% !important;
}

/* Input bar */
#chat-input textarea {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    color: #e6edf3 !important;
    font-size: 0.9rem !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s;
}

#chat-input textarea:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1) !important;
    outline: none !important;
}

#chat-input textarea::placeholder { color: #30363d !important; }

/* Send button */
#send-btn {
    background: linear-gradient(135deg, #58a6ff, #a371f7) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-weight: 600 !important;
    padding: 0 20px !important;
    transition: opacity 0.2s, transform 0.1s;
}
#send-btn:hover { opacity: 0.88; transform: translateY(-1px); }
#send-btn:active { transform: translateY(0); }

/* Clear button */
#clear-btn {
    background: transparent !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    color: #8b949e !important;
    transition: border-color 0.2s, color 0.2s;
}
#clear-btn:hover { border-color: #f85149 !important; color: #f85149 !important; }

/* Example buttons */
.example-btn {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #8b949e !important;
    font-size: 0.79rem !important;
    padding: 6px 12px !important;
    transition: all 0.2s;
}
.example-btn:hover {
    border-color: #58a6ff !important;
    color: #58a6ff !important;
    background: rgba(88,166,255,0.07) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
"""

# ── App layout ─────────────────────────────────────────────────────────────────
with gr.Blocks(title="Abdelrahman's AI Career Agent") as demo:
    # ── Top app bar / branding
    gr.HTML("""
    <div style="
        background: linear-gradient(90deg, #161b22, #0d1117);
        border-bottom: 1px solid #21262d;
        padding: 14px 32px;
        display: flex;
        align-items: center;
        gap: 14px;
        border-radius: 16px 16px 0 0;
    ">
        <span style="font-size:1.5rem;">🤖</span>
        <div>
            <span style="font-size:1rem; font-weight:700; color:#e6edf3; letter-spacing:0.2px;">
                AI Career Agent
            </span>
            <span style="font-size:0.72rem; color:#8b949e; display:block; margin-top:1px;">
                Powered by LangGraph · FastAPI · Gemini
            </span>
        </div>
        <div style="margin-left:auto; font-size:0.72rem; color:#3fb950; background:rgba(35,134,54,0.12);
             border:1px solid rgba(35,134,54,0.3); border-radius:20px; padding:3px 11px; font-weight:600;">
            ● LIVE
        </div>
    </div>
    """)

    # ── Main two-column layout
    with gr.Row(elem_id="main-row"):
        # ══ LEFT — Sidebar ════════════════════════════════════════════════════
        with gr.Column(scale=1, elem_id="sidebar"):
            # Profile card
            gr.HTML("""
            <div id="avatar-wrap">
                <img
                    id="avatar-img"
                    src="https://avatars.githubusercontent.com/u/98597559?v=4"
                    onerror="this.src='https://ui-avatars.com/api/?name=Abdelrahman+M&background=1f4068&color=58a6ff&size=200'"
                    alt="Abdelrahman Mohamed"
                />
                <p id="profile-name">Abdelrahman Mohamed</p>
                <p id="profile-tagline">AI / ML Engineer</p>
                <div id="status-badge">
                    <span id="status-dot"></span> Open to Opportunities
                </div>
            </div>
            """)

            gr.HTML('<div class="sidebar-divider"></div>')

            # Contact links
            gr.HTML("""
            <div class="contact-section">
                <p style="font-size:0.68rem; font-weight:600; text-transform:uppercase;
                           letter-spacing:1px; color:#8b949e; margin-bottom:10px !important;">
                    Contact &amp; Links
                </p>

                <a class="contact-link" href="mailto:abdelrahman.m2922@gmail.com">
                    <span>✉️</span> abdelrahman.m2922@gmail.com
                </a>
                <a class="contact-link" href="tel:+201099394113">
                    <span>📞</span> +20 109 939 4113
                </a>
                <a class="contact-link" href="https://linkedin.com/in/abdelrahman-ai" target="_blank">
                    <span>🔗</span> LinkedIn
                </a>
                <a class="contact-link" href="https://github.com/Veto2922" target="_blank">
                    <span>📁</span> GitHub
                </a>
                <a class="contact-link" href="https://medium.com/@abdelrahman.m2922" target="_blank">
                    <span>✍️</span> Medium Blog
                </a>
                <a class="contact-link" href="https://huggingface.co/Abdelrahman2922" target="_blank">
                    <span>🤗</span> Hugging Face
                </a>
                <a class="contact-link"
                   href="https://github.com/Veto2922/Abdelrahman_AI_Career_Agent" target="_blank">
                    <span>🚀</span> Project Source Code
                </a>
            </div>
            """)

            gr.HTML('<div class="sidebar-divider"></div>')

            # About agent card
            gr.HTML("""
            <div id="about-card">
                <p style="font-size:0.68rem; font-weight:600; text-transform:uppercase;
                           letter-spacing:1px; color:#8b949e; margin-bottom:8px !important;">
                    About This Agent
                </p>
                <p>
                    An AI Career Agent built with <strong style="color:#58a6ff;">LangGraph</strong>
                    &amp; <strong style="color:#a371f7;">FastAPI</strong>. It answers questions
                    about Abdelrahman's career, retrieves CV details, and logs recruiter inquiries
                    automatically.
                </p>
            </div>
            """)

        # ══ RIGHT — Chat panel ════════════════════════════════════════════════
        with gr.Column(scale=3, elem_id="chat-panel"):
            # Headline
            gr.HTML("""
            <div id="chat-headline">
                <h1>💬 Ask Abdelrahman's AI</h1>
                <p>
                    Chat with an AI trained on Abdelrahman's career, projects, and skills.
                    Ask anything — it's smarter than a standard CV! 🚀
                </p>
            </div>
            """)

            # Quick-prompt chips (visual only — clicking fills the textbox via JS)
            gr.HTML("""
            <div id="chips-row" style="margin: 12px 0 6px;">
                <span class="quick-chip"
                    onclick="document.querySelector('#chat-input textarea').value='Tell me about your AI projects';
                             document.querySelector('#chat-input textarea').dispatchEvent(new Event('input'));">
                    🧠 AI Projects
                </span>
                <span class="quick-chip"
                    onclick="document.querySelector('#chat-input textarea').value='What are your top skills?';
                             document.querySelector('#chat-input textarea').dispatchEvent(new Event('input'));">
                    ⚙️ Top Skills
                </span>
                <span class="quick-chip"
                    onclick="document.querySelector('#chat-input textarea').value='Tell me about your work experience.';
                             document.querySelector('#chat-input textarea').dispatchEvent(new Event('input'));">
                    💼 Work Experience
                </span>
                <span class="quick-chip"
                    onclick="document.querySelector('#chat-input textarea').value='I want to hire you, how can I contact you?';
                             document.querySelector('#chat-input textarea').dispatchEvent(new Event('input'));">
                    📬 Hire Me
                </span>
                <span class="quick-chip"
                    onclick="document.querySelector('#chat-input textarea').value='What certifications do you have?';
                             document.querySelector('#chat-input textarea').dispatchEvent(new Event('input'));">
                    🎓 Certifications
                </span>
            </div>
            """)

            # Chat interface
            gr.ChatInterface(
                fn=chat_with_agent,
                chatbot=gr.Chatbot(
                    label="",
                    height=480,
                    avatar_images=(
                        None,  # User avatar — default
                        "https://avatars.githubusercontent.com/u/98597559?v=4",
                    ),
                    render_markdown=True,
                    elem_id="chatbox",
                    placeholder="<h3>Ask me anything about Abdelrahman's career!</h3>",
                ),
                textbox=gr.Textbox(
                    placeholder="Ask me about Abdelrahman's skills, projects, or say 'I want to hire him'...",
                    show_label=False,
                    lines=1,
                    max_lines=4,
                    elem_id="chat-input",
                    scale=5,
                ),
                examples=[
                    "Tell me about your AI projects.",
                    "What are your skills in NLP and LLMs?",
                    "Describe your most impactful project.",
                    "I want to hire you, how can I contact you?",
                    "What is your educational background?",
                ],
                save_history=True,
            )

            # Footer note
            gr.HTML("""
            <p style="text-align:center; font-size:0.72rem; color:#30363d; margin-top:16px;">
                Responses are AI-generated · Built with ❤️ by Abdelrahman Mohamed
            </p>
            """)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=7860,
        show_error=True,
        favicon_path=None,
        theme=gr.themes.Base(
            primary_hue=gr.themes.colors.blue,
            neutral_hue=gr.themes.colors.slate,
            font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
        ),
        css=CUSTOM_CSS,
    )
