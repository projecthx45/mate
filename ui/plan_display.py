import streamlit as st

def get_tool_label(func, TOOL_LABELS):
    if func in TOOL_LABELS:
        return TOOL_LABELS[func][0], TOOL_LABELS[func][1]
    return f"🛠️ {func.replace('_', ' ').title()}", "step"

def get_input_placeholder(key):
    
    mapping = {
        'transactions': 'list[dict] - a list of transactions',
        'content': 'string - the message content',
        'recipients': 'list[str] - recipient phone numbers',
        'to': 'string - recipient contact',
        'file': 'string - file path or name',
        'data': 'dict - structured data',
        'query': 'string - search query',
        'date': 'string - date value',
        'amount': 'float - transaction amount',
        'title': 'string - title or subject',
        
    }
    return mapping.get(key, 'No value provided')

def render_plan(plan, relevant_tools, TOOL_LABELS):
    st.markdown("### 🧠 Task Plan (Visual Diagram)")
    flow_parts = []
    for i, step in enumerate(plan):
        func = step.get('function', f"Step{i+1}")
        label, _ = get_tool_label(func, TOOL_LABELS)
        flow_parts.append(label)
    flow_parts.append("✅ Output")
    flow_str = "<br><span style='font-size:2em;color:#ffb300;'>↓</span><br>".join([f"<span style='font-size:1.2em;'>{part}</span>" for part in flow_parts])
    st.markdown(f"<div style='text-align:center;padding:1.5em 0;'>{flow_str}</div>", unsafe_allow_html=True)
    st.markdown("### 🪄 Step-by-Step Plan")
    for i, step in enumerate(plan):
        func = step.get('function', f"Step{i+1}")
        args = step.get('inputs', {})
        desc = next((t['description'] for t in relevant_tools if t['name'] == func), "")
        label, _ = get_tool_label(func, TOOL_LABELS)
        
        st.markdown(f"**Step {i+1}**")
        st.markdown(f"#### {label}")
        st.markdown(f"<code style='font-size:1.1em;'>{func}</code>", unsafe_allow_html=True)
        if desc:
            st.markdown(f"<span style='color:#bdbdbd;'>What it does:</span> <b>{desc}</b>", unsafe_allow_html=True)
        
        if args:
            shown_any = False
            input_lines = []
            for k, v in args.items():
                if v is not None and v != '' and v != '?':
                    input_lines.append(f"<li><b>{k}</b>: {repr(v)}</li>")
                    shown_any = True
                elif v == '?':
                    input_lines.append(f"<li><b>{k}</b>: {get_input_placeholder(k)}</li>")
                    shown_any = True
            if shown_any:
                st.markdown(f"<span style='color:#bdbdbd;'>Inputs:</span>", unsafe_allow_html=True)
                st.markdown('<ul style="margin-top:0;margin-bottom:0.5em;">' + ''.join(input_lines) + '</ul>', unsafe_allow_html=True)
        st.markdown("<hr style='border:0;border-top:1px solid #333;margin:0.7em 0 1.1em 0;'/>", unsafe_allow_html=True) 