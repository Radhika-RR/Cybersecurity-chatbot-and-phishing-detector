document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show active tab pane
            tabPanes.forEach(pane => pane.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Phishing detection functionality
    const checkButton = document.getElementById('check-phishing');
    const emailTextarea = document.getElementById('email-text');
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    const confidenceText = document.getElementById('confidence');
    
    checkButton.addEventListener('click', async () => {
        const emailText = emailTextarea.value.trim();
        
        if (!emailText) {
            alert('Please enter email content to check');
            return;
        }
        
        try {
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: emailText })
            });
            
            if (!response.ok) {
                throw new Error('Server error');
            }
            
            const data = await response.json();
            
            // Display results
            resultDiv.classList.remove('hidden');
            resultDiv.className = data.is_phishing ? 'phishing' : 'legitimate';
            
            resultText.textContent = data.message;
            confidenceText.textContent = `Confidence: ${(data.probability * 100).toFixed(2)}%`;
            
        } catch (error) {
            console.error('Error:', error);
            alert('Error checking email. Please try again.');
        }
    });
    
    // Chatbot functionality
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
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
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error('Server error');
            }
            
            const data = await response.json();
            addMessage(data.response);
            
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error. Please try again.');
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
});