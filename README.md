<p align="center">
  <strong>🚩 This project is an assignment for <a href="https://codemate.ai/" target="_blank">CodeMate.ai</a></strong>
  <br/>
  <span style="font-size:1.1em;">Learn more at <a href="https://codemate.ai/">codemate.ai</a></span>
  <img src="https://img.icons8.com/fluency/96/robot-2.png" width="90" alt="Toolmate Icon"/>
  <h1 align="center">🤖 Toolmate</h1>
  <p align="center">
    <b><i>The Ultimate AI Workflow Orchestrator</i></b><br/>
    <span style="font-size:1.1em;">Transform your ideas into actionable, automated workflows with the power of AI.</span>
  </p>
  <p align="center">
    <a href="#"><img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square&logo=python" alt="Python"></a>
    <a href="#"><img src="https://img.shields.io/badge/Streamlit-UI-orange.svg?style=flat-square&logo=streamlit" alt="Streamlit"></a>
    <a href="https://img.shields.io/badge/Google%20Gemini-886FBF?logo=googlegemini&logoColor=fff"><img src="https://img.shields.io/badge/Google%20Gemini-886FBF?logo=googlegemini&logoColor=fff" alt="Google Gemini"></a>
  </p>
</p>

---

> **Toolmate is your AI-powered partner for building, visualizing, and executing data workflows.**
> 
> _Describe your task in plain English. Toolmate plans, explains, and helps you automate it—no coding required._

---

## 🌟 Why Toolmate?

- **Stand out with automation:** Toolmate turns your ideas into step-by-step, executable plans using a curated library of smart tools.
- **No more manual busywork:** Let AI handle data extraction, transformation, summarization, and communication.
- **From concept to execution:** Visualize, edit, and (soon) run your workflows—all in one place.

---

## 🚀 How It Works

1. **Describe your workflow** in natural language (e.g., "Summarize this CSV and email it to my manager").
2. **AI analyzes your request** and selects the most relevant tools from its library.
3. **A large language model (Gemini)** generates a step-by-step plan using these tools.
4. **Review, edit, and version** the plan interactively in the UI, or use the CLI for quick access.
5. **Easily extend** Toolmate by adding new tools to a single JSON file—no code changes required!

---

## ✨ Features

- 🧠 **AI-Powered Planning:** Converts your requests into actionable, explainable workflows.
- 🛠️ **Extensible & Enhanced Tool Library:** 30+ built-in tools for data, text, files, communication, and more. Tools now include detailed metadata like category, version, author, tags, and comprehensive parameter descriptions for improved clarity and filtering.
- 🖥️ **Modern Streamlit UI (Toolmate Pro):** Plan, review, and update workflows visually with a refreshed, cleaner user interface.
- 📊 **Workflow Graph Visualization:** View generated plans as a clear, top-down graph for better understanding of the flow.
- 📈 **Tool Usage Statistics:** Track tool usage within your current session (displayed in the sidebar).
- ⭐ **User Feedback on Tools:** Provide ratings and comments for tools directly within the plan view to help improve tool relevance and quality.
- ⚡ **CLI Support:** For power users and scripting.
- 📝 **Interactive Plan Editing:** Tweak, version, and experiment with your workflow steps.
- 🔒 **Secure by Design:** API keys and secrets managed via environment files.
- 🧩 **Plugin-ready:** (Planned) Add your own tools and integrations.
- 🔍 **Semantic Tool Selection:** (Improved with richer tool data, further advancements coming soon) Smarter, context-aware tool matching.

---

## 🎬 Demo

<div align="center">
  <img src="https://user-images.githubusercontent.com/placeholder/demo.gif" alt="Toolmate Demo" width="700"/>
  <br/>
  <i>Describe your workflow, get an AI-generated plan, and review/edit steps interactively.</i>
</div>

---

## 🏗️ Architecture & Project Structure

```
mate/
  core/        # Core logic: prompt building, API calls, tool schema
  data/        # Tool definitions (JSON), sample prompts
  ui/          # Streamlit UI components
  main.py      # CLI entry point
  requirements.txt
  open.env     # API keys and environment variables
```

- **Prompt Builder:** Translates your query and available tools into a prompt for the LLM.
- **Tool Schema:** All tools are defined in a single JSON file for easy extensibility.
- **UI:** Built with Streamlit for a fast, interactive experience.
- **API Integration:** Connects to Gemini (and soon, more models) for planning.

---

## ⚙️ Installation

```bash
# 1. Clone the repository
$ git clone https://github.com/yourusername/toolmate.git
$ cd toolmate

# 2. Install dependencies
$ pip install -r requirements.txt

# 3. Set up environment variables
#    Copy open.env.example to open.env and add your API keys (e.g., GEMINI_API_KEY)
```

---

## 🏃 Usage

### 🌐 Streamlit Web App

```bash
streamlit run ui/ui_app.py
```

### 🖥️ Command-Line Interface

```bash
python main.py
```

---

## 🧩 Adding/Editing Tools

- Edit `data/function_tools.json` to add new function tools or update existing ones.
- Each tool definition is a JSON object with the following enhanced schema:
  - `name` (str): The unique name of the tool.
  - `category` (str): The category the tool belongs to (e.g., "File Operations", "Data Analysis").
  - `version` (str): The version of the tool (e.g., "1.0").
  - `author` (str): The author or maintainer of the tool.
  - `description` (str): A concise description of what the tool does.
  - `tags` (list[str]): A list of relevant tags for filtering and discovery.
  - `keywords` (list[str]): A list of keywords that describe the tool's functionality.
  - `input` (dict): An object where each key is an input parameter name.
    - Each parameter value is an object with:
      - `type` (str): The data type of the parameter (e.g., "str", "int", "list[dict]").
      - `description` (str): A detailed description of what this parameter represents and how to use it.
  - `output` (dict): An object describing the output parameters, similar in structure to `input`.
    - Each parameter value is an object with:
      - `type` (str): The data type of the output.
      - `description` (str): A detailed description of what this output represents.
  - `constraints` (str, optional): Any constraints or specific conditions for using the tool.
  - `meta` (dict, optional): An object for additional contextual information.
    - `usage_examples` (list[str], optional): Examples of how the tool might be used in a user query or plan.
    - `related_tools` (list[str], optional): Names of other tools that are commonly used with or are similar to this one.
- No code changes are required in the core logic for adding or modifying tools with this structure—just update the JSON!

---

## 📦 Dependencies

- `streamlit`, `openai`, `python-dotenv`, `scikit-learn`, `pillow`, `graphviz`, `requests`

---

## 🛠️ Coming Soon & Future Scope

> _Toolmate is just getting started. Here's what's on the horizon:_

- **Model Configuration:**
  - Switch between LLM providers (Gemini, OpenAI, etc.) and customize model parameters from the UI.
- **Sentence Transformers Integration:**
  - Smarter, context-aware tool selection and semantic search using advanced embeddings.
- **Workflow Execution Engine:**
  - Run generated plans end-to-end, with real-time status, error handling, and output visualization.
- **User Profiles & History:**
  - Save, revisit, and share your workflow plans across devices.
- **Plugin System:**
  - Add your own custom tools and integrations with a simple plugin interface.
- **Team Collaboration:**
  - Share, comment, and co-edit workflows with your team.
- **Marketplace for Tools:**
  - Discover and install community-contributed tools and workflow templates.
- **Mobile Companion App:**
  - Plan and review workflows on the go.

> _Stay tuned for these and more features designed to make Toolmate the ultimate AI workflow companion!_

---

## 🤝 Contributing

Pull requests and feature suggestions are welcome! Please open an issue to discuss your ideas.

---

## 🙏 Acknowledgements

- Powered by [Google Gemini](https://ai.google/discover/gemini/) and [Streamlit](https://streamlit.io/)
- Inspired by the need for accessible, AI-driven workflow automation for professionals and teams.

---

> _"Let AI handle the busywork, so you can focus on what matters."_ 