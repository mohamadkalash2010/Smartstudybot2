import streamlit as st
from dotenv import load_dotenv
import os
import requests
import random
from groq import Groq  # Import Groq client

# Hardcode the Groq API key
GROQ_API_KEY = "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"

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Load environment variables for Serper API
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "50610df183d1a757c93a80d9a63ccc2888082fcf")

# Function to fetch resources using Serper API
def get_resources(topic, resource_type="web"):
    url = "https://google.serper.dev/search"
    payload = {
        "q": f"{topic} {resource_type}"
    }
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get("organic", [])
        resources = []
        for result in results[:5]:  # Limit to top 5 results
            resources.append(f"[{result['title']}]({result['link']})")
        return resources
    else:
        return ["No resources found."]

# Function to generate quizzes
def generate_quiz(topic):
    questions = [
        f"What is the main concept of {topic}?",
        f"Can you explain {topic} in your own words?",
        f"What are the key points to remember about {topic}?",
        f"How does {topic} apply in real-world scenarios?"
    ]
    return random.sample(questions, 2)  # Return 2 random questions

# Function to generate flashcards
def generate_flashcards(topic):
    flashcards = [
        {"question": f"What is {topic}?", "answer": f"{topic} is a concept that..."},
        {"question": f"Why is {topic} important?", "answer": f"{topic} is important because..."},
        {"question": f"Can you give an example of {topic}?", "answer": f"An example of {topic} is..."}
    ]
    return flashcards

# Function to split topics and resources across days
def generate_study_plan(duration, topics):
    plan = []
    topics_per_day = max(1, len(topics) // duration)

    for day in range(1, duration + 1):
        start = (day - 1) * topics_per_day
        end = start + topics_per_day
        day_topics = topics[start:end]

        # Define a detailed description for each day
        if day == 1:
            description = "Focus on understanding the basics of the following topics."
        elif day == duration:
            description = "Review all the topics and ensure you're confident about them."
        else:
            description = "Practice and dive deeper into the following topics."

        plan.append({
            "day": day,
            "description": description,
            "topics": day_topics
        })

    return plan

# Function to interact with Groq API
def groq_chat(user_input):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful study assistant. Your goal is to help students understand their study topics clearly and concisely."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        model="llama3-70b-8192",  # Use the appropriate Groq model
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False
    )
    return chat_completion.choices[0].message.content

# Main application
st.title("Smart Study Bot")

# Introduction
st.write("Welcome! I'm here to help you create a personalized study plan.")

# Step 1: Ask for exam details
exam_name = st.text_input("What is the topic or subject of your exam?")
if exam_name:
    st.write(f"Great! Let's prepare for your {exam_name} exam.")

    # Step 2: Ask for duration
    duration = st.number_input("How many days do you have to study?", min_value=1, step=1)

    if duration:
        st.write(f"You have {duration} day(s) to prepare.")

        # Step 3: Ask for topics
        topics_input = st.text_area("List the topics you need to cover, separated by commas:")

        if topics_input:
            topics = [topic.strip() for topic in topics_input.split(',')]

            # Generate study plan
            study_plan = generate_study_plan(duration, topics)

            # Display the plan
            st.subheader("Your Study Plan")
            for day_plan in study_plan:
                st.write(f"### Day {day_plan['day']}: {day_plan['description']}")

                for topic in day_plan['topics']:
                    st.write(f"#### {topic}")

                    # Resource Videos
                    st.write("**Resource Videos:**")
                    video_resources = get_resources(topic, "video")
                    for resource in video_resources:
                        st.write(f"- {resource}")

                    # Quizzes
                    st.write("**Quiz:**")
                    quiz_questions = generate_quiz(topic)
                    for question in quiz_questions:
                        st.write(f"- {question}")

                    # Flashcards
                    st.write("**Flashcards:**")
                    flashcards = generate_flashcards(topic)
                    for card in flashcards:
                        st.write(f"**Q:** {card['question']}")
                        st.write(f"**A:** {card['answer']}")

            # Chatbot Section
            st.subheader("Chatbot Assistance")
            user_input = st.text_input("Ask me anything about your study topics:")
            if user_input:
                response = groq_chat(user_input)
                st.write(f"**Bot:** {response}")
