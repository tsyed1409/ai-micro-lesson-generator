import streamlit as st
import openai
import time

# Set up OpenAI client (passing key from Streamlit Secrets)
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

# --- Streamlit App Layout ---

st.set_page_config(page_title="AI Micro-Lesson Generator", page_icon="🎓")
st.title("🎓 AI Micro-Lesson Generator")
st.write("Enter a topic and choose the difficulty level!")

# --- Clear topic if reset was triggered previously ---
if "reset_triggered" in st.session_state and st.session_state.reset_triggered:
    st.session_state.topic_input = ""
    st.session_state.reset_triggered = False

# --- Input fields ---
topic = st.text_input("Enter a topic:", key="topic_input")
difficulty = st.selectbox("Select difficulty level:", ["Easy", "Medium", "Hard"])

# --- Buttons ---
col1, col2 = st.columns(2)
with col1:
    generate = st.button("Generate Lesson")
with col2:
    reset = st.button("Reset")

# --- Generate lesson logic ---
def generate_micro_lesson(topic, difficulty):
    prompt = f"""
    You are an expert tutor.

    Given the topic "{topic}", create a micro-lesson appropriate for a **{difficulty}** level learner:

    - For EASY: Use simple words, short sentences, and basic explanations.
    - For MEDIUM: Use moderate technical terms, slightly deeper explanations.
    - For HARD: Use advanced terminology, detailed concepts, and assume prior knowledge.

    Generate:
    - 5 detailed bullet points explaining the concept.
    - 2 practice questions with detailed model answers.

    Make sure the lesson matches the {difficulty} level requirements exactly.
    """

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=700
    )

    return response.choices[0].message.content

# --- Handle Generate ---
if generate:
    if st.session_state.topic_input:
        with st.spinner("Generating your lesson..."):
            lesson = generate_micro_lesson(st.session_state.topic_input, difficulty)
            st.success("Here’s your AI-generated lesson!")
            st.markdown(lesson)
    else:
        st.warning("Please enter a topic first.")

# --- Handle Reset ---
if reset:
    st.session_state.reset_triggered = True
    st.rerun()
