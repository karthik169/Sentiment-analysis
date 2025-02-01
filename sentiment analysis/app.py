from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import re

app = Flask(__name__)

# Function to clean text (optional)
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower()

# Function to analyze sentiment with TextBlob
def analyze_sentiment_textblob(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive 😊"
    elif polarity < 0:
        return "Negative 😞"
    else:
        return "Neutral 😐"

# Analyze WhatsApp chat file
def analyze_whatsapp_chat(file):
    chat_text = file.read().decode("utf-8")
    conversations = chat_text.split('\n')  # Split chat into individual messages
    results = []
    for message in conversations:
        if message.strip():  # Skip empty lines
            sentiment = analyze_sentiment_textblob(message)
            results.append({"message": message, "sentiment": sentiment})
    return results

# Analyze text input
def analyze_text_input(text):
    messages = text.split('\n')  # Treat each new line as a separate message
    results = []
    for message in messages:
        if message.strip():  # Skip empty lines
            sentiment = analyze_sentiment_textblob(message)
            results.append({"message": message, "sentiment": sentiment})
    return results

# Serve the HTML template on the root endpoint
@app.route('/')
def index():
    return render_template('index.html')  # This renders the index.html file

# API endpoint to analyze the text or file
@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text', '')  # Get the text input
    file = request.files.get('file')  # Get the uploaded file
    
    if file:
        sentiments = analyze_whatsapp_chat(file)  # Analyze uploaded file
    elif text:
        sentiments = analyze_text_input(text)  # Analyze text input
    else:
        sentiments = {"sentiments": []}  # If no input or file, return empty
    
    return jsonify({"sentiments": sentiments})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run Flask on port 5001
