document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, initializing application...");
    
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    console.log(`Found ${tabButtons.length} tab buttons and ${tabPanes.length} tab panes`);
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            console.log(`Switching to tab: ${tabId}`);
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show active tab pane
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
                if (pane.id === tabId) {
                    pane.classList.add('active');
                    console.log(`Tab ${tabId} is now active`);
                }
            });
        });
    });
    
    // Phishing detection functionality
    const checkButton = document.getElementById('check-phishing');
    const emailTextarea = document.getElementById('email-text');
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    const confidenceText = document.getElementById('confidence');
    
    if (checkButton && emailTextarea) {
        checkButton.addEventListener('click', async () => {
            const emailText = emailTextarea.value.trim();
            
            if (!emailText) {
                alert('Please enter email content to check');
                return;
            }
            
            try {
                console.log("Sending request to /predict endpoint");
                const response = await fetch('http://localhost:8000/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: emailText })
                });
                
                if (!response.ok) {
                    throw new Error(`Server responded with status: ${response.status}`);
                }
                
                const data = await response.json();
                console.log("Received response:", data);
                
                // Display results
                resultDiv.classList.remove('hidden');
                resultDiv.className = data.is_phishing ? 'phishing' : 'legitimate';
                
                resultText.textContent = data.message;
                confidenceText.textContent = `Confidence: ${(data.probability * 100).toFixed(2)}%`;
                
            } catch (error) {
                console.error('Error:', error);
                alert('Error checking email. Please make sure the server is running and try again.');
            }
        });
    } else {
        console.error("Phishing detection elements not found");
    }
    
    // Chatbot functionality
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    if (chatMessages && userInput && sendButton) {
        function addMessage(text, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
            messageDiv.textContent = text;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        async function sendMessage() {
            const message = userInput.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, true);
            userInput.value = '';
            
            try {
                console.log("Sending message to chatbot:", message);
                const response = await fetch('http://localhost:8000/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                
                if (!response.ok) {
                    throw new Error(`Server responded with status: ${response.status}`);
                }
                
                const data = await response.json();
                console.log("Chatbot response:", data);
                addMessage(data.response);
                
            } catch (error) {
                console.error('Error:', error);
                addMessage('Sorry, I encountered an error. Please make sure the server is running and try again.');
            }
        }
        
        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Add welcome message
        addMessage("Hello! I'm your cybersecurity assistant. How can I help you today?");
    } else {
        console.error("Chatbot elements not found");
    }
    
    console.log("Application initialized successfully");
});