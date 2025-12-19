// Chat Widget JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');

    // Toggle chat window
    chatToggle.addEventListener('click', function() {
        chatWindow.style.display = chatWindow.style.display === 'flex' ? 'none' : 'flex';
    });

    // Close chat window
    chatClose.addEventListener('click', function() {
        chatWindow.style.display = 'none';
    });

    // Send message function
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            // Add user message
            addMessage(message, 'user');
            chatInput.value = '';

            // Simulate AI response
            setTimeout(() => {
                const response = getAIResponse(message);
                addMessage(response, 'bot');
            }, 1000);
        }
    }

    // Add message to chat
    function addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Simple AI response logic
    function getAIResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
            return "Hello! How can I help you today?";
        } else if (lowerMessage.includes('helps')) {
            return "I'm here to assist you with any questions about the online exam system. What do you need help with?";
        } else if (lowerMessage.includes('exam') || lowerMessage.includes('test')) {
            return "For exam-related questions, please check the exam section or contact your teacher.";
        } else if (lowerMessage.includes('profile') || lowerMessage.includes('account')) {
            return "You can manage your profile in the student/teacher profile section.";
        } else if (lowerMessage.includes('thank')) {
            return "You're welcome! Is there anything else I can help you with?";
        } else {
            return "I'm sorry, I didn't understand that. Can you please rephrase your question?";
        }
    }

    // Event listeners
    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
