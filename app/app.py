import openai
import requests
from flask import Flask, render_template, request, jsonify, Response, stream_with_context

app = Flask(__name__)

# Configure the OpenAI client to use the llamafile API
openai.api_base = "http://localhost:8080/v1"  # llamafile server's address
openai.api_key = "sk-no-key-required"
LLAMAFILE_URL = "http://127.0.0.1:8080/"  # Update to match your API endpoint

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    # Get the conversation history from the request
    conversation = request.json.get('conversation', [])

    # Get a response from the llamafile API
    bot_response = get_llamafile_response(conversation)

    # Return the response as JSON
    return jsonify({'response': bot_response})

def get_llamafile_response(conversation):
    try:
        # Send the entire conversation to the llamafile API
        completion = openai.ChatCompletion.create(
            model="LLaMA_CPP",
            messages=[
                {"role": "system",
                 "content": "You are a travel assistant chatbot. Help users with their travel-related queries. Provide useful website links if possible to help users plan their trips."},
                *conversation
            ]
        )

        # Return the generated response
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't process your request at the moment."

@app.route('/api/v1/chat', methods=['POST'])
def chat_api_v1():
    # Get the conversation history from the request
    conversation = request.json.get('conversation', [])

    prompt = generate_prompt(conversation)

    # Prepare the payload for the llamafile API
    payload = {
        "prompt": f"You are a travel assistant chatbot. Help users with their travel-related queries. "
                  f"You are in a conversation with a user"
                  f"\n\n{generate_prompt(conversation)}\n\nBot:",
        "stream": True,  # Enable streaming
        "n_predict": 400,
        "temperature": 0.7,
        "stop": ["</s>", "Bot:", "User:"],
    }

    # Send request to llamafile and stream response back to client
    return Response(stream_with_context(stream_llamafile_response(payload)), content_type='text/event-stream')

def generate_prompt(conversation):
    # Generate a prompt from the conversation history
    return "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation)

def stream_llamafile_response(payload):
    with requests.post(LLAMAFILE_URL, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                yield f"{line.decode('utf-8')}\n\n"

if __name__ == '__main__':
    app.run(debug=True)
