from flask import Flask, request, jsonify
from flask_cors import CORS
from difflib import get_close_matches
import google.generativeai as genai
import json
import os

# === Configure Gemini API ===
genai.configure(api_key="AIzaSyBLqfjBdhqWYrhcRfa8cQWy_lAiCoKNPfw")  # Replace with your actual API key

def generate(input_prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(input_prompt)
    return response.text

# === Knowledge Base Functions ===
def load_knowledge_base(filepath: str) -> dict:
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"questions": []}

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question.lower(), [q.lower() for q in questions], n=1, cutoff=0.8)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base['questions']:
        if q['question'].lower() == question.lower():
            return q['answer']
    return None

# === Load knowledge base ===
knowledge_base_path = os.path.join('data', 'knowledge_base.json')
knowledge_base = load_knowledge_base(knowledge_base_path)

# === Flask App Setup ===
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to CodeMate Backend!"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'reply': 'No message provided.'})

    reply = generate_reply(user_message)
    return jsonify({'reply': reply})

def generate_reply(user_input):
    # Validate knowledge base
    if not isinstance(knowledge_base, dict) or 'questions' not in knowledge_base:
        return "Knowledge base error"

    questions = [q['question'] for q in knowledge_base['questions']]
    best_match = find_best_match(user_input, questions)

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return answer

    # If no match, use Gemini
    return generate(user_input)

if __name__ == '__main__':
    app.run(port=5000, debug=False)