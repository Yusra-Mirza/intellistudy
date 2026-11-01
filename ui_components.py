"""
Modern SaaS UI Components & Design System for IntelliStudy.
Provides high-fidelity CSS, consistent color tokens, rounded cards, micro-interactions,
and reusable layout helpers for Streamlit.
"""

import streamlit as st
from typing import List, Dict, Any, Optional

CUSTOM_CSS = """
<style>
/* ==========================================================================
   1. DESIGN TOKENS, TYPOGRAPHY & INTERACTION VARIABLES
   ========================================================================== */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --primary: #4F46E5;
    --primary-light: #EEF2FF;
    --primary-hover: #4338CA;
    --primary-glow: rgba(79, 70, 229, 0.25);
    --secondary: #06B6D4;
    --secondary-glow: rgba(6, 182, 212, 0.25);
    --accent: #8B5CF6;
    --bg-main: #F8FAFC;
    --bg-card: #FFFFFF;
    --text-main: #0F172A;
    --text-muted: #64748B;
    --border-card: #E2E8F0;
    --border-hover: #CBD5E1;
    --border-focus: #A5B4FC;
    --success: #10B981;
    --success-bg: #ECFDF5;
    --success-glow: rgba(16, 185, 129, 0.25);
    --warning: #F59E0B;
    --warning-bg: #FFFBEB;
    --warning-glow: rgba(245, 158, 11, 0.25);
    --danger: #EF4444;
    --danger-bg: #FEF2F2;
    --danger-glow: rgba(239, 68, 68, 0.25);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
    --shadow-hover: 0 12px 24px -4px rgba(79, 70, 229, 0.12), 0 6px 12px -2px rgba(0, 0, 0, 0.04);
    --shadow-soft: 0 8px 30px rgba(0, 0, 0, 0.04);
    --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
    --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-normal: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    --transition-spring: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Global Font & Smooth Experience */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--text-main);
    scroll-behavior: smooth;
}

/* Smooth Modern Custom Scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #F1F5F9;
    border-radius: 9999px;
}
::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 9999px;
    transition: background 0.2s ease;
}
::-webkit-scrollbar-thumb:hover {
    background: #94A3B8;
}

/* Layout container */
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1200px !important;
}

/* ==========================================================================
   2. KEYFRAME ANIMATIONS
   ========================================================================== */
@keyframes pulse-ring {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(52, 211, 153, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
}

@keyframes pulse-warning {
    0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.5); }
    70% { transform: scale(1.02); box-shadow: 0 0 0 6px rgba(245, 158, 11, 0); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
}

@keyframes gradient-line {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ==========================================================================
   3. HERO & HEADERS
   ========================================================================== */
.hero-header {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-lg);
    padding: 1.8rem 2rem;
    margin-bottom: 1.8rem;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
    transition: var(--transition-normal);
}

.hero-header:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--border-hover);
}

.hero-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4F46E5 0%, #8B5CF6 50%, #06B6D4 100%);
    background-size: 200% 200%;
    animation: gradient-line 6s ease infinite;
}

.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.03em;
    margin: 0;
    line-height: 1.2;
    transition: color 0.2s ease;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-muted);
    font-weight: 500;
    margin-top: 0.5rem;
    margin-bottom: 0;
    line-height: 1.5;
}

.pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--primary-light);
    color: var(--primary);
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.28rem 0.85rem;
    border-radius: 9999px;
    border: 1px solid var(--border-focus);
    margin-bottom: 0.6rem;
    transition: var(--transition-fast);
    cursor: default;
}

.pill-badge:hover {
    transform: scale(1.04);
    box-shadow: 0 2px 8px var(--primary-glow);
    background: #E0E7FF;
}

/* ==========================================================================
   4. AI STATUS & SYSTEM CARDS
   ========================================================================== */
.ai-status-card {
    background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
    color: #FFFFFF;
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.8rem;
    box-shadow: var(--shadow-lg);
    margin-bottom: 1.6rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: var(--transition-spring);
    position: relative;
    overflow: hidden;
}

.ai-status-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 32px -4px rgba(30, 27, 75, 0.4), 0 0 20px rgba(99, 102, 241, 0.2);
    border-color: rgba(165, 180, 252, 0.3);
}

.ai-status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    padding: 0.4rem 0.9rem;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 700;
    border: 1px solid rgba(16, 185, 129, 0.3);
    transition: var(--transition-fast);
}

.ai-status-indicator:hover {
    background: rgba(16, 185, 129, 0.25);
    transform: scale(1.03);
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.35);
}

.pulsing-dot {
    width: 9px;
    height: 9px;
    background-color: #34D399;
    border-radius: 50%;
    box-shadow: 0 0 8px #34D399;
    animation: pulse-ring 2.2s cubic-bezier(0.455, 0.03, 0.515, 0.955) infinite;
}

/* ==========================================================================
   5. METRIC CARDS
   ========================================================================== */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.2rem;
    margin-bottom: 1.8rem;
}

.saas-metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-md);
    padding: 1.3rem;
    box-shadow: var(--shadow-sm);
    transition: var(--transition-spring);
    position: relative;
    cursor: default;
    overflow: hidden;
}

.saas-metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-hover);
    border-color: var(--border-focus);
}

.saas-metric-card:active {
    transform: scale(0.98);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
}

.metric-icon-bubble {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: var(--primary-light);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    transition: var(--transition-normal);
}

.saas-metric-card:hover .metric-icon-bubble {
    transform: scale(1.15) rotate(6deg);
    background: var(--primary);
    color: #FFFFFF;
    box-shadow: 0 4px 12px var(--primary-glow);
}

.metric-lbl {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: color 0.2s ease;
}

.saas-metric-card:hover .metric-lbl {
    color: var(--primary);
}

.metric-val {
    font-size: 1.95rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin: 0.2rem 0;
    transition: transform 0.2s ease;
}

.saas-metric-card:hover .metric-val {
    transform: scale(1.02);
    transform-origin: left center;
}

.metric-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
    font-weight: 500;
}

/* ==========================================================================
   6. QUICK ACTION CARDS
   ========================================================================== */
.quick-action-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0F172A;
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
}

.action-card {
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-md);
    padding: 1.3rem;
    box-shadow: var(--shadow-sm);
    transition: var(--transition-spring);
    cursor: pointer;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}

.action-card:hover {
    border-color: var(--primary);
    transform: translateY(-5px);
    box-shadow: 0 14px 28px -4px rgba(79, 70, 229, 0.16);
}

.action-card:active {
    transform: scale(0.97);
}

.action-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.35rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: transform 0.2s ease, color 0.2s ease;
}

.action-card:hover .action-title {
    color: var(--primary);
    transform: translateX(3px);
}

.action-desc {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.45;
    margin-bottom: 0.8rem;
}

/* ==========================================================================
   7. DOCUMENT & UPLOAD CARDS
   ========================================================================== */
.doc-card {
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.9rem;
    box-shadow: var(--shadow-sm);
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: var(--transition-spring);
    position: relative;
    cursor: default;
}

.doc-card:hover {
    border-color: var(--primary);
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
}

.doc-card:active {
    transform: scale(0.99);
}

.doc-icon-wrap {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: #F1F5F9;
    color: #475569;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    margin-right: 1rem;
    transition: var(--transition-normal);
}

.doc-card:hover .doc-icon-wrap {
    transform: scale(1.1) rotate(-4deg);
    background: var(--primary-light);
    color: var(--primary);
}

.doc-name {
    font-weight: 700;
    font-size: 0.98rem;
    color: #0F172A;
    margin-bottom: 0.2rem;
    transition: color 0.2s ease;
}

.doc-card:hover .doc-name {
    color: var(--primary);
}

.doc-meta {
    font-size: 0.82rem;
    color: var(--text-muted);
    display: flex;
    gap: 0.8rem;
}

.doc-status-badge {
    background: var(--success-bg);
    color: var(--success);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.7rem;
    border-radius: 9999px;
    border: 1px solid #A7F3D0;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    transition: var(--transition-fast);
}

.doc-card:hover .doc-status-badge {
    box-shadow: 0 0 10px var(--success-glow);
    transform: scale(1.05);
}

/* Stepper Progress Bar for PDF processing */
.stepper-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1.5rem 0;
    padding: 1.1rem 1.6rem;
    background: #F8FAFC;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-card);
    box-shadow: var(--shadow-sm);
    transition: var(--transition-normal);
}

.stepper-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    position: relative;
    z-index: 1;
    transition: var(--transition-normal);
}

.step-node {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #E2E8F0;
    color: #64748B;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    transition: var(--transition-spring);
    cursor: default;
}

.step-node:hover {
    transform: scale(1.12);
}

.stepper-step.completed .step-node {
    background: var(--success);
    color: #FFFFFF;
    box-shadow: 0 0 10px var(--success-glow);
}

.stepper-step.active .step-node {
    background: var(--primary);
    color: #FFFFFF;
    box-shadow: 0 0 0 5px var(--primary-glow);
    animation: pulse-ring 2s infinite;
}

.stepper-step.completed {
    color: var(--success);
}

.stepper-step.active {
    color: var(--primary);
}

/* ==========================================================================
   8. CHAT & RAG CITATION UI
   ========================================================================== */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1.1rem;
    margin: 1.2rem 0;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
    color: #FFFFFF;
    padding: 1.15rem 1.45rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 82%;
    margin-left: auto;
    margin-top: 1.4rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.22);
    font-size: 0.96rem;
    line-height: 1.55;
    transition: var(--transition-fast);
}

.chat-bubble-user:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.32);
}

.chat-bubble-ai {
    background: #FFFFFF;
    color: #1E293B;
    padding: 1.35rem 1.55rem;
    border-radius: 18px 18px 18px 4px;
    border: 1px solid var(--border-card);
    max-width: 88%;
    margin-right: auto;
    margin-top: 0.6rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-sm);
    font-size: 0.95rem;
    line-height: 1.65;
    transition: var(--transition-normal);
}

.chat-bubble-ai:hover {
    border-color: var(--border-focus);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

/* Native Streamlit Chat Message Spacing Support */
[data-testid="stChatMessage"] {
    margin-top: 1.2rem !important;
    margin-bottom: 1.8rem !important;
    padding: 1.1rem 1.35rem !important;
    border-radius: 14px !important;
}

.source-container {
    margin-top: 0.9rem;
    padding-top: 0.75rem;
    border-top: 1px solid #F1F5F9;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
}

.source-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #F1F5F9;
    color: #334155;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.28rem 0.7rem;
    border-radius: 8px;
    border: 1px solid #CBD5E1;
    font-family: 'JetBrains Mono', monospace;
    transition: var(--transition-fast);
    cursor: pointer;
}

.source-badge:hover {
    background: var(--primary-light);
    color: var(--primary);
    border-color: var(--border-focus);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px var(--primary-glow);
}

.source-badge:active {
    transform: scale(0.96);
}

/* Agent Workflow Card */
.agent-workflow-card {
    background: #FAFAFE;
    border: 1px solid #E0E7FF;
    border-radius: var(--radius-md);
    padding: 1rem 1.25rem;
    margin: 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    transition: var(--transition-normal);
}

.agent-workflow-card:hover {
    border-color: var(--primary);
    box-shadow: 0 6px 18px var(--primary-glow);
    transform: translateY(-2px);
}

.agent-chip {
    background: var(--primary);
    color: #FFFFFF;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: var(--transition-fast);
}

.agent-step-text {
    font-size: 0.88rem;
    color: #4338CA;
    font-weight: 600;
}

/* RAG Flow Diagram inside Expander */
.rag-flow-card {
    background: #F8FAFC;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-md);
    padding: 1.3rem;
    margin: 0.8rem 0;
    transition: var(--transition-normal);
}

.rag-flow-card:hover {
    border-color: var(--border-focus);
    box-shadow: var(--shadow-sm);
}

.rag-step-item {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    position: relative;
    padding-bottom: 1.2rem;
    transition: var(--transition-fast);
}

.rag-step-item:last-child {
    padding-bottom: 0;
}

.rag-step-item::after {
    content: '';
    position: absolute;
    left: 15px;
    top: 32px;
    bottom: 0;
    width: 2px;
    background: #E2E8F0;
}

.rag-step-item:last-child::after {
    display: none;
}

.rag-step-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #EEF2FF;
    color: #4F46E5;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    border: 2px solid #C7D2FE;
    z-index: 2;
    transition: var(--transition-spring);
}

.rag-step-item:hover .rag-step-dot {
    transform: scale(1.18);
    background: var(--primary);
    color: #FFFFFF;
    border-color: var(--primary);
    box-shadow: 0 0 10px var(--primary-glow);
}

/* ==========================================================================
   9. QUIZ & TEST EXPERIENCE
   ========================================================================== */
.quiz-box {
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-lg);
    padding: 2rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.5rem;
    transition: var(--transition-normal);
}

.quiz-box:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-md);
}

.quiz-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border-card);
}

.quiz-q-counter {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.quiz-subtopic-tag {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    background: #F1F5F9;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    transition: var(--transition-fast);
}

.quiz-subtopic-tag:hover {
    background: #E2E8F0;
    color: #0F172A;
}

.quiz-question-text {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.45;
    margin-bottom: 1.5rem;
}

/* Performance Results */
.perf-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-xl);
    padding: 2.2rem;
    text-align: center;
    box-shadow: var(--shadow-md);
    margin-bottom: 2rem;
    transition: var(--transition-spring);
    position: relative;
    overflow: hidden;
}

.perf-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
    border-color: var(--border-focus);
}

.perf-score-display {
    font-size: 3.6rem;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -0.04em;
    line-height: 1;
    margin: 0.5rem 0;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.perf-card:hover .perf-score-display {
    transform: scale(1.06);
}

.perf-pct-pill {
    display: inline-block;
    font-size: 1rem;
    font-weight: 700;
    padding: 0.35rem 1.15rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
    transition: var(--transition-fast);
}

.perf-pct-pill:hover {
    transform: scale(1.05);
}

.perf-rating {
    font-size: 1.35rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.4rem;
}

/* ==========================================================================
   10. WEAK TOPICS & PROGRESS BARS
   ========================================================================== */
.topic-meter-row {
    margin-bottom: 1rem;
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-sm);
    padding: 0.85rem 1.1rem;
    transition: var(--transition-spring);
}

.topic-meter-row:hover {
    transform: translateX(4px);
    border-color: var(--border-focus);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.topic-meter-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.45rem;
}

.meter-track {
    height: 8px;
    background: #E2E8F0;
    border-radius: 9999px;
    overflow: hidden;
}

.meter-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.7s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
}

/* ==========================================================================
   11. STUDY PLAN TIMELINE CARDS
   ========================================================================== */
.timeline-card {
    background: #FFFFFF;
    border: 1px solid var(--border-card);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--shadow-sm);
    position: relative;
    border-left: 5px solid var(--primary);
    transition: var(--transition-spring);
}

.timeline-card:hover {
    transform: translateX(6px) translateY(-3px);
    border-left-width: 8px;
    box-shadow: 0 14px 28px -4px rgba(79, 70, 229, 0.16);
    border-color: var(--border-hover);
}

.timeline-card.weak-focus {
    border-left-color: var(--warning);
    background: #FFFDF9;
}

.timeline-card.weak-focus:hover {
    box-shadow: 0 14px 28px -4px rgba(245, 158, 11, 0.2);
    border-left-color: #D97706;
}

.timeline-card.completed {
    border-left-color: var(--success);
    background: #F9FEFA;
    opacity: 0.95;
}

.timeline-card.completed:hover {
    box-shadow: 0 14px 28px -4px rgba(16, 185, 129, 0.2);
    border-left-color: #059669;
}

.day-badge {
    display: inline-block;
    background: #EEF2FF;
    color: #4F46E5;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.22rem 0.65rem;
    border-radius: 6px;
    margin-bottom: 0.5rem;
    transition: var(--transition-fast);
}

.day-badge:hover {
    background: #E0E7FF;
    transform: scale(1.05);
}

.weak-focus-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: #FEF3C7;
    color: #92400E;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.22rem 0.65rem;
    border-radius: 6px;
    margin-left: 0.5rem;
    transition: var(--transition-fast);
    animation: pulse-warning 3s infinite;
}

.weak-focus-badge:hover {
    transform: scale(1.06);
    background: #FDE68A;
}

/* ==========================================================================
   12. EMPTY STATES
   ========================================================================== */
.empty-state {
    text-align: center;
    padding: 3.5rem 2rem;
    background: #FFFFFF;
    border: 2px dashed #CBD5E1;
    border-radius: var(--radius-lg);
    margin: 1.5rem 0;
    transition: var(--transition-spring);
}

.empty-state:hover {
    border-color: var(--primary);
    background: #FDFEFE;
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}

.empty-state-icon {
    font-size: 2.8rem;
    margin-bottom: 1rem;
    color: #94A3B8;
    transition: var(--transition-spring);
}

.empty-state:hover .empty-state-icon {
    transform: scale(1.15) rotate(5deg);
    color: var(--primary);
}

.empty-state-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 0.4rem;
}

.empty-state-desc {
    font-size: 0.92rem;
    color: #64748B;
    max-width: 440px;
    margin: 0 auto 1.5rem auto;
    line-height: 1.5;
}

/* ==========================================================================
   13. STREAMLIT NATIVE ELEMENT POLISH & MICRO-INTERACTIONS
   ========================================================================== */
/* Primary Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 4px rgba(79, 70, 229, 0.25) !important;
    transition: var(--transition-spring) !important;
    position: relative !important;
    overflow: hidden !important;
}

button[kind="primary"]:hover {
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.38) !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #4338CA 0%, #3730A3 100%) !important;
}

button[kind="primary"]:active {
    transform: scale(0.97) !important;
}

/* Secondary Buttons */
button[kind="secondary"] {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: var(--transition-spring) !important;
    border: 1px solid var(--border-card) !important;
}

button[kind="secondary"]:hover {
    border-color: var(--primary) !important;
    color: var(--primary) !important;
    background: var(--primary-light) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.12) !important;
}

button[kind="secondary"]:active {
    transform: scale(0.97) !important;
}

/* Streamlit Form Input Focus Polish */
input[type="text"]:focus,
input[type="number"]:focus,
textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-glow) !important;
    transition: var(--transition-fast) !important;
}

/* Hide native top nav */
div[data-testid="stSidebarNav"] {
    display: none;
}
</style>
"""

def inject_custom_css():
    """Injects the custom SaaS stylesheet into the current Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero_header(title: str, subtitle: str, badge: str = "AI Learning Platform"):
    """Renders a sleek SaaS hero header with an optional pill badge."""
    html = f"""
    <div class="hero-header">
        <div class="pill-badge">{badge}</div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_ai_status_card(is_ready: bool, model_name: str, total_chunks: int, total_files: int):
    """Renders a prominent dark-mode AI status card showing Gemini & FAISS readiness."""
    status_text = "AI Assistant Ready" if is_ready else "Vector Index Empty"
    indicator_html = (
        f'<span class="ai-status-indicator"><span class="pulsing-dot"></span>{status_text}</span>'
        if is_ready else
        '<span class="ai-status-indicator" style="background:rgba(245,158,11,0.15); color:#FBBF24; border-color:rgba(245,158,11,0.3);">⚠️ Upload Study PDF</span>'
    )

    html = f"""
    <div class="ai-status-card">
        <div>
            <div style="font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#A5B4FC; margin-bottom:0.25rem;">
                Powered by Gemini + RAG
            </div>
            <div style="font-size:1.35rem; font-weight:800; letter-spacing:-0.02em;">
                Personalized Learning Engine
            </div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:0.4rem;">
                Model: <code style="color:#C7D2FE; background:rgba(255,255,255,0.08); padding:2px 6px; border-radius:4px;">{model_name}</code>
                &nbsp;|&nbsp; Embeddings: <code style="color:#C7D2FE; background:rgba(255,255,255,0.08); padding:2px 6px; border-radius:4px;">all-MiniLM-L6-v2</code>
                &nbsp;|&nbsp; Index: <strong>{total_chunks}</strong> searchable chunks ({total_files} file{"s" if total_files != 1 else ""})
            </div>
        </div>
        <div>
            {indicator_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_metric_card(icon: str, label: str, value: Any, subtext: Optional[str] = None):
    """Renders a modern metric card with an icon bubble and clean typography."""
    sub_html = f'<div class="metric-sub">{subtext}</div>' if subtext else ''
    html = f"""
    <div class="saas-metric-card">
        <div class="metric-header">
            <span class="metric-lbl">{label}</span>
            <div class="metric-icon-bubble">{icon}</div>
        </div>
        <div class="metric-val">{value}</div>
        {sub_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_empty_state(icon: str, title: str, description: str):
    """Renders a friendly SaaS empty state box."""
    html = f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <div class="empty-state-desc">{description}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_source_chips(sources: List[Dict[str, Any]]):
    """Renders visually distinct source badges with page numbers and document labels."""
    if not sources:
        return

    chips = []
    for s in sources:
        page = s.get("page", 1)
        file_name = s.get("file_name", "Document")
        score = s.get("score", "")
        score_str = f" ({score})" if score else ""
        chips.append(f'<span class="source-badge">📄 {file_name} &bull; Page {page}{score_str}</span>')

    html = f"""
    <div class="source-container">
        <span style="font-size:0.78rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.04em;">Sources:</span>
        {' '.join(chips)}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_rag_pipeline_flow(query: str, chunk_count: int, top_score: float = 0.0):
    """
    Renders an interactive step-by-step visual pipeline showing how RAG retrieved the answer.
    Designed for demonstrations to evaluators.
    """
    html = f"""
    <div class="rag-flow-card">
        <div style="font-weight:700; font-size:0.92rem; color:#0F172A; margin-bottom:1rem; display:flex; align-items:center; gap:0.4rem;">
            <span>🔍</span> RAG Retrieval & Inference Workflow
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">1</div>
            <div>
                <div style="font-weight:700; font-size:0.88rem; color:#0F172A;">Student Query Ingestion</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:2px;">
                    Received: <em>"{query}"</em>
                </div>
            </div>
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">2</div>
            <div>
                <div style="font-weight:700; font-size:0.88rem; color:#0F172A;">Dense Semantic Embedding</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:2px;">
                    Converted query into 384-dimensional dense vector using <code>all-MiniLM-L6-v2</code>
                </div>
            </div>
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">3</div>
            <div>
                <div style="font-weight:700; font-size:0.88rem; color:#0F172A;">FAISS Vector Index Similarity Search</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:2px;">
                    Executed cosine similarity search across indexed chunks &bull; Retained top {chunk_count} matches (Top Score: {top_score:.3f})
                </div>
            </div>
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">4</div>
            <div>
                <div style="font-weight:700; font-size:0.88rem; color:#0F172A;">Context Augmentation & Prompt Injection</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:2px;">
                    Strict ground truth constraints injected into Gemini system prompt to prevent hallucinations
                </div>
            </div>
        </div>
        <div class="rag-step-item">
            <div class="rag-step-dot">5</div>
            <div>
                <div style="font-weight:700; font-size:0.88rem; color:#0F172A;">Gemini 2.5 Flash Grounded Response</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:2px;">
                    Synthesized precise answer with explicit page citations
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_agent_status_banner(tool_name: str, step_status: str = "Active"):
    """Renders the visible agent workflow card demonstrating Agentic AI behavior."""
    tool_icons = {
        "search_study_material": "🔍 Search Study Material",
        "generate_quiz": "📝 Generate Quiz",
        "calculate_quiz_score": "📊 Calculate Quiz Score",
        "create_study_plan": "📅 Create Study Plan",
        "get_student_memory": "🧠 Get Student Memory"
    }
    tool_display = tool_icons.get(tool_name, f"🛠️ {tool_name}")

    html = f"""
    <div class="agent-workflow-card">
        <span class="agent-chip">AI Agent: {step_status}</span>
        <div class="agent-step-text">
            Routed request to &rarr; <strong>{tool_display}</strong>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_performance_card(score: int, total: int, percentage: float):
    """Renders an eye-catching quiz performance summary card."""
    if percentage >= 80:
        badge_bg = "#ECFDF5"
        badge_color = "#047857"
        rating_text = "🌟 Outstanding Mastery!"
        tip = "You have an excellent grasp of these concepts. Keep reviewing to maintain memory retention!"
    elif percentage >= 60:
        badge_bg = "#EFF6FF"
        badge_color = "#1D4ED8"
        rating_text = "👍 Solid Performance!"
        tip = "Good effort! Review the questions you missed and tackle your weak topics to achieve full mastery."
    else:
        badge_bg = "#FEF2F2"
        badge_color = "#B91C1C"
        rating_text = "⚠️ Needs Focused Practice"
        tip = "Don't worry! Review the explanations below and use the Study Plan generator to target your weak spots."

    html = f"""
    <div class="perf-card">
        <div style="font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#64748B;">
            Quiz Completed 🎉
        </div>
        <div class="perf-score-display">{score} / {total}</div>
        <div class="perf-pct-pill" style="background:{badge_bg}; color:{badge_color};">
            Score: {percentage}%
        </div>
        <div class="perf-rating">{rating_text}</div>
        <div style="font-size:0.9rem; color:#64748B; max-width:550px; margin:0.5rem auto 0 auto; line-height:1.5;">
            {tip}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_weak_topic_bar(topic: str, mastery_pct: float):
    """Renders a progress bar indicating topic mastery."""
    # Color based on score
    if mastery_pct >= 75:
        bar_color = "#10B981"
        status_label = "Strong"
        bg_color = "#ECFDF5"
        text_color = "#047857"
    elif mastery_pct >= 50:
        bar_color = "#F59E0B"
        status_label = "Reviewing"
        bg_color = "#FFFBEB"
        text_color = "#B45309"
    else:
        bar_color = "#EF4444"
        status_label = "Needs Focus"
        bg_color = "#FEF2F2"
        text_color = "#B91C1C"

    html = f"""
    <div class="topic-meter-row">
        <div class="topic-meter-header">
            <span style="color:#0F172A;">{topic}</span>
            <div>
                <span style="font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:4px; background:{bg_color}; color:{text_color}; margin-right:8px;">
                    {status_label}
                </span>
                <span style="color:#475569;">{mastery_pct}%</span>
            </div>
        </div>
        <div class="meter-track">
            <div class="meter-fill" style="width: {min(100, max(5, mastery_pct))}%; background: {bar_color};"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_stepper(current_step: int = 5):
    """
    Renders the multi-step upload progress indicator:
    0: Uploading -> 1: Extracting text -> 2: Creating chunks -> 3: Generating embeddings -> 4: Building vector index -> 5: Ready
    """
    steps = [
        "Uploading",
        "Extracting text",
        "Creating chunks",
        "Generating embeddings",
        "Building vector index",
        "Ready"
    ]
    
    step_items = []
    for idx, name in enumerate(steps):
        if idx < current_step:
            css_class = "stepper-step completed"
            icon = "✓"
        elif idx == current_step:
            css_class = "stepper-step active"
            icon = str(idx + 1)
        else:
            css_class = "stepper-step"
            icon = str(idx + 1)

        step_items.append(f"""
        <div class="{css_class}">
            <div class="step-node">{icon}</div>
            <div>{name}</div>
        </div>
        """)

    html = f"""
    <div class="stepper-container">
        {''.join(step_items)}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_question_review_card(item: Dict[str, Any]):
    """
    Renders a single question review card with correct/incorrect badge and explanation.
    Uses string concatenation to guarantee zero Markdown code-block interpretation issues.
    """
    is_correct = item.get("is_correct", False)
    border_col = "#10B981" if is_correct else "#EF4444"
    badge_text = "✓ Correct" if is_correct else "✗ Incorrect"
    badge_bg = "#ECFDF5" if is_correct else "#FEF2F2"
    badge_col = "#047857" if is_correct else "#B91C1C"

    correct_block = ""
    if not is_correct:
        correct_block = (
            f'<div style="font-size:0.9rem; margin-bottom:0.4rem;">'
            f'<strong>Correct Answer:</strong> <span style="color:#047857; font-weight:600;">'
            f'{item.get("correct_option", "")}. {item.get("correct_text", "")}</span></div>'
        )

    html = (
        f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid {border_col}; border-radius:12px; padding:1.2rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.05);">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">'
        f'<span style="font-weight:700; font-size:0.95rem; color:#0F172A;">Question {item.get("id", "")}</span>'
        f'<span style="background:{badge_bg}; color:{badge_col}; font-weight:700; font-size:0.78rem; padding:2px 8px; border-radius:6px;">{badge_text}</span>'
        f'</div>'
        f'<div style="font-weight:600; font-size:1.05rem; color:#1E293B; margin-bottom:0.8rem;">{item.get("question", "")}</div>'
        f'<div style="font-size:0.9rem; margin-bottom:0.4rem;">'
        f'<strong>Your Answer:</strong> <span style="color:{badge_col}; font-weight:600;">{item.get("selected_option", "")}. {item.get("selected_text", "")}</span>'
        f'</div>'
        f'{correct_block}'
        f'<div style="font-size:0.88rem; color:#475569; background:#F8FAFC; border:1px solid #E2E8F0; padding:0.6rem 0.8rem; border-radius:6px; margin-top:0.6rem;">'
        f'💡 <strong>Explanation:</strong> {item.get("explanation", "")}'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_recent_question_card(item: Dict[str, Any]):
    """Renders a recent question card on the Dashboard."""
    q_text = item.get("question", "")
    topic = item.get("topic", "General")
    timestamp = item.get("timestamp", "")
    html = (
        f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.8rem 1rem; margin-bottom:0.6rem; display:flex; justify-content:space-between; align-items:center;">'
        f'<div>'
        f'<div style="font-weight:600; font-size:0.92rem; color:#0F172A;">"{q_text}"</div>'
        f'<div style="font-size:0.78rem; color:#64748B; margin-top:2px;">Topic: {topic} &bull; {timestamp}</div>'
        f'</div>'
        f'<span style="font-size:1.1rem; color:#4F46E5;">💬</span>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_document_card(doc: Dict[str, Any]):
    """Renders an indexed document card in the library."""
    fname = doc.get("file_name", "Document")
    pages = doc.get("total_pages", 1)
    chunks = doc.get("total_chunks", 1)
    html = (
        f'<div class="doc-card">'
        f'<div style="display:flex; align-items:center;">'
        f'<div class="doc-icon-wrap" style="background:#EEF2FF; color:#4F46E5;">📘</div>'
        f'<div>'
        f'<div class="doc-name">{fname}</div>'
        f'<div class="doc-meta">'
        f'<span>{pages} pages</span>'
        f'<span>&bull;</span>'
        f'<span>{chunks} chunks</span>'
        f'</div>'
        f'</div>'
        f'</div>'
        f'<span class="doc-status-badge">✓ Ready</span>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_timeline_day_card_header(day_number: int, title: str, is_completed: bool, is_weak: bool, weak_label: Optional[str] = None):
    """Renders the timeline day card header cleanly without markdown code block indentation issues."""
    weak_badge_html = f'<span class="weak-focus-badge">⚠️ Focus Area: {weak_label or "Weak Topic"}</span>' if is_weak else ""
    card_class = "timeline-card"
    if is_completed:
        card_class += " completed"
    elif is_weak:
        card_class += " weak-focus"

    html = (
        f'<div class="{card_class}">'
        f'<div style="display:flex; justify-content:space-between; align-items:flex-start;">'
        f'<div>'
        f'<span class="day-badge">DAY {day_number}</span>'
        f'{weak_badge_html}'
        f'<h4 style="margin:0.4rem 0 0.6rem 0; font-size:1.15rem; font-weight:700; color:#0F172A;">{title}</h4>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


