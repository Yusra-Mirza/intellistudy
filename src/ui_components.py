"""
Humanized Editorial UI Components & Design System for StudyDesk.
Uses a warm notebook paper palette, Fraunces + DM Sans + JetBrains Mono typography,
crisp inline SVG line icons (zero emojis), HTML-escaped dynamic strings, and
reduced-motion-safe entrance animations.
"""

import html as _html
import streamlit as st
from typing import List, Dict, Any, Optional
from . import config

_SVG_ICONS: Dict[str, str] = {
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "quiz": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
}


def _esc(val: Any) -> str:
    """Safely escapes untrusted text before inserting into HTML."""
    return _html.escape("" if val is None else str(val), quote=True)


def svg_icon(name: str, size: int = 18, stroke_width: float = 1.9) -> str:
    """Returns a crisp inline SVG line icon without relying on emoji glyphs."""
    paths = _SVG_ICONS.get(name, _SVG_ICONS["book"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{paths}</svg>'
    )


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-paper: #FAF7F2;
    --bg-card: #FFFDF9;
    --bg-subtle: #F3EFE6;
    --bg-ink: #1C1917;
    --ink: #1C1917;
    --ink-muted: #57534E;
    --ink-soft: #78716C;
    --border: #E6DFD3;
    --border-strong: #D6CCBC;
    --accent: #C2410C;
    --accent-hover: #9A3412;
    --accent-soft: #FFF1E6;
    --accent-border: #FDBA74;
    --sage: #15803D;
    --sage-soft: #ECFDF5;
    --sage-border: #A7F3D0;
    --amber: #B45309;
    --amber-soft: #FEF3C7;
    --danger: #B91C1C;
    --danger-soft: #FEF2F2;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --shadow-sm: 0 1px 2px rgba(28, 25, 23, 0.05);
    --shadow-md: 0 6px 18px -4px rgba(28, 25, 23, 0.08);
    --shadow-lg: 0 14px 32px -8px rgba(28, 25, 23, 0.12);
}

/* Warm study desk canvas */
.stApp {
    background-color: var(--bg-paper);
    background-image:
        radial-gradient(circle at 12% 8%, rgba(194, 65, 12, 0.06) 0%, transparent 42%),
        radial-gradient(circle at 88% 12%, rgba(21, 128, 61, 0.05) 0%, transparent 38%),
        radial-gradient(rgba(120, 113, 108, 0.14) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 24px 24px;
}

section[data-testid="stSidebar"] {
    background-color: #F5F0E6 !important;
    border-right: 1px solid var(--border);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--ink);
}

/* Force crisp high-contrast ink across Streamlit markdown, headings, labels, and widgets */
.stApp,
.stApp p,
.stApp li,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stCheckbox"] label,
[data-testid="stCaptionContainer"] {
    color: var(--ink) !important;
}

.stApp code,
[data-testid="stSidebar"] code {
    background: var(--bg-subtle) !important;
    color: var(--accent-hover) !important;
    border: 1px solid var(--border);
    padding: 2px 6px;
    border-radius: 5px;
    font-family: 'JetBrains Mono', monospace;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: var(--bg-card) !important;
    color: var(--ink) !important;
    border: 1.5px dashed var(--border-strong) !important;
    border-radius: var(--radius-md) !important;
}

[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] div {
    color: var(--ink-muted) !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background-color: var(--bg-subtle) !important;
    color: var(--ink) !important;
    border: 1px solid var(--border-strong) !important;
}

.ai-status-card,
.ai-status-card * {
    color: #FAF7F2 !important;
}

.ai-status-card .ai-status-kicker {
    color: #FDBA74 !important;
}

.ai-status-card .ai-status-meta,
.ai-status-card .ai-status-meta strong {
    color: #E7E5E4 !important;
}

.ai-status-card .ai-status-meta code {
    color: #FED7AA !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.14) !important;
}

.ai-status-card .ai-status-indicator {
    color: #86EFAC !important;
}

.ai-status-card .ai-status-indicator.idle {
    color: #FDE68A !important;
}

.chat-bubble-user,
.chat-bubble-user * {
    color: #FAF7F2 !important;
}

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3rem !important;
    max-width: 1180px !important;
}

/* Entrance animation (compositor-only, reduced-motion safe) */
@keyframes cardRise {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-header,
.ai-status-card,
.saas-metric-card,
.action-card,
.doc-card,
.quiz-box,
.perf-card,
.timeline-card {
    @media (prefers-reduced-motion: no-preference) {
        animation: cardRise 0.35s cubic-bezier(0.22, 1, 0.36, 1) both;
        animation-delay: calc(var(--stagger-index, 0) * 45ms);
        animation-delay: calc(sibling-index() * 45ms);
    }
}

/* ==========================================================================
   HERO HEADER
   ========================================================================== */
.hero-header {
    background: linear-gradient(135deg, #FFFDF9 0%, #F7F2E9 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}

.hero-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 5px;
    background: linear-gradient(180deg, var(--accent) 0%, #EA580C 60%, var(--sage) 100%);
}

.pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.28rem 0.78rem;
    border-radius: 9999px;
    border: 1px solid var(--accent-border);
    margin-bottom: 0.65rem;
}

.hero-title {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 2.05rem;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.025em;
    margin: 0;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1.02rem;
    color: var(--ink-muted);
    font-weight: 400;
    margin-top: 0.45rem;
    margin-bottom: 0;
    line-height: 1.55;
    max-width: 68ch;
}

/* ==========================================================================
   STUDY DESK STATUS BANNER
   ========================================================================== */
.ai-status-card {
    background: linear-gradient(135deg, #1C1917 0%, #292524 100%);
    color: #FAF7F2;
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.75rem;
    box-shadow: var(--shadow-lg);
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    border: 1px solid #44403C;
}

.ai-status-kicker {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #FDBA74;
    margin-bottom: 0.25rem;
}

.ai-status-heading {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.015em;
    color: #FFFDF9;
}

.ai-status-meta {
    font-size: 0.85rem;
    color: #D6D3D1;
    margin-top: 0.45rem;
    line-height: 1.5;
}

.ai-status-meta code {
    color: #FED7AA;
    background: rgba(255, 255, 255, 0.08);
    padding: 2px 7px;
    border-radius: 5px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}

.ai-status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(21, 128, 61, 0.22);
    color: #86EFAC;
    padding: 0.4rem 0.9rem;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 600;
    border: 1px solid rgba(134, 239, 172, 0.32);
}

.ai-status-indicator.idle {
    background: rgba(217, 119, 6, 0.2);
    color: #FDE68A;
    border-color: rgba(253, 230, 138, 0.35);
}

.pulsing-dot {
    width: 8px;
    height: 8px;
    background-color: #4ADE80;
    border-radius: 50%;
    @media (prefers-reduced-motion: no-preference) {
        animation: pulse-ring 2.2s ease-out infinite;
    }
}

@keyframes pulse-ring {
    0% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.65); }
    70% { box-shadow: 0 0 0 7px rgba(74, 222, 128, 0); }
    100% { box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }
}

/* ==========================================================================
   METRIC & QUICK ACTION CARDS
   ========================================================================== */
.saas-metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.25rem;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.saas-metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--border-strong);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.55rem;
}

.metric-icon-bubble {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: var(--accent-soft);
    color: var(--accent);
    border: 1px solid #FDE6D4;
    display: flex;
    align-items: center;
    justify-content: center;
}

.metric-lbl {
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--ink-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.metric-val {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin: 0.15rem 0;
}

.metric-sub {
    font-size: 0.8rem;
    color: var(--ink-soft);
    font-weight: 400;
}

.quick-action-header {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--ink);
    margin-top: 1.6rem;
    margin-bottom: 0.8rem;
    letter-spacing: -0.015em;
}

.desk-section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.35rem 1.5rem 1.1rem 1.5rem;
    margin: 1.2rem 0 0.9rem 0;
    box-shadow: var(--shadow-sm);
}

.desk-section-eyebrow {
    font-size: 0.73rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent);
    margin-bottom: 0.25rem;
}

.desk-section-title {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0;
}

.desk-section-desc {
    font-size: 0.88rem;
    color: var(--ink-muted);
    margin-top: 0.25rem;
    line-height: 1.45;
}

.action-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.2rem;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
    margin-bottom: 0.5rem;
}

.action-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.action-title {
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.35rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.action-title svg {
    color: var(--accent);
    flex-shrink: 0;
}

.action-desc {
    font-size: 0.86rem;
    color: var(--ink-muted);
    line-height: 1.48;
}

/* ==========================================================================
   DOCUMENTS & STEPPER
   ========================================================================== */
.doc-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.05rem 1.25rem;
    margin-bottom: 0.75rem;
    box-shadow: var(--shadow-sm);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.8rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.doc-card:hover {
    border-color: var(--border-strong);
    box-shadow: var(--shadow-md);
}

.doc-icon-wrap {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--accent-soft);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.9rem;
    flex-shrink: 0;
}

.doc-name {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--ink);
    margin-bottom: 0.15rem;
    word-break: break-word;
}

.doc-meta {
    font-size: 0.8rem;
    color: var(--ink-soft);
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
}

.doc-status-badge {
    background: var(--sage-soft);
    color: var(--sage);
    font-size: 0.74rem;
    font-weight: 700;
    padding: 0.24rem 0.65rem;
    border-radius: 9999px;
    border: 1px solid var(--sage-border);
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    white-space: nowrap;
}

.stepper-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1rem 0;
    padding: 0.9rem 1.1rem;
    background: var(--bg-subtle);
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    gap: 0.5rem;
    flex-wrap: wrap;
}

.stepper-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.76rem;
    font-weight: 600;
    color: var(--ink-soft);
}

.step-node {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #E5DEC9;
    color: var(--ink-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
}

.stepper-step.completed .step-node {
    background: var(--sage);
    color: #FFFFFF;
}

.stepper-step.active .step-node {
    background: var(--accent);
    color: #FFFFFF;
    box-shadow: 0 0 0 4px rgba(194, 65, 12, 0.18);
}

.stepper-step.completed { color: var(--sage); }
.stepper-step.active { color: var(--accent); }

/* ==========================================================================
   CHAT & SOURCES
   ========================================================================== */
.chat-bubble-user {
    background: #1C1917;
    color: #FAF7F2;
    padding: 0.95rem 1.25rem;
    border-radius: 16px 16px 4px 16px;
    max-width: 80%;
    margin-left: auto;
    margin-bottom: 0.75rem;
    box-shadow: var(--shadow-sm);
    font-size: 0.95rem;
    line-height: 1.55;
}

.chat-ai-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}

.chat-ai-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--ink-muted);
}

.source-container {
    margin-top: 0.65rem;
    padding-top: 0.65rem;
    border-top: 1px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    align-items: center;
}

.source-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: var(--bg-subtle);
    color: var(--ink);
    font-size: 0.76rem;
    font-weight: 500;
    padding: 0.25rem 0.62rem;
    border-radius: 6px;
    border: 1px solid var(--border-strong);
    font-family: 'JetBrains Mono', monospace;
}

.agent-workflow-card {
    background: var(--accent-soft);
    border: 1px solid var(--accent-border);
    border-radius: var(--radius-md);
    padding: 0.85rem 1.1rem;
    margin: 0.75rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.agent-chip {
    background: var(--accent);
    color: #FFFFFF;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.agent-step-text {
    font-size: 0.88rem;
    color: #7C2D12;
    font-weight: 600;
}

/* RAG Pipeline Steps */
.rag-flow-card {
    background: var(--bg-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.15rem;
    margin: 0.6rem 0;
}

.rag-step-item {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    position: relative;
    padding-bottom: 1.1rem;
}

.rag-step-item:last-child { padding-bottom: 0; }

.rag-step-item::after {
    content: '';
    position: absolute;
    left: 14px;
    top: 30px;
    bottom: 0;
    width: 2px;
    background: var(--border-strong);
}

.rag-step-item:last-child::after { display: none; }

.rag-step-dot {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: var(--accent-soft);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.82rem;
    font-weight: 700;
    border: 1.5px solid var(--accent-border);
    z-index: 2;
    flex-shrink: 0;
}

/* ==========================================================================
   QUIZ & RESULTS
   ========================================================================== */
.quiz-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.25rem;
}

.quiz-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}

.quiz-q-counter {
    font-size: 0.86rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.quiz-subtopic-tag {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--ink-muted);
    background: var(--bg-subtle);
    padding: 0.22rem 0.65rem;
    border-radius: 6px;
    border: 1px solid var(--border);
}

.quiz-question-text {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--ink);
    line-height: 1.45;
}

.perf-card {
    background: linear-gradient(135deg, #FFFDF9 0%, #F7F2E9 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 2rem;
    text-align: center;
    box-shadow: var(--shadow-md);
    margin-bottom: 1.6rem;
}

.perf-score-display {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 3.2rem;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.03em;
    line-height: 1.05;
    margin: 0.5rem 0;
}

.perf-pct-pill {
    display: inline-block;
    font-size: 0.95rem;
    font-weight: 700;
    padding: 0.35rem 1.1rem;
    border-radius: 9999px;
    margin-bottom: 0.9rem;
}

.perf-rating {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.4rem;
}

/* ==========================================================================
   TOPIC METERS & TIMELINE
   ========================================================================== */
.topic-meter-row {
    margin-bottom: 0.85rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.8rem 1rem;
}

.topic-meter-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 0.45rem;
    gap: 0.5rem;
}

.meter-track {
    height: 7px;
    background: #E8E1D3;
    border-radius: 9999px;
    overflow: hidden;
}

.meter-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.5s ease;
}

.timeline-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.4rem;
    margin-bottom: 0.9rem;
    box-shadow: var(--shadow-sm);
    border-left: 4px solid var(--accent);
}

.timeline-card.weak-focus {
    border-left-color: var(--amber);
    background: #FFFBF2;
}

.timeline-card.completed {
    border-left-color: var(--sage);
    background: #F6FBF7;
}

.day-badge {
    display: inline-block;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 0.76rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    letter-spacing: 0.04em;
}

.weak-focus-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: var(--amber-soft);
    color: #92400E;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    margin-left: 0.5rem;
}

/* ==========================================================================
   EMPTY STATES & STREAMLIT OVERRIDES
   ========================================================================== */
.empty-state {
    text-align: center;
    padding: 2.5rem 1.5rem;
    background: var(--bg-card);
    border: 1.5px dashed var(--border-strong);
    border-radius: var(--radius-lg);
    margin: 1rem 0;
}

.empty-state-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--bg-subtle);
    color: var(--ink-muted);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.85rem;
}

.empty-state-title {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.12rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.35rem;
}

.empty-state-desc {
    font-size: 0.9rem;
    color: var(--ink-muted);
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.5;
}

button[kind="primary"] {
    background: var(--accent) !important;
    color: #FFFDF9 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 6px rgba(194, 65, 12, 0.22) !important;
    transition: background-color 0.2s ease, box-shadow 0.2s ease !important;
}

button[kind="primary"]:hover {
    background: var(--accent-hover) !important;
    box-shadow: 0 4px 12px rgba(194, 65, 12, 0.3) !important;
}

button[kind="secondary"] {
    border-radius: 8px !important;
    font-weight: 600 !important;
    border-color: var(--border-strong) !important;
    background-color: var(--bg-card) !important;
    color: var(--ink) !important;
}

div[data-testid="stSidebarNav"] {
    display: none;
}
</style>
"""


def _render_html(markup: str):
    """Renders custom HTML with inline SVGs safely without Markdown code-block indentation issues."""
    cleaned = "\n".join(line.lstrip() for line in markup.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def inject_custom_css():
    """Injects the StudyDesk editorial stylesheet into the current Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero_header(title: str, subtitle: str, badge: str = "StudyDesk"):
    """Renders an editorial hero header with a subtle kicker pill."""
    html = f"""
    <div class="hero-header">
        <div class="pill-badge">{_esc(badge)}</div>
        <h1 class="hero-title">{_esc(title)}</h1>
        <p class="hero-subtitle">{_esc(subtitle)}</p>
    </div>
    """
    _render_html(html)


def render_ai_status_card(is_ready: bool, model_name: str, total_chunks: int, total_files: int):
    """Renders the desk readiness card showing active model, embeddings, and indexed count."""
    status_text = "Notes indexed and ready" if is_ready else "Waiting for your first PDF"
    dot_html = '<span class="pulsing-dot"></span>' if is_ready else svg_icon("upload", size=14)
    cls = "ai-status-indicator" if is_ready else "ai-status-indicator idle"
    embed_name = _esc(config.EMBEDDING_MODEL_NAME)
    file_word = "file" if total_files == 1 else "files"

    html = f"""
    <div class="ai-status-card">
        <div>
            <div class="ai-status-kicker">AI Study Engine</div>
            <div class="ai-status-heading">
                {"Study materials are indexed and ready" if is_ready else "Upload a PDF below to get started"}
            </div>
            <div class="ai-status-meta">
                Model: <code>{_esc(model_name)}</code>
                &nbsp;|&nbsp; Embeddings: <code>{embed_name}</code>
                &nbsp;|&nbsp; Library: <strong>{int(total_chunks)}</strong> passages across <strong>{int(total_files)}</strong> {file_word}
            </div>
        </div>
        <div>
            <span class="{cls}">{dot_html}{_esc(status_text)}</span>
        </div>
    </div>
    """
    _render_html(html)


def render_metric_card(icon: str, label: str, value: Any, subtext: Optional[str] = None):
    """Renders a metric card with a clean line icon and serif figure."""
    icon_markup = svg_icon(icon, size=18) if icon in _SVG_ICONS else _esc(icon)
    sub_html = f'<div class="metric-sub">{_esc(subtext)}</div>' if subtext else ""
    html = f"""
    <div class="saas-metric-card">
        <div class="metric-header">
            <span class="metric-lbl">{_esc(label)}</span>
            <div class="metric-icon-bubble">{icon_markup}</div>
        </div>
        <div class="metric-val">{_esc(value)}</div>
        {sub_html}
    </div>
    """
    _render_html(html)


def render_empty_state(icon: str, title: str, description: str):
    """Renders a calm empty state card."""
    icon_markup = svg_icon(icon, size=22) if icon in _SVG_ICONS else _esc(icon)
    html = f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon_markup}</div>
        <div class="empty-state-title">{_esc(title)}</div>
        <div class="empty-state-desc">{_esc(description)}</div>
    </div>
    """
    _render_html(html)


def render_source_chips(sources: List[Dict[str, Any]]):
    """Renders citation badges with document name, page number, and score."""
    if not sources:
        return

    chips = []
    for s in sources:
        page = _esc(s.get("page", 1))
        file_name = _esc(s.get("file_name", "Document"))
        score = s.get("score", "")
        score_str = f" ({_esc(score)})" if score else ""
        chips.append(
            f'<span class="source-badge">{svg_icon("file", size=12)}{file_name} &bull; p.{page}{score_str}</span>'
        )

    html = f"""
    <div class="source-container">
        <span style="font-size:0.75rem; font-weight:700; color:#57534E; text-transform:uppercase; letter-spacing:0.05em;">Sources:</span>
        {' '.join(chips)}
    </div>
    """
    _render_html(html)


def render_rag_pipeline_flow(query: str, chunk_count: int, top_score: float = 0.0):
    """Renders a step-by-step explanation of how the answer was retrieved."""
    embed_name = _esc(config.EMBEDDING_MODEL_NAME)
    model_name = _esc(config.GEMINI_MODEL_NAME)
    html = f"""
    <div class="rag-flow-card">
        <div style="font-weight:700; font-size:0.9rem; color:#1C1917; margin-bottom:0.9rem; display:flex; align-items:center; gap:0.45rem;">
            {svg_icon("search", size=16)} How this answer was found
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">1</div>
            <div>
                <div style="font-weight:600; font-size:0.86rem; color:#1C1917;">Your question</div>
                <div style="font-size:0.8rem; color:#57534E; margin-top:2px;">"{_esc(query)}"</div>
            </div>
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">2</div>
            <div>
                <div style="font-weight:600; font-size:0.86rem; color:#1C1917;">Semantic embedding</div>
                <div style="font-size:0.8rem; color:#57534E; margin-top:2px;">Encoded using <code>{embed_name}</code></div>
            </div>
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">3</div>
            <div>
                <div style="font-weight:600; font-size:0.86rem; color:#1C1917;">FAISS passage lookup</div>
                <div style="font-size:0.8rem; color:#57534E; margin-top:2px;">
                    Matched top {int(chunk_count)} passages (best similarity: {float(top_score):.3f})
                </div>
            </div>
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">4</div>
            <div>
                <div style="font-weight:600; font-size:0.86rem; color:#1C1917;">Grounded answer ({model_name})</div>
                <div style="font-size:0.8rem; color:#57534E; margin-top:2px;">
                    Synthesized strictly from the retrieved pages with citations
                </div>
            </div>
        </div>
    </div>
    """
    _render_html(html)


def render_agent_status_banner(tool_name: str, step_status: str = "Active"):
    """Renders the agent routing banner."""
    tool_labels = {
        "search_study_material": "Search Study Material",
        "generate_quiz": "Generate Quiz",
        "calculate_quiz_score": "Calculate Quiz Score",
        "create_study_plan": "Create Study Plan",
        "get_student_memory": "Get Student Memory",
    }
    tool_display = tool_labels.get(tool_name, tool_name)

    html = f"""
    <div class="agent-workflow-card">
        <span class="agent-chip">Assistant: {_esc(step_status)}</span>
        <div class="agent-step-text">
            Chosen action &rarr; <strong>{_esc(tool_display)}</strong>
        </div>
    </div>
    """
    _render_html(html)


def render_performance_card(score: int, total: int, percentage: float):
    """Renders the quiz completion summary card with supportive human feedback."""
    if percentage >= 80:
        badge_bg = "#ECFDF5"
        badge_color = "#15803D"
        rating_text = "Strong grasp of the material"
        tip = "Great work. You have a solid handle on these concepts — a quick check-in next week will keep them fresh."
    elif percentage >= 60:
        badge_bg = "#FFF1E6"
        badge_color = "#C2410C"
        rating_text = "Solid progress"
        tip = "You are getting there. Take a minute to read through the questions you missed below to lock in the details."
    else:
        badge_bg = "#FEF2F2"
        badge_color = "#B91C1C"
        rating_text = "Worth another pass"
        tip = "This is where learning clicks. Walk through the explanations below, then revisit these topics in Ask AI or your Study Plan."

    html = f"""
    <div class="perf-card">
        <div style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#57534E;">
            Quiz Complete
        </div>
        <div class="perf-score-display">{int(score)} / {int(total)}</div>
        <div class="perf-pct-pill" style="background:{badge_bg}; color:{badge_color};">
            Score: {_esc(percentage)}%
        </div>
        <div class="perf-rating">{_esc(rating_text)}</div>
        <div style="font-size:0.92rem; color:#57534E; max-width:540px; margin:0.45rem auto 0 auto; line-height:1.55;">
            {_esc(tip)}
        </div>
    </div>
    """
    _render_html(html)


def render_weak_topic_bar(topic: str, mastery_pct: float):
    """Renders a progress bar indicating topic mastery."""
    if mastery_pct >= 75:
        bar_color = "#15803D"
        status_label = "Strong"
        bg_color = "#ECFDF5"
        text_color = "#15803D"
    elif mastery_pct >= 50:
        bar_color = "#B45309"
        status_label = "Reviewing"
        bg_color = "#FEF3C7"
        text_color = "#92400E"
    else:
        bar_color = "#B91C1C"
        status_label = "Needs Focus"
        bg_color = "#FEF2F2"
        text_color = "#B91C1C"

    clamped = min(100, max(5, float(mastery_pct)))
    html = f"""
    <div class="topic-meter-row">
        <div class="topic-meter-header">
            <span style="color:#1C1917;">{_esc(topic)}</span>
            <div>
                <span style="font-size:0.73rem; font-weight:700; padding:2px 8px; border-radius:4px; background:{bg_color}; color:{text_color}; margin-right:8px;">
                    {status_label}
                </span>
                <span style="color:#57534E;">{_esc(mastery_pct)}%</span>
            </div>
        </div>
        <div class="meter-track">
            <div class="meter-fill" style="width: {clamped}%; background: {bar_color};"></div>
        </div>
    </div>
    """
    _render_html(html)


def render_stepper(current_step: int = 5):
    """
    Renders the multi-step upload progress indicator:
    0: Uploading -> 1: Extracting -> 2: Chunking -> 3: Embedding -> 4: Indexing -> 5: Ready
    """
    steps = [
        "Uploading",
        "Reading PDF",
        "Splitting notes",
        "Embedding",
        "Indexing",
        "Ready",
    ]

    step_items = []
    for idx, name in enumerate(steps):
        if idx < current_step:
            css_class = "stepper-step completed"
            icon = svg_icon("check", size=14, stroke_width=2.5)
        elif idx == current_step:
            css_class = "stepper-step active"
            icon = str(idx + 1)
        else:
            css_class = "stepper-step"
            icon = str(idx + 1)

        step_items.append(
            f'<div class="{css_class}"><div class="step-node">{icon}</div><div>{_esc(name)}</div></div>'
        )

    return f'<div class="stepper-container">{"".join(step_items)}</div>'


def render_question_review_card(item: Dict[str, Any]):
    """Renders a single question review card with HTML escaping."""
    is_correct = item.get("is_correct", False)
    border_col = "#15803D" if is_correct else "#B91C1C"
    badge_text = "Correct" if is_correct else "Needs Review"
    badge_bg = "#ECFDF5" if is_correct else "#FEF2F2"
    badge_col = "#15803D" if is_correct else "#B91C1C"

    correct_block = ""
    if not is_correct:
        correct_block = (
            f'<div style="font-size:0.9rem; margin-bottom:0.4rem;">'
            f'<strong>Correct Answer:</strong> <span style="color:#15803D; font-weight:600;">'
            f'{_esc(item.get("correct_option", ""))}. {_esc(item.get("correct_text", ""))}</span></div>'
        )

    html = (
        f'<div style="background:#FFFDF9; border:1px solid #E6DFD3; border-left:4px solid {border_col}; '
        f'border-radius:12px; padding:1.2rem; margin-bottom:0.9rem; box-shadow:0 1px 2px rgba(28,25,23,0.05);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">'
        f'<span style="font-weight:700; font-size:0.92rem; color:#1C1917;">Question {_esc(item.get("id", ""))}</span>'
        f'<span style="background:{badge_bg}; color:{badge_col}; font-weight:700; font-size:0.76rem; padding:2px 9px; border-radius:999px;">{badge_text}</span>'
        f'</div>'
        f'<div style="font-weight:600; font-size:1.02rem; color:#1C1917; margin-bottom:0.75rem;">{_esc(item.get("question", ""))}</div>'
        f'<div style="font-size:0.9rem; margin-bottom:0.35rem;">'
        f'<strong>Your Answer:</strong> <span style="color:{badge_col}; font-weight:600;">'
        f'{_esc(item.get("selected_option", ""))}. {_esc(item.get("selected_text", ""))}</span>'
        f'</div>'
        f'{correct_block}'
        f'<div style="font-size:0.88rem; color:#57534E; background:#F3EFE6; border:1px solid #E6DFD3; '
        f'padding:0.65rem 0.85rem; border-radius:8px; margin-top:0.6rem; line-height:1.5;">'
        f'<strong>Why:</strong> {_esc(item.get("explanation", ""))}'
        f'</div>'
        f'</div>'
    )
    _render_html(html)


def render_recent_question_card(item: Dict[str, Any]):
    """Renders a recent question card on the Dashboard."""
    q_text = _esc(item.get("question", ""))
    topic = _esc(item.get("topic", "General"))
    timestamp = _esc(item.get("timestamp", ""))
    html = (
        f'<div style="background:#FFFDF9; border:1px solid #E6DFD3; border-radius:10px; '
        f'padding:0.8rem 1rem; margin-bottom:0.55rem; display:flex; justify-content:space-between; align-items:center; gap:0.75rem;">'
        f'<div>'
        f'<div style="font-weight:500; font-size:0.92rem; color:#1C1917;">"{q_text}"</div>'
        f'<div style="font-size:0.78rem; color:#78716C; margin-top:2px;">{topic} &bull; {timestamp}</div>'
        f'</div>'
        f'<span style="color:#C2410C; flex-shrink:0;">{svg_icon("chat", size=16)}</span>'
        f'</div>'
    )
    _render_html(html)


def render_document_card(doc: Dict[str, Any]):
    """Renders an indexed document card in the library."""
    fname = _esc(doc.get("file_name", "Document"))
    pages = int(doc.get("total_pages", 1))
    chunks = int(doc.get("total_chunks", 1))
    html = (
        f'<div class="doc-card">'
        f'<div style="display:flex; align-items:center; min-width:0;">'
        f'<div class="doc-icon-wrap">{svg_icon("book", size=18)}</div>'
        f'<div style="min-width:0;">'
        f'<div class="doc-name">{fname}</div>'
        f'<div class="doc-meta">'
        f'<span>{pages} pages</span>'
        f'<span>&bull;</span>'
        f'<span>{chunks} passages</span>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'<span class="doc-status-badge">{svg_icon("check", size=12, stroke_width=2.5)} Ready</span>'
        f'</div>'
    )
    _render_html(html)


def render_timeline_day_card_header(day_number: int, title: str, is_completed: bool, is_weak: bool, weak_label: Optional[str] = None):
    """Renders a study plan day header card with HTML escaping."""
    weak_badge_html = (
        f'<span class="weak-focus-badge">Focus Area: {_esc(weak_label or "Weak Topic")}</span>'
        if is_weak
        else ""
    )
    card_class = "timeline-card"
    if is_completed:
        card_class += " completed"
    elif is_weak:
        card_class += " weak-focus"

    html = (
        f'<div class="{card_class}">'
        f'<div style="display:flex; justify-content:space-between; align-items:flex-start;">'
        f'<div>'
        f'<span class="day-badge">DAY {int(day_number)}</span>'
        f'{weak_badge_html}'
        f'<h4 style="font-family:\'DM Sans\', sans-serif; margin:0.45rem 0 0.2rem 0; font-size:1.12rem; font-weight:700; color:#1C1917;">{_esc(title)}</h4>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    _render_html(html)
