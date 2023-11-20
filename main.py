from flask import Flask, render_template, request
import json
from typing import List, Optional, Dict
from difflib import get_close_matches

app = Flask(__name__)

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Save the updated knowledge base to the JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the closest matching question
def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: Dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

knowledge_base = load_knowledge_base('knowledge_base.json')

@app.route('/')
def index():
    return render_template('indexpopup.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    best_match = find_best_match(user_message, [q["question"] for q in knowledge_base["questions"]])
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        response = {"response": answer}
    else:
        response = {"response": "I don't know the answer. Can you teach me?"}
    return json.dumps(response)

if __name__ == "__main__":
    app.run()
