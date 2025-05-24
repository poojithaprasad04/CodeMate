from flask import Flask, request, jsonify
from flask_cors import CORS
from difflib import get_close_matches
from huggingface_hub import InferenceClient
import json
import os

def load_knowledge_base(filepath: str) -> dict:
    """Load knowledge base from a JSON file."""
    try:
        with open(filepath, 'r') as file:
            data: dict = json.load(file)
        return data
    except FileNotFoundError:
        return {"questions": []}

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """Find the best match for a user question from a list of questions."""
    if not questions:
        print("No questions available.")
        return None
    matches: list = get_close_matches(user_question.lower(), [q.lower() for q in questions], n=1, cutoff=0.8)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """Get the answer for a given question from the knowledge base."""
    for q in knowledge_base['questions']:
        if q['question'].lower() == question.lower():
            return q['answer']
    return None

# Load knowledge base
knowledge_base_path = os.path.join('data', 'knowledge_base.json')
knowledge_base = load_knowledge_base(knowledge_base_path)

client = InferenceClient(
    "microsoft/Phi-3-mini-4k-instruct",
    token="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",
)

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
    # Check if the knowledge base is loaded and valid
    if not isinstance(knowledge_base, dict) or 'questions' not in knowledge_base:
        return "Knowledge base error"

    # Extract questions from the knowledge base
    questions = [q['question'] for q in knowledge_base['questions']]

    # Find the best match for the user input
    best_match = find_best_match(user_input, questions)
    
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return answer

    # If no good match, use the AI model to generate a response
    output = ""
    for message in client.chat_completion(
        messages=[{"role": "user", "content": user_input}],
        max_tokens=2000,
        stream=True,
    ):
        output += message.choices[0].delta.content
    
    return output

if __name__ == '__main__':
    app.run(port=5000, debug=False)
