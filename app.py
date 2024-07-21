import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! Welcome to the Travel Assistant Chatbot.'

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # Send user input to the llamafile service
    try:
        response = requests.post(
            'http://llamafile_service:8080', 
            json={'input': user_input}
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

    model_response = response.json()

    # Return the model's response
    return jsonify({'response': model_response.get('output')})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
