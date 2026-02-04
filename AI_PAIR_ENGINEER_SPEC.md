# AI Pair Engineer - Project Specification

## 📋 Overview
An interactive AI coding assistant that works alongside developers to detect design flaws, propose tests, and suggest refactors in real-time.

---

## 🎯 Core Objectives
Build a **60-minute MVP** that demonstrates:
1. Design flaw detection
2. Auto-generated unit tests
3. Refactoring suggestions with before/after comparison

---

## ⚙️ Technical Constraints

### Time Budget
- **Total**: 60 minutes
- Setup: 10 min
- Core features: 35 min
- Testing & polish: 15 min

### Tools (All Free)
- **Platform**: Streamlit
- **AI**: Google Gemini API (gemini-2.0-flash-exp) - FREE tier, no credit card required
- **Language**: Python
- **Code Editor**: Streamlit-Ace for VS Code-like experience
- **No external databases** - keep it stateless

### Data Requirements
- Use **self-created sample code** (Python functions)
- 5-7 example functions covering common issues:
  - Long functions
  - Missing error handling
  - Poor naming
  - No type hints
  - Nested conditionals

---

## 🛠️ Features (Prioritized)

### Must-Have (MVP)
1. **Code Input**: Text area for pasting Python code
2. **Design Flaw Detection**: 
   - Identify 2-3 issues (complexity, naming, structure)
   - Explain *why* it's a problem
3. **Unit Test Generation**:
   - Generate 2-3 test cases
   - Use pytest format
4. **Refactor Suggestion**:
   - Show improved version
   - Highlight key changes

### Nice-to-Have (If time permits)
- Side-by-side diff view
- Copy buttons for generated code
- Conversation mode (ask AI follow-up questions)
- Multiple language support

### Out of Scope
- Live code execution
- Multi-file analysis
- Integration with IDEs
- Persistent storage

---

## 🎨 User Interface

### Layout (Simple Streamlit)
```
[Header: AI Pair Engineer]

[Text Area: Paste your Python code here]
[Button: Analyze Code]

--- Results ---

[Section 1: Design Issues Found]
- Issue 1: [description + why it matters]
- Issue 2: ...

[Section 2: Generated Tests]
[Code block with pytest tests]

[Section 3: Refactored Code]
[Before/After comparison]

[Optional: Ask a follow-up question]
```

---

## 🧠 AI Prompt Strategy

### System Prompt Structure
```
Role: Expert Python developer and code reviewer
Task: Analyze code for design flaws, generate tests, suggest refactors
Output format: Structured JSON with:
  - design_issues: [{issue, severity, explanation, line_reference}]
  - unit_tests: {test_code}
  - refactored_code: {code, key_changes}
```

### Key Prompt Components
1. **Context**: "You are pair programming with a developer"
2. **Constraints**: "Focus on practical, actionable feedback"
3. **Tone**: "Helpful and educational, not critical"
4. **Format**: "Return ONLY valid JSON, no markdown formatting"

### Gemini API Setup
- Model: `gemini-2.0-flash-exp` (fast, free, accurate)
- Free tier: 60 requests/minute (more than enough!)
- No credit card required
- Get key from: https://aistudio.google.com/app/apikey

---

## 📊 Sample Test Cases

### Test Case 1: Long Function
```python
def process_user_data(user):
    if user.is_active:
        if user.has_permission:
            if user.email_verified:
                data = fetch_data(user.id)
                processed = transform(data)
                validated = validate(processed)
                return save(validated)
    return None
```
**Expected AI Output**:
- Design flaw: Deep nesting, violates single responsibility
- Tests: Edge cases for each condition
- Refactor: Early returns, extract functions

### Test Case 2: Poor Naming
```python
def f(x, y):
    z = x + y
    return z * 2
```

### Test Case 3: Missing Error Handling
```python
def divide_numbers(a, b):
    return a / b
```

### Test Case 4: No Type Hints
```python
def calculate_discount(price, discount_percent):
    return price - (price * discount_percent / 100)
```

### Test Case 5: Complex Conditionals
```python
def check_eligibility(age, income, credit_score, employed):
    if age >= 18 and age <= 65 and income > 30000 and credit_score > 650 and employed == True:
        return True
    return False
```

---

## 🚀 Implementation Plan

### Phase 1: Setup (10 min)
- [ ] Create Streamlit app skeleton
- [ ] Set up Claude API connection
- [ ] Test basic prompt/response

### Phase 2: Core Features (35 min)
- [ ] Build design flaw detector (12 min)
- [ ] Build test generator (12 min)
- [ ] Build refactor suggester (11 min)

### Phase 3: Polish (15 min)
- [ ] Add styling and formatting
- [ ] Test with all 5 sample cases
- [ ] Create screenshots
- [ ] Write 100-word summary

---

## 📤 Deliverables

### 1. Public Link
- Streamlit Cloud deployment OR
- Google Colab shareable link

### 2. Documentation
- This specification document
- README with usage instructions
- Sample inputs/outputs

### 3. 100-Word Summary
```
AI Pair Engineer is an interactive coding assistant that detects 
design flaws, generates unit tests, and suggests refactors in 
real-time. Built with Streamlit and Google Gemini API (free tier), 
it analyzes Python code for common issues like deep nesting, poor 
naming, and missing error handling. Features a VS Code-like editor 
with syntax highlighting and line numbers. The tool provides 
actionable feedback with before/after comparisons, helping developers 
write cleaner, more maintainable code. Unlike passive code reviewers, 
it acts as a pair programming partner—explaining why issues matter 
and proposing concrete solutions. Developed in 60 minutes using 
completely free tools, demonstrating practical AI-assisted workflows.
```

### 4. Screenshots
- Main interface with sample code
- Analysis results showing all 3 features
- Before/after refactor comparison

---

## 🎓 Success Criteria

### Minimum Viable Demo
✅ Analyzes code and returns structured feedback  
✅ Generates at least 2 valid unit tests  
✅ Produces improved code version  
✅ Works on 5 different test cases  
✅ Deployed and publicly accessible  

### Bonus Points
⭐ Interactive conversation mode  
⭐ Visual diff highlighting  
⭐ Multiple programming languages  
⭐ Export results as markdown  

---

## 🔧 Fallback Plan

If running short on time:
1. **Remove**: Refactor suggestions (hardest)
2. **Keep**: Design flaws + tests (most impressive)
3. **Simplify**: Use pre-formatted output instead of parsing

If API issues:
1. Switch to OpenAI GPT-3.5
2. Or use pre-cached responses for demo

---

## 📝 Notes

- Keep prompt engineering simple—don't over-optimize
- Focus on **demo quality** over feature completeness
- Test with diverse code samples to show versatility
- Make UI clean and professional (first impressions matter)

**Key Differentiator**: This is interactive and educational, not just a linter.