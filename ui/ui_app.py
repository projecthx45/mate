import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from core.prompt_builder import build_prompt, load_tools_json, filter_tools_by_query, extract_json_array
from core.openrouter_api import call_gemini
from ui.sidebar import render_sidebar
from ui.plan_display import render_plan
from ui.update_plan import render_update_plan
from core.update_prompt_builder import UpdatePromptBuilder
import json
import random

st.set_page_config(page_title="Toolmate", page_icon="🤖", layout="wide")

st.markdown('<h1 style="text-align:center;">🤖 Toolmate</h1>', unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'active_chat_id' not in st.session_state:
    st.session_state['active_chat_id'] = None
if 'user_query' not in st.session_state:
    st.session_state['user_query'] = ""
if 'trigger_generate' not in st.session_state:
    st.session_state['trigger_generate'] = False
if 'update_input' not in st.session_state:
    st.session_state['update_input'] = ""

def get_random_prompt():
    try:
        with open(os.path.join(os.path.dirname(__file__), '../data/sample_prompts.txt'), 'r', encoding='utf-8') as f:
            prompts = [line.strip() for line in f if line.strip()]
        return random.choice(prompts) if prompts else ""
    except Exception:
        return ""

def add_new_chat(user_query, plan, reasoning, relevant_tools):
    chat_id = str(random.getrandbits(48))
    st.session_state['chat_history'].append({
        'id': chat_id,
        'user_query': user_query,
        'plans': [{'plan': plan, 'reasoning': reasoning, 'relevant_tools': relevant_tools}],
    })
    st.session_state['active_chat_id'] = chat_id

def update_chat_plan(chat_id, new_plan, new_reasoning, relevant_tools):
    for chat in st.session_state['chat_history']:
        if chat['id'] == chat_id:
            chat['plans'].append({'plan': new_plan, 'reasoning': new_reasoning, 'relevant_tools': relevant_tools})
            break

def delete_chat(chat_id):
    st.session_state['chat_history'] = [c for c in st.session_state['chat_history'] if c['id'] != chat_id]
    if st.session_state['active_chat_id'] == chat_id:
        st.session_state['active_chat_id'] = None

def get_active_chat():
    for chat in st.session_state['chat_history']:
        if chat['id'] == st.session_state['active_chat_id']:
            return chat
    return None

def set_active_chat(chat_id):
    st.session_state['active_chat_id'] = chat_id
    chat = get_active_chat()
    if chat:
        st.session_state['user_query'] = chat['user_query']

def revert_to_plan_version(chat_id, version_idx):
    chat = next((c for c in st.session_state['chat_history'] if c['id'] == chat_id), None)
    if chat and 0 <= version_idx < len(chat['plans']):
        chat['plans'] = chat['plans'][:version_idx+1]

with st.sidebar:
    render_sidebar(st.session_state, set_active_chat, delete_chat)

active_chat = get_active_chat()
if not active_chat:
    
    col1, col2, col3 = st.columns([10,1,2])
    with col1:
        user_query = st.text_input(
            label="",
            value=st.session_state['user_query'],
            key="user_query_input",
            placeholder="e.g. Summarize this CSV and email it to my manager",
            label_visibility="collapsed"
        )
    st.markdown("""
        <style>
        div[data-testid="column"] button {
            min-height: 2.8em !important;
            height: 2.8em !important;
            padding-top: 0.2em !important;
            padding-bottom: 0.2em !important;
            font-size: 1.2em !important;
            margin-top: 0.1em !important;
        }
        div[data-testid="column"] button span {
            font-size: 1.2em !important;
        }
        </style>
    """, unsafe_allow_html=True)
    with col2:
        surprise_clicked = st.button("🎲", key="surprise_btn", help="Surprise Me", use_container_width=True)
    with col3:
        generate_clicked = st.button("Generate", use_container_width=True)
    if surprise_clicked:
        st.session_state['user_query'] = get_random_prompt()
        st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
    if user_query != st.session_state.get('user_query', ''):
        st.session_state['user_query'] = user_query
        generate_clicked = True
else:
    generate_clicked = False

TOOL_LABELS = {
    "get_invoices_tool": ("🗂️ Get Invoices", "step"),
    "calculate_invoice_total_tool": ("🧮 Calculate Total", "step"),
    "generate_email_body_tool": ("✉️ Generate Email", "step"),
    "send_email_tool": ("📤 Send Email", "step"),
    "summarize_text_tool": ("📝 Summarize Text", "step"),
    "parse_csv_tool": ("📊 Parse CSV", "step"),
    "send_sms_tool": ("📱 Send SMS", "step"),
    "summarize_numeric_tool": ("📈 Summarize Numbers", "step"),
    "readExcelTool": ("📗 Read Excel", "step"),
    "extractTablesTool": ("📋 Extract Tables", "step"),
    "pivotTableTool": ("🔀 Pivot Table", "step"),
    "groupByCategoryTool": ("🧩 Group by Category", "step"),
    "calculateSumTool": ("➕ Sum", "step"),
    "generateSummaryPDFTool": ("📄 PDF Report", "step"),
    "generateEmailTool": ("📝 Compose Email", "step"),
    "formatSMSTool": ("✏️ Format SMS", "step"),
    "sendSMSTool": ("📲 Send SMS", "step"),
    "Output": ("✅ Output", "output"),
}

active_chat = get_active_chat()
if generate_clicked and user_query and not active_chat:
    with st.spinner("Planning your workflow..."):
        all_tools = load_tools_json()
        relevant_tools = filter_tools_by_query(user_query, all_tools, top_n=12)
        if not relevant_tools:
            st.warning("No relevant tools found for your query. Try rephrasing.")
            st.stop()
        prompt = build_prompt(user_query, relevant_tools)
        try:
            response = call_gemini(prompt)
        except Exception as e:
            st.error(f"Sorry, there was an error contacting the AI model: {e}")
            st.stop()
        with st.expander("[Debug] Raw LLM Response", expanded=False):
            st.code(response)
        plan, reasoning = None, None
        try:
            parsed = json.loads(response)
            plan = parsed if isinstance(parsed, list) else parsed.get('plan', [])
            reasoning = parsed.get('reasoning', None) if isinstance(parsed, dict) else None
        except Exception:
            plan = extract_json_array(response)
            reasoning = None
        if not plan or not isinstance(plan, list) or len(plan) == 0:
            st.error("Sorry, I couldn't generate a valid plan for your request. Please try rephrasing, or check your API/model settings.")
            st.stop()
    add_new_chat(user_query, plan, reasoning, relevant_tools)
    st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()

active_chat = get_active_chat()
if active_chat:
    if 'plan_version_idx' not in st.session_state or st.session_state['active_chat_id'] != active_chat['id']:
        st.session_state['plan_version_idx'] = len(active_chat['plans']) - 1
    num_versions = len(active_chat['plans'])
    idx = st.session_state['plan_version_idx']
    if idx < 0:
        idx = 0
    if idx > num_versions - 1:
        idx = num_versions - 1
    st.session_state['plan_version_idx'] = idx
    plan_version = active_chat['plans'][idx]
    plan = plan_version['plan']
    reasoning = plan_version.get('reasoning', None)
    relevant_tools = plan_version.get('relevant_tools', [])
    st.markdown(f"### 📝 Your Task\n> {active_chat['user_query']}")
    render_plan(plan, relevant_tools, TOOL_LABELS)
    if reasoning:
        st.markdown("### 🤔 Why these functions?")
        st.info(reasoning)
    render_update_plan(active_chat, idx, relevant_tools, call_gemini, extract_json_array, update_chat_plan)