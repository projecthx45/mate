import streamlit as st
import json
from core.prompt_builder import filter_tools_by_query, load_tools_json
from core.update_prompt_builder import UpdatePromptBuilder

def render_update_plan(active_chat, idx, relevant_tools, call_gemini, extract_json_array, update_chat_plan):
    num_versions = len(active_chat['plans'])
    col_v1, col_v2, col_v3, _ = st.columns([2,1,2,8])
    with col_v1:
        select_prev = st.button("◀", key="prev_plan_btn", disabled=(idx==0), help="Previous version")
    with col_v2:
        st.markdown(f'<span style="color:#bdbdbd;font-size:0.98em;">{idx+1} of {num_versions}</span>', unsafe_allow_html=True)
    with col_v3:
        select_next = st.button("▶", key="next_plan_btn", disabled=(idx==num_versions-1), help="Next version")
    if select_prev:
        st.session_state['plan_version_idx'] = idx - 1
        st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
    if select_next:
        st.session_state['plan_version_idx'] = idx + 1
        st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
    st.markdown("### ✏️ Update Plan")
    st.session_state['update_input'] = st.text_input("Describe your update (e.g. add a step, change a tool, delete a step, etc.)", value=st.session_state.get('update_input', ''), key="update_input_box")
    if st.button("Update Plan", key="update_plan_btn") and st.session_state['update_input']:
        current_plan = active_chat['plans'][idx]['plan']
        all_tools = load_tools_json()
        combined_query = active_chat['user_query'] + ' ' + st.session_state['update_input']
        strict_relevant_tools = filter_tools_by_query(combined_query, all_tools, top_n=12)
        update_instruction = st.session_state['update_input']
        update_prompt = UpdatePromptBuilder.build_update_prompt(
            active_chat['user_query'],
            current_plan,
            update_instruction,
            strict_relevant_tools
        )
        with st.spinner("Preparing workflow..."):
            try:
                response = call_gemini(update_prompt)
            except Exception as e:
                st.error(f"Sorry, there was an error updating the plan: {e}")
                st.stop()
            with st.expander("[Debug] Raw LLM Response (Update)", expanded=False):
                st.code(response)
            new_plan = None
            try:
                parsed = json.loads(response)
                new_plan = parsed if isinstance(parsed, list) else parsed.get('plan', [])
            except Exception:
                new_plan = extract_json_array(response)
            if not new_plan or not isinstance(new_plan, list) or len(new_plan) == 0:
                st.error("Sorry, I couldn't generate a valid updated plan. Please try rephrasing your update.")
                st.stop()
            update_chat_plan(active_chat['id'], new_plan, None, strict_relevant_tools)
            st.session_state['update_input'] = ""
            st.session_state['plan_version_idx'] = len(active_chat['plans']) - 1
            st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun() 