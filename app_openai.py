import streamlit as st
import json
from openai import OpenAI

st.set_page_config(page_title="AI Pair Engineer", page_icon="🤖", layout="wide")

def get_client():
    api_key = st.session_state.get("api_key") or st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def analyze_code(code_snippet):
    client = get_client()
    if not client:
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
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cheaper model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        response_text = response.choices[0].message.content
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
st.markdown("*Your AI coding partner that detects flaws, generates tests, and suggests refactors*")

with st.sidebar:
    st.header("⚙️ Setup")
    api_key_input = st.text_input("OpenAI API Key", type="password", help="Get free $5 credits from platform.openai.com")
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

code_input = st.text_area(
    "📝 Paste your Python code here:",
    value=st.session_state.get("code_input", ""),
    height=200,
    placeholder="def my_function():\n    pass"
)

analyze_btn = st.button("🔍 Analyze Code", type="primary", use_container_width=True)

if analyze_btn and code_input.strip():
    if not get_client():
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar first.")
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