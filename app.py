import streamlit as st
import json
from datetime import datetime
import sys
import os

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {
        "q": "How does walking affect your physical condition during the day?",
        "opts": [
            ("It greatly improves my energy and physical condition", 0),
            ("It slightly improves my condition", 1),
            ("It has no noticeable effect", 2),
            ("It sometimes makes me feel tired", 3),
            ("It makes me feel more physically exhausted", 4)
        ]
    },
    {
        "q": "After finishing your daily tasks, how do you feel about going for a walk?",
        "opts": [
            ("I feel motivated and energized to walk", 0),
            ("I am willing to walk with little effort", 1),
            ("I feel neutral about it", 2),
            ("I feel somewhat tired but may still walk", 3),
            ("I feel too tired and avoid walking", 4)
        ]
    },
    {
        "q": "To what extent do you believe walking helps reduce your stress?",
        "opts": [
            ("It reduces my stress significantly", 0),
            ("It helps reduce stress", 1),
            ("It has a small effect", 2),
            ("It rarely helps", 3),
            ("It does not help at all", 4)
        ]
    },
    {
        "q": "When going for a walk, how do you usually choose your location?",
        "opts": [
            ("I always choose calm or pleasant walking areas", 0),
            ("I often prefer comfortable locations", 1),
            ("I sometimes consider the location", 2),
            ("I rarely think about where I walk", 3),
            ("I do not consider location at all", 4)
        ]
    },
    {
        "q": "What is your opinion about walking as a daily activity?",
        "opts": [
            ("It is very valuable and beneficial", 0),
            ("It is useful", 1),
            ("It is neutral to me", 2),
            ("It feels slightly unnecessary", 3),
            ("It feels like a waste of time", 4)
        ]
    },
    {
        "q": "How regularly do you go for walks intentionally?",
        "opts": [
            ("Daily", 0),
            ("Several times a week", 1),
            ("Occasionally", 2),
            ("Rarely", 3),
            ("Never", 4)
        ]
    },
    {
        "q": "After walking, how do you usually feel mentally?",
        "opts": [
            ("Very refreshed", 0),
            ("Refreshed", 1),
            ("Neutral", 2),
            ("Slightly tired", 3),
            ("Mentally drained", 4)
        ]
    },
    {
        "q": "How often do you reach your personal daily step goal?",
        "opts": [
            ("Always", 0),
            ("Often", 1),
            ("Sometimes", 2),
            ("Rarely", 3),
            ("Never", 4)
        ]
    },
    {
        "q": "How often do you consider participating in walking or fitness events (e.g., step challenges, marathon)?",
        "opts": [
            ("Very often", 0),
            ("Often", 1),
            ("Sometimes", 2),
            ("Rarely", 3),
            ("Never", 4)
        ]
    },
    {
        "q": "How strongly do you agree that regular physical activity (e.g., walking, running) improves overall health?",
        "opts": [
            ("Strongly agree", 0),
            ("Agree", 1),
            ("Neutral", 2),
            ("Disagree", 3),
            ("Strongly disagree", 4)
        ]
    },
    {
        "q": "How would you rate your overall mental well-being?",
        "opts": [
            ("Excellent", 0),
            ("Good", 1),
            ("Average", 2),
            ("Poor", 3),
            ("Very poor", 4)
        ]
    },
    {
        "q": "How frequently do you feel calm and relaxed?",
        "opts": [
            ("Always", 0),
            ("Often", 1),
            ("Sometimes", 2),
            ("Rarely", 3),
            ("Never", 4)
        ]
    },
    {
        "q": "How often do you experience difficulty concentrating?",
        "opts": [
            ("Never", 0),
            ("Rarely", 1),
            ("Sometimes", 2),
            ("Often", 3),
            ("Always", 4)
        ]
    },
    {
        "q": "How often do you track your daily step count or walking distance?",
        "opts": [
            ("Always", 0),
            ("Often", 1),
            ("Sometimes", 2),
            ("Rarely", 3),
            ("Never", 4)
        ]
    },
    {
        "q": "When attempting longer walking distances, how often do you experience physical discomfort or minor injuries?",
        "opts": [
            ("Never", 0),
            ("Rarely", 1),
            ("Sometimes", 2),
            ("Often", 3),
            ("Always", 4)
        ]
    }
]

interpret_score = {
    "Excellent vitality": (0, 12),
    "Good correlation": (13, 24),
    "Moderate vitality": (25, 36),
    "Low vitality": (37, 48),
    "Very low vitality": (49, 60)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Daily Step Count and Mental Vitality Survey")
st.title("📝 Daily Step Count and Mental Vitality Survey")

st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    # Validate inputs
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Save results to JSON
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
