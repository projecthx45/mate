import streamlit as st

def render_sidebar(session_state, set_active_chat, delete_chat):
    st.markdown("<h3 style='margin-bottom:0.5em;'>💬 Chat History</h3>", unsafe_allow_html=True)
    if st.button("➕ New Chat", key="new_chat_btn", use_container_width=True):
        session_state['user_query'] = ""
        session_state['active_chat_id'] = None
        session_state['update_input'] = ""
    st.markdown("---")
    for chat in reversed(session_state['chat_history']):
        is_active = chat['id'] == session_state['active_chat_id']
        label = chat['user_query'][:40] + ("..." if len(chat['user_query']) > 40 else "")
        col1, col2 = st.columns([8,1])
        with col1:
            if st.button(label, key=f"chat_{chat['id']}", use_container_width=True):
                set_active_chat(chat['id'])
        with col2:
            if st.button("🗑️", key=f"del_{chat['id']}", use_container_width=True):
                delete_chat(chat['id'])
                st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
    st.markdown("---") 