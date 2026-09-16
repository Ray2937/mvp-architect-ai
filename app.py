import os
import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="MVP Architect & Tech Stack Advisor",
    page_icon="🚀",
    layout="wide"
)

# Custom styling for clean layout
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.markdown("### About the Agent")
    st.markdown("This AI acts as your **Senior Technical Product Manager**, breaking down raw app concepts into production-ready student MVPs.")
    st.markdown("---")
    # st.markdown("🎯 **Built for:** GDG MCET Organizer Challenge")
    
    st.markdown("### Quick Idea Prompts:")
    sample_1 = "A student-first expense tracker using Next.js 15, Tailwind, and LocalStorage with a longevity projection tool."
    sample_2 = "A peer-to-peer study group & hackathon teammate finder app for college students."
    sample_3 = "An AI code reviewer that flags security vulnerabilities and migrates old code snippets."
    if st.button("💡 Try Expense Tracker Idea"):
        st.session_state["idea_input"] = sample_1
    if st.button("💡 Try Teammate Finder Idea"):
        st.session_state["idea_input"] = sample_2
    if st.button("💡 Try Code Auditor Idea"):
        st.session_state["idea_input"] = sample_3
    st.markdown("---")
    st.markdown("⚙️ **Powered by:** Google Gemini 3.5 Flash")

    # Main Header Section
st.title("🚀 Idea-to-MVP Architecture & Tech Stack Advisor")
st.markdown("Transform your raw app ideas into a structured, production-ready engineering blueprint instantly.")
st.markdown("---")

if "idea_input" not in st.session_state:
    st.session_state["idea_input"] = ""

# User Input Form
with st.form("mvp_form"):
    st.markdown("#### Describe Your App Concept")
    user_idea = st.text_area(
        "Enter your App Idea:",
        value=st.session_state["idea_input"],
        placeholder="e.g., A student expense tracker web app built with Next.js, featuring local storage...",
        height=120
    )
    
    col1, col2 = st.columns(2)
    with col1:
        timeline = st.selectbox(
            "Target Timeline", 
            ["Weekend Hackathon (48 hours)", "1 Week MVP", "1 Month Project"]
        )
    with col2:
        experience_level = st.selectbox(
            "Your Experience Level", 
            ["Beginner", "Intermediate", "Advanced"]
        )
        
    st.markdown("")
    submit_button = st.form_submit_button("Generate MVP Blueprint 🛠️")

# Handle Generation Logic
if submit_button:
    if not user_idea.strip():
        st.warning("Please enter or select an app idea first!")
    else:
        with st.spinner("Analyzing idea, designing architecture, and mapping out roadmap..."):
            try:
                client = genai.Client()
                
                system_instruction = """
                You are a Senior Solutions Architect and Technical Product Manager mentoring student developers. 
                Your goal is to take a raw app idea and convert it into a practical, structured, and realistic MVP blueprint. 
                Prioritize lightweight, modern, and free-tier technologies (e.g., Next.js, Tailwind CSS, shadcn/ui, LocalStorage, Supabase) 
                suited for students working under tight deadlines.
                
                Structure your response using clear markdown headings:
                1. 💡 **Core Feature Breakdown** (Must-haves vs. Nice-to-haves)
                2. 🛠️ **Recommended Tech Stack** (Frontend, Backend/State, Styling, Deployment with rationale)
                3. 🗄️ **Data Schema / State Management** (Briefly how data flows or is structured)
                4. 📅 **Step-by-Step Execution Roadmap** (Milestones broken down by days)
                5. ⚠️ **Potential Bottlenecks & Pro-Tips** (What to watch out for)
                """
                
                prompt = f"""
                App Idea: {user_idea}
                Timeline: {timeline}
                Developer Experience: {experience_level}
                
                Generate a comprehensive MVP architecture plan based on these constraints.
                """
                
                # Auto-retry logic to seamlessly bypass 503 traffic spikes
                import time
                response = None
                max_retries = 3
                
                for attempt in range(max_retries):
                    try:
                        response = client.models.generate_content(
                            model='gemini-3.5-flash',
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.7,
                            ),
                        )
                        break # Success, exit retry loop
                    except Exception as api_err:
                        if "503" in str(api_err) and attempt < max_retries - 1:
                            time.sleep(1.5) # Wait a moment before retrying
                            continue
                        else:
                            raise api_err # Raise error if all retries fail
                
                st.markdown("---")
                # st.success("Blueprint Generated Successfully!")
                
                # Save blueprint and reset chat history for the new project in session state
                st.session_state["current_blueprint"] = response.text
                st.session_state["chat_history"] = []
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Initialize session state variables for follow-ups if they don't exist
if "current_blueprint" not in st.session_state:
    st.session_state["current_blueprint"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display Blueprint if it exists in session state
if st.session_state["current_blueprint"]:
    st.markdown("---")
    st.success("Blueprint Generated Successfully!")
    st.markdown(st.session_state["current_blueprint"])

    # Render Chat History Discussion First (so past Q&As stay visible)
    if st.session_state["chat_history"]:
        st.markdown("---")
        st.markdown("#### 🗣️ Q&A Discussion History")
        for chat in st.session_state["chat_history"]:
            st.markdown(f"**👤 You:** {chat['question']}")
            st.markdown(f"**🤖 Architect Agent:**\n{chat['answer']}")
            st.markdown("---")

    # --- INTERACTIVE DEEP DIVE / FOLLOW-UP ASSISTANT FORM ---
    st.markdown("### 💬 Deep Dive & Follow-Up Assistant")
    st.markdown("Have a doubt about this blueprint, need a specific code snippet, or want to modify a feature? Ask your AI Architect below:")

    with st.form("follow_up_form"):
        user_question = st.text_input(
            "Ask a follow-up question about this blueprint:", 
            placeholder="e.g., Can you write out the exact React code for the LocalStorage hook?"
        )
        ask_button = st.form_submit_button("Ask Agent 🤖")

    if ask_button and user_question.strip():
        with st.spinner("Thinking through your question..."):
            try:
                client = genai.Client()

                # Build context incorporating previous conversation history if available
                history_text = "\n".join([f"Q: {c['question']}\nA: {c['answer']}" for c in st.session_state["chat_history"]])

                chat_context = f"""
                You are a Senior Solutions Architect. You previously generated this MVP blueprint for the user:
                {st.session_state["current_blueprint"]}

                Previous Q&A discussion context:
                {history_text}

                The user now has a new follow-up question or doubt:
                "{user_question}"

                Provide a clear, detailed, and helpful technical answer maintaining context. If they asked for code, provide clean, copy-pasteable code blocks.
                """

                # Auto-retry loop for follow-up 503 spikes
                import time
                answer_response = None
                max_retries = 3

                for attempt in range(max_retries):
                    try:
                        answer_response = client.models.generate_content(
                            model='gemini-3.5-flash',
                            contents=chat_context,
                        )
                        break
                    except Exception as api_err:
                        if "503" in str(api_err) and attempt < max_retries - 1:
                            time.sleep(1.5)
                            continue
                        else:
                            raise api_err

                # Append new question and answer to chat history
                st.session_state["chat_history"].append({
                    "question": user_question, 
                    "answer": answer_response.text
                })
                st.rerun() # Refresh app to immediately display the new Q&A

            except Exception as e:
                st.error(f"Error answering follow-up: {e}")