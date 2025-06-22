import streamlit as st
import graphviz

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

    # New Graphviz visualization
    st.markdown("### 📊 Workflow Graph")
    render_plan_as_graph(plan, TOOL_LABELS)

    st.markdown("### 🪄 Step-by-Step Plan")
    for i, step in enumerate(plan):
        func = step.get('function', f"Step{i+1}")
        args = step.get('inputs', {})
        tool_details = next((t for t in relevant_tools if t['name'] == func), None)
        desc = tool_details.get('description', "No description available.") if tool_details else "Tool details not found."
        category = tool_details.get('category', 'N/A') if tool_details else 'N/A'
        version = tool_details.get('version', 'N/A') if tool_details else 'N/A'
        author = tool_details.get('author', 'N/A') if tool_details else 'N/A'
        tags = tool_details.get('tags', []) if tool_details else []

        label, _ = get_tool_label(func, TOOL_LABELS)
        
        st.markdown(f"**Step {i+1}**")
        st.markdown(f"#### {label}")
        st.markdown(f"<code style='font-size:1.1em;'>{func}</code>", unsafe_allow_html=True)
        
        # Display new tool information
        st.markdown(f"""
        <small>
            <span style='color:#888;'>Category:</span> <b style='color:#555;'>{category}</b> |
            <span style='color:#888;'>Version:</span> <b style='color:#555;'>{version}</b> |
            <span style='color:#888;'>Author:</span> <b style='color:#555;'>{author}</b>
        </small>
        """, unsafe_allow_html=True)
        if tags:
            st.markdown(f"<small><span style='color:#888;'>Tags:</span> <i style='color:#555;'>{', '.join(tags)}</i></small>", unsafe_allow_html=True)

        st.markdown(f"<span style='color:#bdbdbd;'>What it does:</span> <b>{desc}</b>", unsafe_allow_html=True)

        # Display input parameters with their descriptions
        if args:
            input_lines = []
            if tool_details and isinstance(tool_details.get('input'), dict):
                for k, v in args.items():
                    param_info = tool_details['input'].get(k, {})
                    param_desc = param_info.get('description', 'No specific description.')
                    param_type = param_info.get('type', 'unknown')
                    val_display = repr(v) if v is not None and v != '' and v != '?' else get_input_placeholder(k)
                    input_lines.append(f"<li><b>{k}</b> (<i>{param_type}</i>): {val_display} <br><small style='color:#777;'>&nbsp;&nbsp;&nbsp;└ {param_desc}</small></li>")
            else: # Fallback if tool_details or its input schema is not found/malformed
                for k, v in args.items():
                    val_display = repr(v) if v is not None and v != '' and v != '?' else get_input_placeholder(k)
                    input_lines.append(f"<li><b>{k}</b>: {val_display}</li>")

            if input_lines:
                st.markdown(f"<span style='color:#bdbdbd;'>Inputs:</span>", unsafe_allow_html=True)
                st.markdown('<ul style="margin-top:0;margin-bottom:0.5em;">' + ''.join(input_lines) + '</ul>', unsafe_allow_html=True)

        # Display output parameters with their descriptions
        if tool_details and isinstance(tool_details.get('output'), dict) and tool_details['output']:
            output_lines = []
            st.markdown(f"<span style='color:#bdbdbd;'>Expected Outputs:</span>", unsafe_allow_html=True)
            for out_param_name, out_param_details in tool_details['output'].items():
                out_param_type = out_param_details.get('type', 'unknown')
                out_param_desc = out_param_details.get('description', 'No specific description.')
                output_lines.append(f"<li><b>{out_param_name}</b> (<i>{out_param_type}</i>): <small style='color:#777;'>{out_param_desc}</small></li>")
            if output_lines:
                st.markdown('<ul style="margin-top:0;margin-bottom:0.5em;">' + ''.join(output_lines) + '</ul>', unsafe_allow_html=True)

        st.markdown("<hr style='border:0;border-top:1px solid #333;margin:0.7em 0 1.1em 0;'/>", unsafe_allow_html=True)

        # User Feedback Section for each tool
        with st.expander(f"📝 Provide Feedback for {func_name}"):
            feedback_rating_key = f"rating_{active_chat['id']}_{i}_{func_name}"
            feedback_comment_key = f"comment_{active_chat['id']}_{i}_{func_name}"
            feedback_button_key = f"submit_feedback_{active_chat['id']}_{i}_{func_name}"

            rating = st.radio(
                "Rate this tool:",
                options=[1, 2, 3, 4, 5],
                index=4,  # Default to 5 stars
                key=feedback_rating_key,
                horizontal=True
            )
            comment = st.text_area("Your comments (optional):", key=feedback_comment_key, height=100)

            if st.button("Submit Feedback", key=feedback_button_key):
                if func_name not in st.session_state['tool_feedback']:
                    st.session_state['tool_feedback'][func_name] = []

                feedback_entry = {"rating": rating, "comment": comment, "plan_id": active_chat['id'], "step_index": i}
                st.session_state['tool_feedback'][func_name].append(feedback_entry)
                st.success(f"Thanks for your feedback on {func_name}!")
                # Consider clearing the input fields after submission if desired, by resetting their keys or rerunning.
                # For now, let's keep it simple.

def render_plan_as_graph(plan, TOOL_LABELS):
    """
    Renders the workflow plan as a Graphviz graph.
    """
    dot = graphviz.Digraph(comment='Workflow Plan', graph_attr={'rankdir': 'TB', 'splines':'ortho'})
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='#e8f0fe', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='9', color='#555555')

    # Start node
    dot.node('start', '🏁 Start', shape='ellipse', fillcolor='#a2d5ac')

    last_node_name = 'start'

    for i, step in enumerate(plan):
        func_name = step.get('function', f"UnknownStep{i+1}")
        tool_label, _ = get_tool_label(func_name, TOOL_LABELS)

        # Sanitize label for node name
        node_name = f"step_{i}_{func_name}"

        # Node label with function name and custom label
        node_label_html = f'''<
            <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
            <TR><TD><B>{tool_label}</B></TD></TR>
            <TR><TD><FONT POINT-SIZE="9" COLOR="#555555">{func_name}</FONT></TD></TR>
            </TABLE>
        >'''
        dot.node(node_name, label=node_label_html, shape='record', fillcolor='#e8f0fe')
        dot.edge(last_node_name, node_name)
        last_node_name = node_name

    # End node
    dot.node('output', '✅ Output', shape='ellipse', fillcolor='#a2d5ac')
    dot.edge(last_node_name, 'output')

    try:
        st.graphviz_chart(dot, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to render workflow graph: {e}")