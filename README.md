<!-- # 🚀 MVP Architect & Roadmap Agent
Built for the GDG MCET Organizer Selection Challenge.

## 💡 About the Project
An AI-powered technical product manager that converts raw app ideas into structured engineering blueprints, tech stack recommendations, and execution roadmaps tailored for student constraints.

## 🛠️ Tech Stack
- **Frontend / UI:** Streamlit
- **AI Backend:** Google GenAI SDK (Gemini 2.5 Flash)
- **Language:** Python

## ⚙️ How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install streamlit google-genai`
3. Set your API key: `export GEMINI_API_KEY="your_key"`
4. Run the app: `streamlit run app.py` -->

# 🚀 Idea-to-MVP Architecture & Tech Stack Advisor

An AI-powered technical product management tool built for student developers to instantly transform raw app ideas into structured, production-ready engineering blueprints. Built with **Python, Streamlit, and Google Gemini 3.5 Flash**.

## 💡 What it Solves
Students often have great app ideas for hackathons or portfolio projects but struggle with:
* Choosing the right lightweight tech stack (e.g., Next.js vs. Vanilla, LocalStorage vs. Supabase).
* Breaking down core features versus nice-to-haves.
* Structuring a realistic execution timeline under tight deadlines.

## ✨ Key Features
* **Automated Architecture Blueprints:** Generates tech stack rationales, data schemas, and day-by-day roadmaps.
* **Interactive Deep Dive & Follow-Up Assistant:** A sequential chat history contextually answers follow-up doubts or writes specific code snippets on demand.
* **Smart UI & Error Handling:** Built-in auto-retry logic for API traffic spikes and custom clean styling.

## 🛠️ Tech Stack
* **Frontend/UI:** Streamlit
* **Intelligence:** Google Gemini 3.5 Flash API (`google-genai` SDK)
* **Language:** Python 3.10+

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Ray2937/mvp-architect-ai.git](https://github.com/Ray2937/mvp-architect-ai.git)
   cd mvp-architect-ai
2. Install dependencies: `pip install streamlit google-genai`
3. Set your API key: `export GEMINI_API_KEY="your_key"`
4. Run the app: `streamlit run app.py`