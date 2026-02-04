# 🤖 AI Pair Engineer

An interactive AI coding assistant that detects design flaws, generates unit tests, and suggests refactors in real-time.

## 🚀 Quick Start

### Local Setup (3 minutes)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get your FREE Google API key (no credit card!):**
   - Go to https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

3. **Run the app:**
```bash
streamlit run app.py
```

4. **Paste API key in sidebar** and start analyzing code!

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "AI Pair Engineer"
git push origin main
```

2. **Deploy:**
   - Go to https://share.streamlit.io/
   - Connect your GitHub repo
   - Add `GOOGLE_API_KEY` in secrets (Settings → Secrets)
   - Format: `GOOGLE_API_KEY = "your-key-here"`

3. **Share the link!**

---

## ✨ Features

- **🔍 Design Flaw Detection**: Identifies complexity, naming, and structural issues
- **🧪 Auto-Generated Tests**: Creates pytest test cases for your code
- **✨ Smart Refactoring**: Suggests improved code with explanations
- **📊 Side-by-Side Comparison**: See before/after changes clearly
- **💻 Real Code Editor**: VS Code-like editor with syntax highlighting
- **📚 Quick Load Samples**: Pre-loaded examples to try instantly
- **🆓 100% Free**: No credit card, no hidden costs

---

## 🎯 Usage Example

**Input:**
```python
def f(x, y):
    z = x + y
    return z * 2
```

**AI Output:**
- **Issue**: Poor function and variable naming (Medium severity)
- **Tests**: Generated pytest with edge cases  
- **Refactor**: `calculate_sum_doubled(num1: int, num2: int) -> int` with proper docstring

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Code Editor**: Streamlit-Ace (Monaco-like experience)
- **AI**: Google Gemini 2.0 Flash (FREE API)
- **Language**: Python 3.9+
- **Cost**: $0 (completely free tier)

---

## 📝 Project Context

Built as a 60-minute prototype demonstrating:
- Real-time AI-assisted code review
- Interactive pair programming workflows
- Practical AI integration in developer tools

**Differentiator**: Unlike passive linters, this tool acts as an educational pair programming partner—explaining *why* issues matter and proposing concrete solutions.

---

## 🎓 100-Word Summary

AI Pair Engineer is an interactive coding assistant that detects design flaws, generates unit tests, and suggests refactors in real-time. Built with Streamlit and Google Gemini API (free tier), it analyzes Python code for common issues like deep nesting, poor naming, and missing error handling. Features a VS Code-like editor with syntax highlighting and line numbers. The tool provides actionable feedback with before/after comparisons, helping developers write cleaner, more maintainable code. Unlike passive code reviewers, it acts as a pair programming partner—explaining why issues matter and proposing concrete solutions. Developed in 60 minutes using completely free tools, demonstrating practical AI-assisted workflows.

---

## 📦 File Structure

```
.
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── AI_PAIR_ENGINEER_SPEC.md   # Project specification
└── README.md                  # This file
```

---

## 🔮 Future Enhancements

- [ ] Multi-language support (JS, Java, Go)
- [ ] Conversation mode for follow-up questions
- [ ] Export results as markdown reports
- [ ] Integration with GitHub for PR reviews
- [ ] Custom rule configuration

---

## 📄 License

MIT License - feel free to use and modify!

---

## 🤝 Contributing

This is a prototype, but suggestions welcome! Open an issue or PR.

---

**Made with ❤️ in 60 minutes**