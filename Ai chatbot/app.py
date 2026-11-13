from flask import Flask, render_template, request, jsonify
import openai
from faqs import faqs

app = Flask(__name__)

# Yahan apni OpenAI API key daalein
openai.api_key = "YOUR_OPENAI_API_KEY"

def build_prompt(user_question):
    prompt = "Yeh ek college/school helpdesk chatbot hai. Yeh kuch common questions aur unke answers hain:\n"
    for faq in faqs:
        prompt += f"Q: {faq['question']}\nA: {faq['answer']}\n"
    prompt += f"\nAb student ka question:\nQ: {user_question}\nA:"
    return prompt

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    prompt = build_prompt(user_question)
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.3,
            stop=["\nQ:"]
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        answer = "Sorry, kuch error aa gaya hai. Kripya baad mein try karein."
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True) 