import streamlit as st
import json
import google.generativeai as genai
from streamlit_ace import st_ace

st.set_page_config(page_title="AI Pair Engineer", page_icon="🤖", layout="wide")

def get_client():
    api_key = st.session_state.get("api_key") or st.secrets.get("GOOGLE_API_KEY", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3-flash-preview')

def analyze_code(code_snippet):
    model = get_client()
    if not model:
        return None
    
    prompt = f"""You are an expert Python code reviewer and pair programming partner.

Analyze this code and provide:
1. Design Issues: Find 2-3 design flaws (complexity, naming, structure, best practices)
2. Unit Tests: Generate 2-3 pytest test cases
3. Refactored Code: Provide an improved version

Return ONLY a JSON object with this structure:
{{
  "design_issues": [
    {{"issue": "brief description", "severity": "high/medium/low", "explanation": "why it matters", "line_reference": "which part"}}
  ],
  "unit_tests": "complete pytest code as string",
  "refactored_code": "improved code as string",
  "key_changes": ["change 1", "change 2"]
}}

Code to analyze:
```python
{code_snippet}
```

Return only valid JSON, no markdown formatting."""

    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Clean markdown
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(response_text)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

st.title("🤖 AI Pair Engineer")
st.markdown("*Your AI coding partner powered by Google Gemini (FREE!)*")

with st.sidebar:
    st.header("⚙️ Setup")
    st.info("🆓 Get FREE API key from Google AI Studio - No credit card needed!")
    st.markdown("[Get API Key →](https://aistudio.google.com/app/apikey)")
    
    api_key_input = st.text_input("Google API Key", type="password", help="From aistudio.google.com/app/apikey")
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.success("✅ API key saved!")
    
    st.markdown("---")
    st.header("📚 Sample Code")
    
    samples = {
        "Deep Nesting": """def process_user_data(user):
    if user.is_active:
        if user.has_permission:
            if user.email_verified:
                data = fetch_data(user.id)
                processed = transform(data)
                return save(processed)
    return None""",
        
        "Poor Naming": """def f(x, y):
    z = x + y
    return z * 2""",
        
        "Missing Error Handling": """def divide_numbers(a, b):
    return a / b""",
    }
    
    selected_sample = st.selectbox("Load example:", [""] + list(samples.keys()))
    if selected_sample and st.button("Load Sample"):
        st.session_state.code_input = samples[selected_sample]
        st.session_state.editor_version = st.session_state.get('editor_version', 0) + 1
        st.rerun()

st.markdown("### 💻 Code Editor")
code_input = st_ace(
    value=st.session_state.get("code_input", ""),
    language="python",
    theme="monokai",
    height=300,
    font_size=14,
    tab_size=4,
    show_gutter=True,
    show_print_margin=False,
    wrap=False,
    auto_update=True,
    readonly=False,
    key=f"ace_editor_{st.session_state.get('editor_version', 0)}"  # Dynamic key
)
analyze_btn = st.button("🔍 Analyze Code", type="primary", use_container_width=True)

if analyze_btn and code_input.strip():
    if not get_client():
        st.warning("⚠️ Please enter your Google API key in the sidebar first.")
    else:
        with st.spinner("🧠 AI is analyzing..."):
            result = analyze_code(code_input)
        
        if result:
            st.markdown("---")
            st.header("🔍 Design Issues Found")
            for i, issue in enumerate(result.get("design_issues", []), 1):
                severity_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                icon = severity_icons.get(issue.get("severity", "medium"), "🟡")
                
                with st.expander(f"{icon} Issue {i}: {issue.get('issue', 'N/A')}", expanded=True):
                    st.markdown(f"**Severity:** {issue.get('severity', 'N/A').title()}")
                    st.markdown(f"**Location:** `{issue.get('line_reference', 'N/A')}`")
                    st.markdown(f"**Why:** {issue.get('explanation', 'N/A')}")
            
            st.markdown("---")
            st.header("🧪 Generated Unit Tests")
            st.code(result.get("unit_tests", "# No tests"), language="python")
            
            st.markdown("---")
            st.header("✨ Refactored Code")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("❌ Before")
                st.code(code_input, language="python")
            with col2:
                st.subheader("✅ After")
                st.code(result.get("refactored_code", ""), language="python")
            
            if result.get("key_changes"):
                st.markdown("#### 🔑 Key Changes:")
                for change in result["key_changes"]:
                    st.markdown(f"- {change}")

elif analyze_btn:
    st.warning("⚠️ Please paste some code first!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Built with ❤️ using Streamlit + Google Gemini</div>", unsafe_allow_html=True)