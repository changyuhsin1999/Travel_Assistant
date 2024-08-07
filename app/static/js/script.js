let conversationHistory = [];

function sendMessage1() {
    const inputElement = document.getElementById('user-input');
    const message = inputElement.value.trim();

    if (message) {
        // Add user message to the chat history
        conversationHistory.push({role: 'user', content: message});
        displayMessage(message, 'user');
        inputElement.value = '';

        // Show loading indicator
        const loadingIndicator = document.getElementById('loading-indicator');
        loadingIndicator.style.display = 'block';

        // Send the conversation history to the backend
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({conversation: conversationHistory})
        })
            .then(response => response.json())
            .then(data => {
                // Hide loading indicator
                loadingIndicator.style.display = 'none';

                // Add bot response to the chat history
                conversationHistory.push({role: 'bot', content: data.response});
                displayMessage(data.response, 'bot');
            })
            .catch(error => {
                console.error('Error:', error);
                loadingIndicator.style.display = 'none'; // Ensure loading is hidden on error
            });
    }
}

function displayMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(sender);

    messageElement.innerText = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
}

function startNewChat() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = ''; // Clear chat history

    // Reset conversation history
    conversationHistory = [];

    displayMessage('Welcome to the Travel Chatbot! How can I assist you today?', 'bot');
}

function toggleLoadingIndicator(state) {
    const loadingIndicator = document.getElementById('loading-indicator');
    const sendButton = document.getElementById('send-button');

    if (state) {
        loadingIndicator.classList.add('active');
        sendButton.classList.add('disabled');
    }else {
        loadingIndicator.classList.remove('active');
        sendButton.classList.remove('disabled');
    }
}

function sendMessage() {
    const inputElement = document.getElementById('user-input');
    const message = inputElement.value.trim();

    if (message) {
        // Add user message to the chat history
        conversationHistory.push({role: 'user', content: message});
        displayMessage(message, 'user');
        inputElement.value = '';

        // Show loading indicator
        toggleLoadingIndicator(true);

        // Send the conversation history to the backend
        fetch('/api/v1/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({conversation: conversationHistory})
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const chatBox = document.getElementById('chat-box');
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.classList.add('bot');

                messageElement.innerText = "";
                chatBox.appendChild(messageElement);

                const reader = response.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let result = '';

                reader.read().then(function processText({done, value}) {
                    if (done) {
                        // Hide loading indicator
                        toggleLoadingIndicator(false);
                        // Add bot response to the chat history
                        conversationHistory.push({role: 'bot', content: result});
                        return;
                    }

                    const text = decoder.decode(value, {stream: true});

                    //remove the first text "data: " from the text
                    const data = text.substring(6);
                    const json = JSON.parse(`${data}`);


                    messageElement.innerText += json.content;
                    result += json.content;


                    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
                    return reader.read().then(processText);
                });

            })
            .catch(error => {
                console.error('Error:', error);
                toggleLoadingIndicator(false); // Ensure loading is hidden on error
            });
    }
}
