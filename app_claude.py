import streamlit as st
import json

# Page config
st.set_page_config(page_title="AI Pair Engineer", page_icon="🤖", layout="wide")

# Initialize Anthropic client
def get_client():
    try:
        import anthropic
        api_key = st.session_state.get("api_key") or st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return None
        return anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing client: {e}")
        return None

def analyze_code(code_snippet):
    """Send code to Claude for analysis"""
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
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        # Clean potential markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(response_text)
    except Exception as e:
        st.error(f"Error analyzing code: {str(e)}")
        return None

# UI Header
st.title("🤖 AI Pair Engineer")
st.markdown("*Your AI coding partner that detects flaws, generates tests, and suggests refactors*")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Setup")
    api_key_input = st.text_input("Anthropic API Key", type="password", help="Get your key from console.anthropic.com")
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
        
        "No Type Hints": """def calculate_discount(price, discount_percent):
    return price - (price * discount_percent / 100)""",
        
        "Complex Conditionals": """def check_eligibility(age, income, credit_score, employed):
    if age >= 18 and age <= 65 and income > 30000 and credit_score > 650 and employed == True:
        return True
    return False"""
    }
    
    selected_sample = st.selectbox("Load example:", [""] + list(samples.keys()))
    if selected_sample and st.button("Load Sample"):
        st.session_state.code_input = samples[selected_sample]

# Main input area
code_input = st.text_area(
    "📝 Paste your Python code here:",
    value=st.session_state.get("code_input", ""),
    height=200,
    placeholder="def my_function():\n    # Your code here\n    pass"
)

analyze_btn = st.button("🔍 Analyze Code", type="primary", use_container_width=True)

# Analysis section
if analyze_btn and code_input.strip():
    if not get_client():
        st.warning("⚠️ Please enter your Anthropic API key in the sidebar first.")
    else:
        with st.spinner("🧠 AI is analyzing your code..."):
            result = analyze_code(code_input)
        
        if result:
            # Design Issues
            st.markdown("---")
            st.header("🔍 Design Issues Found")
            for i, issue in enumerate(result.get("design_issues", []), 1):
                severity_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                severity_icon = severity_color.get(issue.get("severity", "medium"), "🟡")
                
                with st.expander(f"{severity_icon} Issue {i}: {issue.get('issue', 'N/A')}", expanded=True):
                    st.markdown(f"**Severity:** {issue.get('severity', 'N/A').title()}")
                    st.markdown(f"**Location:** `{issue.get('line_reference', 'N/A')}`")
                    st.markdown(f"**Why it matters:** {issue.get('explanation', 'N/A')}")
            
            # Unit Tests
            st.markdown("---")
            st.header("🧪 Generated Unit Tests")
            st.code(result.get("unit_tests", "# No tests generated"), language="python")
            
            # Refactored Code
            st.markdown("---")
            st.header("✨ Refactored Code")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("❌ Before")
                st.code(code_input, language="python")
            
            with col2:
                st.subheader("✅ After")
                st.code(result.get("refactored_code", "# No refactoring suggested"), language="python")
            
            # Key Changes
            if result.get("key_changes"):
                st.markdown("#### 🔑 Key Changes:")
                for change in result["key_changes"]:
                    st.markdown(f"- {change}")

elif analyze_btn:
    st.warning("⚠️ Please paste some code first!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Built with ❤️ using Streamlit + Claude AI</p>
        <p style='font-size: 12px;'>Tip: Try the sample codes from the sidebar!</p>
    </div>
    """,
    unsafe_allow_html=True
)