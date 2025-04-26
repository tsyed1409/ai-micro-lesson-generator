import streamlit as st
import openai
import time

# Set your OpenAI API key here
openai.api_key = st.secrets["openai_api_key"]  # <-- replace with your real API key

# Function to generate the micro-lesson
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
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if you don't have GPT-4 access
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=700
    )
    return response['choices'][0]['message']['content']

# --- Streamlit App ---

st.set_page_config(page_title="AI Micro-Lesson Generator", page_icon="🎓")

st.title("🎓 AI Micro-Lesson Generator")
st.write("Enter a topic and choose the difficulty level!")

# Input fields
topic = st.text_input("Enter a topic:")
difficulty = st.selectbox("Select difficulty level:", ["Easy", "Medium", "Hard"])

# Layout with two columns for buttons
col1, col2 = st.columns(2)

# Generate button
with col1:
    if st.button("Generate Lesson"):
        if topic:
            with st.spinner("Generating your lesson..."):
                lesson = generate_micro_lesson(topic, difficulty)
                st.success("Here’s your AI-generated lesson!")
                st.markdown(lesson)
        else:
            st.warning("Please enter a topic first.")

# Reset button
with col2:
    if st.button("Reset"):
        st.success("Reset successful! Ready for a new topic.")
        time.sleep(1)
        st.rerun()
