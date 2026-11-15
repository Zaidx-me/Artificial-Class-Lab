"""Component 8: Streamlit dashboard for the Agentic Recruitment & Screening System."""
import base64
import re
import time
from html import escape

import pandas as pd
import streamlit as st

import config
from agent import RecruitmentAgent
from llm import get_llm
from tools import database as db
from tools.email_tool import check_imap_connection
from tools.knowledge_tool import reload_index

# Geometric mark (4-point spark), served as a data URI so the favicon stays an
# inline SVG instead of an emoji glyph.
_PAGE_ICON = (
    "data:image/svg+xml;base64,"
    "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiI+"
    "PHBhdGggZD0iTTggMS40bDEuOSA0LjcgNC43IDEuOS00LjcgMS45TDggMTQuNmwtMS45LTQuN0wxLjQg"
    "OGw0LjctMS45eiIgZmlsbD0iIzBGOEE2MyIvPjwvc3ZnPg=="
)

st.set_page_config(page_title="AI Recruitment Agent", page_icon=_PAGE_ICON, layout="wide")
db.init_db()

APP_CSS = """<style>
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root, html, body {
    --bg: #f9fafb;
    --surface: #ffffff;
    --line: #e2e8f0;
    --ink: #18181b;
    --muted: #71717a;
    --accent: #0F8A63;
    --font-sans: "Satoshi", ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    --ease: cubic-bezier(.16, 1, .3, 1);
    --radius: 10px;
    --shadow: 0 1px 2px rgba(24, 24, 27, .05);
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 16px;
    --space-4: 24px;
    --space-5: 32px;
    color-scheme: light;
}
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: var(--font-sans);
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}
h1, h2, h3, h4,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
.app-header h1,
.empty-state h3 {
    font-family: var(--font-sans) !important;
    font-weight: 700;
    letter-spacing: -0.025em;
}
code, pre, kbd, .mono,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
.run-step .meta {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
}
/* The app is intentionally a single light theme. Streamlit 1.51 paints its own
   text with generated classes, so when the viewer's browser is in dark mode the
   default text turns white on top of this light background. Pin the surface and
   the text colours so the UI is readable no matter what the browser/OS prefers. */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
.stApp {
    background: var(--bg) !important;
    color: var(--ink) !important;
    color-scheme: light;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
[data-testid="stMainBlockContainer"] {
    padding-top: var(--space-5) !important;
}
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-baseweb="tab"] {
    color: var(--ink) !important;
}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
[data-testid="stWidgetLabel"] label {
    color: var(--muted) !important;
}
/* Sidebar: one plane deeper than the canvas so white content reads raised. */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: #f1f3f5 !important;
}
section[data-testid="stSidebar"] {
    position: relative;
    border-right: 1px solid var(--line);
}
/* Vertical brand rail: the sidebar's signature edge. */
section[data-testid="stSidebar"]::before {
    content: "RECRUITMENT AGENT";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 2;
    width: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-right: 1px solid var(--line);
    background:
        linear-gradient(var(--accent), var(--accent)) 21px 2.4rem / 1px 24px no-repeat,
        linear-gradient(var(--accent), var(--accent)) 21px calc(100% - 2.4rem) / 1px 24px no-repeat;
    color: var(--muted);
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    writing-mode: vertical-rl;
    pointer-events: none;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: var(--ink) !important;
}
/* Clear the rail and stagger the stacked sections in. */
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding-left: 34px !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"],
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"] {
    animation: rise-in .45s var(--ease) both;
    animation-delay: calc(var(--i, 0) * 60ms);
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(1) { --i: 0; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(2) { --i: 1; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(3) { --i: 2; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(4) { --i: 3; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(5) { --i: 4; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(6) { --i: 5; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(7) { --i: 6; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(8) { --i: 7; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(9) { --i: 8; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(10) { --i: 9; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(11) { --i: 10; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(12) { --i: 11; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(13) { --i: 12; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(14) { --i: 13; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(15) { --i: 14; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(16) { --i: 15; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(17) { --i: 16; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(18) { --i: 17; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(19) { --i: 18; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"] > :nth-child(20) { --i: 19; }
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: var(--space-3) !important;
}
section[data-testid="stSidebar"] h1 {
    font-size: 1.05rem;
    letter-spacing: -0.02em;
    margin-bottom: 0.1rem;
}
/* Hairline rule above an uppercase mono micro-label, rhythm from space only. */
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    display: block;
    margin: var(--space-2) 0 calc(-1 * var(--space-2));
    padding: 0;
    border: 0;
    font-family: var(--font-mono) !important;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted) !important;
}
section[data-testid="stSidebar"] h2::before,
section[data-testid="stSidebar"] h3::before {
    content: "";
    display: block;
    width: 20px;
    height: 1px;
    margin-bottom: var(--space-2);
    background: var(--accent);
}
/* Keep form controls light so they don't turn into dark boxes on the light page. */
[data-baseweb="input"],
[data-baseweb="textarea"],
[data-baseweb="select"] > div,
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background-color: var(--surface) !important;
    border-radius: var(--radius) !important;
}
[data-baseweb="input"],
[data-baseweb="textarea"] {
    border: 1px solid var(--line) !important;
    box-shadow: none !important;
}
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(15, 138, 99, .10) !important;
}
/* The chat wrap is the single focus indicator. Streamlit's own primaryColor
   focus border on the inner div stays transparent in both rest and focus. */
[data-testid="stChatInput"] {
    border: 1px solid var(--line) !important;
    box-shadow: 0 10px 30px -18px rgba(24, 24, 27, .30) !important;
    transition: border-color .3s cubic-bezier(.16, 1, .3, 1),
                box-shadow .3s cubic-bezier(.16, 1, .3, 1);
}
[data-testid="stChatInput"] > div {
    border-color: transparent !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(15, 138, 99, .12) !important;
}
/* Sidebar controls: single indicator, hairline-only treatments. */
section[data-testid="stSidebar"] [data-baseweb="input"] {
    background: transparent !important;
    border: 0 !important;
    border-bottom: 1px solid var(--line) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    transition: border-color .3s cubic-bezier(.16, 1, .3, 1);
}
section[data-testid="stSidebar"] [data-baseweb="input"] > div {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] [data-baseweb="input"]:focus-within {
    border-bottom-color: var(--accent) !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] [data-baseweb="textarea"] {
    background: transparent !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius) !important;
    box-shadow: none !important;
    transition: border-color .3s cubic-bezier(.16, 1, .3, 1);
}
section[data-testid="stSidebar"] [data-baseweb="textarea"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] [role="radiogroup"] {
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: var(--space-2);
    background: transparent;
    transition: border-color .3s cubic-bezier(.16, 1, .3, 1);
}
section[data-testid="stSidebar"] [role="radiogroup"]:focus-within {
    border-color: var(--accent);
}
section[data-testid="stSidebar"] .stButton > button {
    background: var(--surface);
}
section[data-testid="stSidebar"] .stButton > button:active {
    transform: translateY(1px) scale(.98);
}
input, textarea, select,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    color: var(--ink) !important;
}
::placeholder {
    color: var(--muted) !important;
    opacity: 1;
}
/* Asymmetric header: left-weighted title block, right-anchored status stack. */
.app-header {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: start;
    gap: var(--space-5);
    padding: var(--space-5) 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: var(--space-4);
}
.header-main {
    max-width: 60ch;
    padding-right: 0;
}
.header-eyebrow {
    margin: 0 0 var(--space-2);
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
}
.app-header h1 {
    margin: 0;
    font-size: clamp(1.55rem, 1.3rem + 0.9vw, 2rem);
    line-height: 1.12;
    letter-spacing: -0.03em;
    font-weight: 700;
    color: var(--ink);
    text-wrap: balance;
}
.app-header .header-sub {
    margin: var(--space-2) 0 0;
    max-width: 54ch;
    color: var(--muted);
    font-size: 0.95rem;
    line-height: 1.55;
    text-wrap: pretty;
}
.status-row {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: flex-end;
    gap: var(--space-2);
    max-width: 34rem;
    padding-top: 0;
}
.header-main > *,
.status-row > * {
    animation: rise-in .55s var(--ease) both;
    animation-delay: calc(var(--i, 0) * 60ms);
}
@keyframes rise-in {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
.status-pill {
    position: relative;
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    min-height: var(--space-5);
    padding: 0 var(--space-3);
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, .65);
    background: linear-gradient(135deg, rgba(255, 255, 255, .92), rgba(255, 255, 255, .58));
    backdrop-filter: blur(14px) saturate(1.4);
    -webkit-backdrop-filter: blur(14px) saturate(1.4);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, .9),
        0 0 0 1px rgba(24, 24, 27, .06),
        0 2px 6px -2px rgba(24, 24, 27, .10);
    color: var(--ink);
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    font-variant-numeric: tabular-nums;
    transition: border-color .3s cubic-bezier(.16, 1, .3, 1),
                color .3s cubic-bezier(.16, 1, .3, 1),
                transform .3s cubic-bezier(.16, 1, .3, 1),
                box-shadow .3s cubic-bezier(.16, 1, .3, 1);
}
.status-pill--idle {
    color: var(--muted);
}
.kpi-num {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
}
.kpi-truncate {
    display: inline-block;
    max-width: 12rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    vertical-align: bottom;
}
.status-pill:hover {
    border-color: rgba(15, 138, 99, .35);
    transform: translateY(-1px);
}
.status-dot {
    position: relative;
    z-index: 1;
    flex: 0 0 auto;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: breathe 2.8s ease-in-out infinite;
}
.status-dot--idle {
    background: var(--muted);
    animation: none;
    opacity: .6;
}
@keyframes breathe {
    0%, 100% { transform: scale(.85); opacity: .55; }
    50% { transform: scale(1.3); opacity: 1; }
}
/* Shimmer is reserved for the single live/running pill. */
.status-pill--live::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(100deg, transparent 25%, rgba(255, 255, 255, .8) 50%, transparent 75%);
    transform: translateX(-130%);
    animation: shimmer 4.6s var(--ease) infinite;
    pointer-events: none;
}
@keyframes shimmer {
    0%, 55% { transform: translateX(-130%); }
    100% { transform: translateX(130%); }
}
/* Pending drafts: hairline strip under the header, one line per draft. */
.drafts-strip {
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    padding: var(--space-2) 0;
    margin: 0 0 var(--space-3);
    animation: rise-in .4s var(--ease) both;
}
.drafts-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: var(--space-2);
}
.drafts-title {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    font-family: var(--font-mono);
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
}
.drafts-title svg {
    color: var(--accent);
}
.drafts-count {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-variant-numeric: tabular-nums;
    color: var(--muted);
}
.drafts-rows {
    display: grid;
    gap: var(--space-1);
    margin-top: var(--space-2);
}
.draft-row {
    display: flex;
    align-items: baseline;
    gap: var(--space-2);
    min-width: 0;
    font-size: 0.88rem;
    line-height: 1.5;
}
.draft-id {
    flex: 0 0 auto;
    font-family: var(--font-mono);
    color: var(--accent);
}
.draft-arrow,
.draft-sep {
    flex: 0 0 auto;
    color: var(--muted);
}
.draft-to {
    flex: 0 0 auto;
    max-width: 22ch;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--ink);
}
.draft-subject {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: var(--muted);
}
[data-testid="stChatMessage"] {
    background: var(--surface);
    color: var(--ink);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: var(--space-3);
    margin-bottom: var(--space-3);
    box-shadow: var(--shadow);
    animation: rise-in .4s var(--ease) both;
}
[data-testid="stChatMessage"] p {
    line-height: 1.6;
}
.stButton > button, .stDownloadButton > button {
    min-height: 2.45rem;
    border-radius: var(--radius);
    border: 1px solid var(--line);
    background: var(--surface);
    color: var(--ink);
    font-weight: 500;
    letter-spacing: -0.005em;
    box-shadow: 0 1px 1px rgba(24, 24, 27, .03);
    transition: border-color .3s cubic-bezier(.16, 1, .3, 1),
                background-color .3s cubic-bezier(.16, 1, .3, 1),
                color .3s cubic-bezier(.16, 1, .3, 1),
                transform .3s cubic-bezier(.16, 1, .3, 1),
                box-shadow .3s cubic-bezier(.16, 1, .3, 1);
}
.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: rgba(15, 138, 99, .45);
    background: rgba(15, 138, 99, .05);
    color: var(--accent);
}
.stButton > button:active, .stDownloadButton > button:active {
    transform: translateY(1px) scale(.98);
    box-shadow: none;
}
.stButton > button[kind="primary"] {
    background: var(--accent);
    border-color: var(--accent);
    color: #ffffff;
    box-shadow: 0 1px 2px rgba(15, 138, 99, .28);
}
.stButton > button[kind="primary"]:hover {
    background: #0c7654;
    border-color: #0c7654;
    color: #ffffff;
}
.stTabs [data-baseweb="tab-list"] {
    gap: var(--space-4);
    border-bottom: 1px solid var(--line);
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    padding: var(--space-2) 0;
    background: transparent;
    color: var(--muted) !important;
    font-weight: 500;
    letter-spacing: -0.01em;
    animation: rise-in .5s var(--ease) both;
    animation-delay: calc(var(--i, 0) * 60ms);
}
.stTabs [data-baseweb="tab"]:nth-child(1) { --i: 0; }
.stTabs [data-baseweb="tab"]:nth-child(2) { --i: 1; }
.stTabs [data-baseweb="tab"]:nth-child(3) { --i: 2; }
.stTabs [data-baseweb="tab"]:nth-child(4) { --i: 3; }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: var(--ink) !important;
    font-weight: 600;
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color: var(--accent) !important;
    height: 2px;
}
.stTabs [data-baseweb="tab-border"] {
    background: transparent !important;
}
/* Leaderboard metrics: unboxed, separated by negative space and a single rule. */
[data-testid="stMetric"] {
    background: transparent;
    border: 0;
    border-top: 1px solid var(--line);
    border-radius: 0;
    padding: var(--space-3) 0 0;
    box-shadow: none;
}
[data-testid="stMetricLabel"] p {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted) !important;
}
[data-testid="stMetricValue"] {
    color: var(--ink) !important;
    font-weight: 500;
    letter-spacing: -0.02em;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stExpander"] {
    border-radius: 12px;
}
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
    border-radius: 12px;
    border-color: var(--line);
}
[data-testid="stExpander"] summary {
    transition: border-color .3s cubic-bezier(.16, 1, .3, 1),
                background-color .3s cubic-bezier(.16, 1, .3, 1);
}
[data-testid="stExpander"] summary:hover {
    border-color: var(--line);
    background: rgba(24, 24, 27, .02);
}
.empty-state {
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: var(--space-4);
    background: var(--surface);
    color: var(--ink);
    margin: var(--space-2) 0 var(--space-3);
    box-shadow: var(--shadow);
}
.empty-state h3 {
    margin: 0;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--ink);
}
.empty-state p {
    margin: var(--space-2) 0 0;
    max-width: 60ch;
    color: var(--muted);
}
.empty-state .empty-hint {
    font-size: 0.88rem;
}
/* Live run panel: one divided row per completed agent step, never a card. */
.run-timeline {
    display: flex;
    flex-direction: column;
    margin: var(--space-1) 0 0;
}
.run-step {
    display: flex;
    align-items: baseline;
    gap: var(--space-2);
    padding: var(--space-1) 0;
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--ink);
}
.run-step + .run-step {
    border-top: 1px solid var(--line);
}
.run-step .icon {
    flex: 0 0 auto;
    display: inline-flex;
    align-self: center;
    color: var(--accent);
}
.run-step .icon svg {
    display: block;
}
.run-step .label {
    flex: 0 0 auto;
    font-weight: 600;
    letter-spacing: -0.005em;
    white-space: nowrap;
}
.run-step .meta {
    min-width: 0;
    color: var(--muted);
    font-size: 0.78rem;
    overflow-wrap: anywhere;
}
.caret {
    display: inline-block;
    width: 0.5ch;
    height: 1.05em;
    margin-left: 2px;
    vertical-align: -0.15em;
    border-radius: 1px;
    background: currentColor;
    animation: caret-blink 1s steps(2, start) infinite;
}
@keyframes caret-blink {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0; }
}
::selection {
    background: rgba(15, 138, 99, .18);
    color: var(--ink);
}
button:focus-visible,
[role="button"]:focus-visible,
[data-baseweb="tab"]:focus-visible,
summary:focus-visible,
input[type="checkbox"]:focus-visible,
input[type="radio"]:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}
@media (max-width: 1100px) {
    .app-header {
        grid-template-columns: minmax(0, 1fr);
        gap: var(--space-3);
    }
    .status-row {
        max-width: none;
        justify-content: flex-start;
        padding-top: var(--space-2);
    }
}
@media (max-width: 767px) {
    .app-header {
        grid-template-columns: minmax(0, 1fr);
        gap: var(--space-3);
        padding-bottom: var(--space-5);
    }
    .header-main {
        padding-right: 0;
    }
    .status-row {
        flex-direction: row;
        flex-wrap: wrap;
        align-items: flex-start;
        padding-top: 0;
    }
    section[data-testid="stSidebar"]::before {
        display: none;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding-left: 0 !important;
    }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
    }
    .status-dot {
        animation: none;
        opacity: 1;
        transform: none;
    }
    .status-pill--live::after {
        display: none;
    }
}
</style>"""

st.markdown(APP_CSS, unsafe_allow_html=True)

_ICON_PATHS = {
    "check": '<path d="M3.4 8.3l3 3.1 6.2-7.2"/>',
    "mail": '<rect x="2" y="3.75" width="12" height="8.5" rx="1.5"/><path d="M2.7 4.8L8 8.4l5.3-3.6"/>',
    "timer": '<circle cx="8" cy="8.9" r="4.6"/><path d="M8 6.4v2.6l1.7 1"/><path d="M6.3 2.1h3.4"/>',
    "search": '<circle cx="7.1" cy="7.1" r="4.1"/><path d="M10.3 10.3l3 3"/>',
    "warn": '<path d="M8 2.7l5.5 10.2H2.5L8 2.7z"/><path d="M8 6.3v2.7"/><path d="M8 11h.01"/>',
}


def icon_svg(name, size=14):
    """Return an inline SVG icon at stroke 1.5 that inherits the surrounding colour."""
    return (
        f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 16 16" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{_ICON_PATHS[name]}</svg>'
    )


def icon_label(name, text, color="#18181b"):
    """Build an expander/status label with the icon embedded as a Markdown data-URI image."""
    svg = icon_svg(name).replace(' class="icon"', "").replace('stroke="currentColor"', f'stroke="{color}"')
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"![{name}]({uri}) {text}"


ACTION_REPLIES = re.compile(
    r"^(?:yes|yeah|yep|sure|ok|okay|go ahead|go for it|do it|please do|check|check now|check it|check inbox|check the inbox|check email|check emails|check new applications|check new emails|any new(?: applications| emails)?|anything new)(?: please)?[.! ]*$",
    re.I,
)


def expand_action(prompt, job_title):
    """Expand a short affirmative reply into a full inbox-processing prompt.

    Args:
        prompt: Raw user message; may be ``None``.
        job_title: Current job title used to scope the request.

    Returns:
        The expanded prompt when ``prompt`` is an affirmative reply,
        otherwise the original ``prompt`` unchanged.
    """
    if prompt and ACTION_REPLIES.fullmatch(prompt.strip()):
        return f"Process all new applicant emails for the {job_title} role."
    return prompt

# ---------------------------------------------------------------- sidebar
sb = st.sidebar
sb.title("Recruitment Agent")

# The LLM is shown once, as a header chip; the sidebar keeps only its model.
llm = get_llm()
llm_mode = "Offline demo" if llm.name == "mock" else getattr(llm, "model", config.LLM_MODEL)

# 1 · Role
sb.subheader("Role")
jobs = db.get_jobs()
sample_jd = (config.BASE_DIR / "assets" / "sample_jd.txt").read_text()
job_title = sb.text_input("Job title", value="Software Engineer")
jd = sb.text_area("Job description", value=(db.get_job(job_title) or {}).get("description", sample_jd), height=200)
if sb.button("Save job"):
    db.save_job(job_title, jd)
    sb.success("Job saved")

# 2 · Inbox source
sb.subheader("Inbox source")
gmail_ready = bool(config.EMAIL_USER and config.EMAIL_PASS)
email_source = sb.radio(
    "Source",
    ["Local demo inbox", "Gmail inbox"],
    index=1 if gmail_ready else 0,
    help="Email checks are on-demand. Credentials are read from .env (EMAIL_USER / EMAIL_PASS).",
)
gmail_selected = email_source == "Gmail inbox"
only_applications = False
email_limit = 20

if gmail_selected:
    if gmail_ready:
        sb.caption(f"Gmail account: {config.EMAIL_USER}")
    else:
        sb.warning("Gmail isn't configured. Set EMAIL_USER and EMAIL_PASS in .env, or use the local demo inbox.")
    only_applications = sb.checkbox(
        "Only process application-looking emails",
        value=True,
        help="Keeps emails with a PDF/DOCX/TXT attachment or application keywords in the subject/body.",
    )
    email_limit = sb.number_input(
        "Max emails to process per check",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
        help="Stops after this many matching emails. Non-matching unread messages are scanned but not processed.",
    )
    if gmail_ready and sb.button("Test Gmail connection"):
        result = check_imap_connection(config.EMAIL_USER, config.EMAIL_PASS, config.IMAP_SERVER)
        if result["ok"]:
            sb.success(result["message"])
        else:
            sb.error(result["error"])
else:
    sb.caption("Using `assets/inbox/*.eml` — no credentials needed.")

# 3 · Uploads
sb.subheader("Uploads")
uploads = sb.file_uploader("Upload resumes (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
if uploads:
    config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for u in uploads:
        (config.UPLOAD_DIR / u.name).write_bytes(u.getvalue())
    sb.info(f"{len(uploads)} file(s) queued. Ask the agent to process them.")

# 4 · Session
sb.subheader("Session")
if sb.button("Reset candidates & memory"):
    db.clear_candidates(); db.clear_memory(); st.session_state.pop("chat", None)
    sb.success("Cleared"); st.rerun()

# 5 · How-to: setup reference and usage, kept out of the operating compartments
sb.subheader("How-to")
with sb.expander("Gmail setup (.env)"):
    # st.markdown, not sb.markdown: sb bypasses the expander context and
    # renders this as a sibling after the closed expander (leaks outside).
    st.markdown(
        "Set these keys in the project's `.env` file:\n\n"
        "```\nEMAIL_USER=you@gmail.com\nEMAIL_PASS=your-16-character-app-password\nIMAP_SERVER=imap.gmail.com\n```\n\n"
        "Create the app password in **Google Account → Security → 2-Step Verification → App passwords**.\n"
        "Application checks read only unread messages; general email questions search the inbox read-only."
    )
with sb.expander("Usage tips"):
    # st.markdown, not sb.markdown — same expander-context trap as above.
    st.markdown(
        "- Checks are on demand: nothing polls your inbox in the background.\n"
        "- Drafts are written before anything sends, so you can review recipient and wording.\n"
        "- Ask in chat for rankings, candidate details, or inbox searches.\n"
        "- Process new applications runs the full pipeline on unread mail."
    )

db.save_job(job_title, jd)
agent = RecruitmentAgent(
    job_title,
    jd,
    llm=llm,
    email_user=config.EMAIL_USER if gmail_selected else "",
    email_password=config.EMAIL_PASS if gmail_selected else "",
    imap_server=config.IMAP_SERVER if gmail_selected else None,
    email_filter_applications=only_applications,
    email_mode="imap" if gmail_selected else "local",
    email_limit=int(email_limit),
)

# ---------------------------------------------------------------- main
pending_drafts = db.list_drafts("pending")
candidate_count = len(db.get_ranked_candidates(job_title))
draft_chip_idle = "" if pending_drafts else " status-pill--idle"
candidate_chip_idle = "" if candidate_count else " status-pill--idle"

st.markdown(
    f"""
    <div class="app-header">
      <div class="header-main">
        <p class="header-eyebrow" style="--i:0">Talent operations</p>
        <h1 style="--i:1">Agentic AI Recruitment &amp; Applicant Ranking</h1>
        <p class="header-sub" style="--i:2">Screen applications, search your inbox, and rank the shortlist. Email checks run only when you ask.</p>
      </div>
      <div class="status-row">
        <span class="status-pill{draft_chip_idle}" style="--i:3"><span class="status-dot status-dot--idle"></span>Drafts <span class="kpi-num">· {len(pending_drafts)}</span></span>
        <span class="status-pill{candidate_chip_idle}" style="--i:4"><span class="status-dot status-dot--idle"></span>Candidates <span class="kpi-num">· {candidate_count}</span></span>
        <span class="status-pill status-pill--live" style="--i:5" title="LLM: {escape(llm_mode)}"><span class="status-dot"></span>LLM <span class="kpi-num kpi-truncate">· {escape(llm_mode)}</span></span>
        <span class="status-pill" style="--i:6"><span class="status-dot status-dot--idle"></span>{escape(email_source)}</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Root-level strip: sibling of st.chat_input, between the header and the composer.
if pending_drafts:
    visible_drafts = pending_drafts[:4]
    hidden_drafts = len(pending_drafts) - len(visible_drafts)
    draft_rows = "".join(
        f'<div class="draft-row"><span class="draft-id">#{d["id"]}</span>'
        f'<span class="draft-arrow">→</span>'
        f'<span class="draft-to" title="{escape(str(d["to_addr"]))}">{escape(str(d["to_addr"]))}</span>'
        f'<span class="draft-sep">—</span>'
        f'<span class="draft-subject">{escape(str(d["subject"]))}</span></div>'
        for d in visible_drafts
    )
    if hidden_drafts:
        draft_rows += (
            f'<div class="draft-row"><span class="draft-id">+{hidden_drafts}</span>'
            f'<span class="draft-subject">more queued</span></div>'
        )
    st.markdown(
        f'<div class="drafts-strip" data-testid="drafts-strip">'
        f'<div class="drafts-head"><span class="drafts-title">{icon_svg("mail")}Pending drafts</span>'
        f'<span class="drafts-count">{len(pending_drafts):02d} queued</span></div>'
        f'<div class="drafts-rows">{draft_rows}</div></div>',
        unsafe_allow_html=True,
    )

# Keep this at the app root: Streamlit only pins st.chat_input to the bottom of the
# viewport when it has no ancestor container, so nesting it in a tab would make it scroll away.
prompt = st.chat_input("Ask about candidates, your inbox, or anything else…")

tab_chat, tab_board, tab_kb = st.tabs(["Agent", "Leaderboard", "Knowledge base"])


def render_trace(trace):
    """Render an agent tool-execution trace as a series of expanders.

    Args:
        trace: List of step dicts with ``step``, ``tool``, ``args`` and
            ``result`` keys.

    Returns:
        None. Writes the expanders to the current Streamlit container.
    """
    for t in trace:
        with st.expander(f"Step {t['step']}: `{t['tool']}`", expanded=False):
            st.json({"args": t["args"], "result": t["result"]}, expanded=False)


PROGRESS = {
    "process_new_applications": "Working through the applications…",
    "fetch_new_applications": "Checking the inbox…",
    "search_inbox": "Searching your inbox…",
    "search_knowledge": "Pulling up the hiring rubric…",
    "parse_resume": "Reading a resume…",
    "evaluate_candidate": "Scoring a candidate…",
    "save_candidate": "Saving the evaluation…",
    "skip_email": "Skipping an email with no resume…",
    "get_leaderboard": "Ranking the shortlist…",
    "get_candidate_details": "Pulling up candidate details…",
    "draft_email": "Drafting a reply…",
    "send_draft": "Sending the draft…",
    "send_batch": "Sending the batch…",
}

RESULT_THROTTLE = 0.05  # seconds between placeholder paints (~20 updates/sec)


def step_summary(tool, result):
    """Turn a tool's raw result into a short, friendly timeline summary.

    Args:
        tool: Tool name from the step event (e.g. ``"fetch_new_applications"``).
        result: The tool's return value; usually a dict, sometimes an error dict.

    Returns:
        A one-line summary string, or ``"Working…"`` for an unknown tool.
    """
    r = result if isinstance(result, dict) else {}
    if tool == "process_new_applications":
        return f"Processed {int(r.get('scored', 0) or 0)} · skipped {int(r.get('skipped', 0) or 0)}"
    if tool == "fetch_new_applications":
        return f"Checked the inbox — {int(r.get('count', 0) or 0)} new"
    if tool == "search_inbox":
        return f"Searched inbox — {int(r.get('count', 0) or 0)} found"
    if tool == "search_knowledge":
        return f"Pulled up {len(r.get('results') or [])} rubric passages"
    if tool == "parse_resume":
        name = str(r.get("path", "")).replace("\\", "/").rsplit("/", 1)[-1] or "a resume"
        return f"Read {name}"
    if tool == "evaluate_candidate":
        score = r.get("score", 0)
        try:
            score = f"{float(score):g}"
        except (TypeError, ValueError):
            score = str(score)
        return f"Scored {r.get('name') or 'a candidate'} — {score}/100"
    if tool == "save_candidate":
        return f"Saved {r.get('name') or 'the candidate'}"
    if tool == "skip_email":
        return "Skipped an email (no resume)"
    if tool == "get_leaderboard":
        return f"Ranked {int(r.get('count', 0) or 0)} candidates"
    if tool == "get_candidate_details":
        return f"Pulled up {r.get('name') or r.get('error') or 'the candidate'}"
    if tool == "draft_email":
        return f"Drafted → {r.get('to') or r.get('error') or 'a draft'}"
    if tool == "send_draft":
        if r.get("sent") or r.get("ok"):
            return f"Sent to {r.get('to') or 'the recipient'}"
        return str(r.get("error") or "Send failed")
    if tool == "send_batch":
        return f"Sent {int(r.get('sent', 0) or 0)} · failed {int(r.get('failed', 0) or 0)}"
    return "Working…"


def render_timeline(steps):
    """Render the staged run timeline as compact, theme-matched HTML rows.

    Args:
        steps: List of ``(label, summary)`` pairs, oldest first.

    Returns:
        None. Writes the timeline markup to the current Streamlit container.
    """
    if not steps:
        return
    rows = "".join(
        f'<div class="run-step"><span class="icon">{icon_svg("check")}</span>'
        f'<span class="label">{escape(label)}</span>'
        f'<span class="meta">{escape(summary)}</span></div>'
        for label, summary in steps
    )
    st.markdown(f'<div class="run-timeline">{rows}</div>', unsafe_allow_html=True)

with tab_chat:
    st.session_state.setdefault("chat", [{"role": "assistant", "content":
        "Hey! I can screen new applications, search your inbox, and talk through the shortlist. "
        "Ask me anything — 'what emails came in today?', 'find emails from Amazon', or 'who are the top candidates?'"}])

    quick_specs = (
        ("Check new applications", f"Process all new applicant emails for the {job_title} role."),
        ("Top candidates", "Who are the top candidates?"),
        ("What's in my inbox?", "What emails came in today?"),
    )
    quick_columns = st.columns(len(quick_specs))
    quick_prompt = None
    for index, (column, (label, value)) in enumerate(zip(quick_columns, quick_specs)):
        if column.button(label, key=f"quick_action_{index}", use_container_width=True):
            quick_prompt = value

    c1, c2 = st.columns([1, 3])
    quick = c1.button("Process new applications", type="primary", use_container_width=True)
    c2.caption("Runs the application pipeline on unread mail. Nothing polls in the background.")

    # Re-entered later to append new messages above the pinned chat input.
    convo = st.container()
    with convo:
        for m in st.session_state.chat:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
                if m.get("trace"):
                    render_trace(m["trace"])

    if quick:
        prompt = f"Process all new applicant emails for the {job_title} role."
    if quick_prompt:
        prompt = quick_prompt
    raw_prompt = prompt
    prompt = expand_action(prompt, job_title)
    email_intent = bool(quick) or any(
        word in (prompt or "").lower() for word in ("application", "inbox", "email", "mail", "message", "process")
    )
    if prompt and gmail_selected and email_intent and not gmail_ready:
        with convo:
            st.warning("Gmail isn't configured. Set EMAIL_USER and EMAIL_PASS in .env, or switch to the local demo inbox.")
        prompt = None
    if prompt:
        st.session_state.chat.append({"role": "user", "content": raw_prompt or prompt})
        with convo:
            with st.chat_message("user"):
                st.markdown(raw_prompt or prompt)
            with st.chat_message("assistant"):
                started = time.monotonic()
                steps = []
                stream = {"buf": "", "last": 0.0}
                status = st.status("Working…", expanded=True)
                timeline_slot = status.empty()
                answer_slot = st.empty()
                detail_slot = st.empty()

                def on_step(e):
                    """Render one completed tool step into the live run panel.

                    Args:
                        e: Step event dict with ``tool``, ``args``, ``result`` and
                            ``step`` keys.

                    Returns:
                        None. Updates the panel header and timeline in place.
                    """
                    label = PROGRESS.get(e["tool"], "Working…").rstrip("…")
                    steps.append((label, step_summary(e["tool"], e["result"])))
                    elapsed = int(time.monotonic() - started)
                    status.update(label=icon_label("timer", f"Working… · {elapsed}s"))
                    # Text streamed before a tool call is preamble, not the final answer.
                    if stream["buf"]:
                        stream["buf"] = ""
                        answer_slot.empty()
                    with timeline_slot.container():
                        render_timeline(steps)

                def on_token(chunk):
                    """Stream answer tokens into the chat placeholder, throttled.

                    Args:
                        chunk: A content delta emitted by the language model.

                    Returns:
                        None. Updates the answer placeholder in place.
                    """
                    if not chunk:
                        return
                    stream["buf"] += chunk
                    now = time.monotonic()
                    if now - stream["last"] >= RESULT_THROTTLE:
                        stream["last"] = now
                        answer_slot.markdown(stream["buf"] + '<span class="caret"></span>', unsafe_allow_html=True)

                try:
                    out = agent.run(prompt, on_step=on_step, on_token=on_token)
                    elapsed = int(round(time.monotonic() - started))
                    count = len(out["trace"])
                    plural = "" if count == 1 else "s"
                    status.update(label=icon_label("check", f"Done in {elapsed}s · {count} step{plural}", "#0F8A63"),
                                  state="complete", expanded=False)
                    answer_slot.markdown(out["answer"])
                    with detail_slot.container():
                        with st.expander(icon_label("search", f"Run details · {count} step{plural}")):
                            render_trace(out["trace"])
                    st.session_state.chat.append({"role": "assistant", "content": out["answer"], "trace": out["trace"]})
                except Exception as exc:
                    status.update(label=icon_label("warn", "Couldn't finish"), state="error", expanded=False)
                    friendly = (
                        "I couldn't reach the language model. Check that `LLM_BASE_URL`, `LLM_API_KEY` "
                        "and `LLM_MODEL` in `.env` match your provider — e.g. NVIDIA uses "
                        "`https://integrate.api.nvidia.com/v1`.\n\n"
                        f"`{type(exc).__name__}: {exc}`"
                    )
                    answer_slot.error(friendly)
                    st.session_state.chat.append({"role": "assistant", "content": friendly})

with tab_board:
    rows = db.get_ranked_candidates(job_title)
    if not rows:
        st.markdown(
            '<div class="empty-state">'
            "<h3>No candidates yet</h3>"
            "<p>Process a batch of applications to start your shortlist.</p>"
            '<p class="empty-hint">Ask the agent to check the inbox, or use “Process new applications” in the Agent tab.</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.caption("Scores and rankings appear here once at least one resume has been evaluated.")
    else:
        df = pd.DataFrame(rows)
        df.insert(0, "rank", range(1, len(df) + 1))
        m1, m2, m3 = st.columns(3)
        m1.metric("Candidates", len(df)); m2.metric("Top score", df.score.max()); m3.metric("Average", round(df.score.mean(), 1))
        st.dataframe(df[["rank", "name", "email", "score", "skills_score", "experience_score", "education_score", "recommendation"]],
                     hide_index=True, use_container_width=True)
        st.bar_chart(df.set_index("name")[["skills_score", "experience_score", "education_score"]])
        for _, r in df.iterrows():
            with st.expander(f"#{r['rank']}  {r['name']} — {r['score']}/100 · {r['recommendation']}"):
                st.markdown(f"**Justification:** {r['justification']}")
                a, b, c = st.columns(3)
                a.markdown(f"**Strengths**\n\n{r['strengths']}")
                b.markdown(f"**Weaknesses**\n\n{r['weaknesses']}")
                c.markdown(f"**Missing skills**\n\n{r['missing_skills']}")
        st.download_button("Export CSV", df.to_csv(index=False), "candidates.csv", "text/csv")

with tab_kb:
    st.caption("Documents retrieved by the agent (RAG). Edit these files to change scoring policy.")
    for f in sorted(config.KNOWLEDGE_DIR.glob("*.md")):
        with st.expander(f.name):
            st.markdown(f.read_text())
    reload_index()
