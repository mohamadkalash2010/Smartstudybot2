import streamlit as st
from dotenv import load_dotenv
import os

# Function to generate the study plan
def generate_study_plan(duration, topics, resources):
    plan = []
    topics_per_day = len(topics) // duration
    extra_topics = len(topics) % duration

    topic_index = 0
    for day in range(1, duration + 1):
        num_topics = topics_per_day + (1 if day <= extra_topics else 0)
        day_topics = topics[topic_index:topic_index + num_topics]
        day_resources = {topic: resources.get(topic, {}) for topic in day_topics}

        plan.append({"day": day, "topics": day_topics, "resources": day_resources})
        topic_index += num_topics

    return plan


# Example function to fetch resources (simulate fetching data)
def get_resources():
    return {
        "Reproduction": {
            "Videos": [
                "Crash Course: 'Reproduction 101' (YouTube)",
                "Khan Academy: 'Reproduction Basics' (YouTube)"
            ],
            "Quizzes": [
                "Quizlet: 'Reproductive System Quiz'",
                "Kahoot: 'Reproduction Basics'"
            ],
            "Games": [
                "Interactive Biology Game: 'Reproduction Challenge'",
                "Matching Game: 'Reproductive Systems'"
            ]
        },
        "Photosynthesis": {
            "Videos": [
                "SciShow: 'Photosynthesis Explained' (YouTube)",
                "Crash Course: 'Photosynthesis Basics' (YouTube)"
            ],
            "Quizzes": [
                "Quizlet: 'Photosynthesis Quiz'",
                "Kahoot: 'Photosynthesis Fundamentals'"
            ],
            "Games": [
                "Puzzle Game: 'Photosynthesis Cycle'",
                "Interactive Game: 'Photosynthesis Fun'"
            ]
        },
        "Genetics": {
            "Videos": [
                "Khan Academy: 'Genetics Basics' (YouTube)",
                "Crash Course: 'Introduction to Genetics' (YouTube)"
            ],
            "Quizzes": [
                "Quizlet: 'Genetics Quiz'",
                "Kahoot: 'DNA and Genes Quiz'"
            ],
            "Games": [
                "DNA Matching Game",
                "Genetics Explorer Game"
            ]
        }
    }


# Main function for Streamlit app
def main():
    st.title("SmartStudyBot.ai")
    st.write("Organize, Plan, and Prepare Effectively for Your Exams!")

    # Input: Subject and exam preparation details
    st.header("Step 1: Input Your Study Details")
    purpose = st.text_input("What subject or topic are you preparing for?")
    duration = st.number_input("How many days do you have to prepare?", min_value=1, step=1)
    topics_input = st.text_area("List the topics you need to study (separate by commas):")

    if purpose and duration and topics_input:
        st.success(f"Preparing study plan for: {purpose}")

        # Parse the input topics
        topics = [topic.strip() for topic in topics_input.split(",") if topic.strip()]

        # Fetch resources
        all_resources = get_resources()

        # Generate the study plan
        study_plan = generate_study_plan(duration, topics, all_resources)

        # Display the study plan
        st.header("Your Study Plan")
        for day_plan in study_plan:
            day = day_plan["day"]
            day_topics = day_plan["topics"]
            day_resources = day_plan["resources"]

            st.subheader(f"Day {day}")
            st.write(f"Topics to Study: {', '.join(day_topics)}")

            for topic in day_topics:
                st.write(f"### Resources for {topic}")
                topic_resources = day_resources.get(topic, {})

                if "Videos" in topic_resources:
                    st.write("**Videos:**")
                    for video in topic_resources["Videos"]:
                        st.write(f"- {video}")

                if "Quizzes" in topic_resources:
                    st.write("**Quizzes:**")
                    for quiz in topic_resources["Quizzes"]:
                        st.write(f"- {quiz}")

                if "Games" in topic_resources:
                    st.write("**Games:**")
                    for game in topic_resources["Games"]:
                        st.write(f"- {game}")

    else:
        st.warning("Please complete all input fields to generate your study plan.")


if __name__ == "__main__":
    main()
