const chatbotMessages = document.getElementById('chatbotMessages');
const questions = document.querySelectorAll('.question');
const chatbotContainer = document.getElementById('chatbotContainer');
const chatbotButton = document.getElementById('chatbotButton');
const closeBtn = document.getElementById('closeBtn');

const responses = {
    "What are common skin diseases?": "Common skin diseases include eczema, psoriasis, acne, and dermatitis.",
    "What causes acne?": "Acne is primarily caused by hormonal changes, excess oil production, clogged pores, and bacteria.",
    "How can I treat eczema?": "Eczema can be treated with moisturizers, topical corticosteroids, and avoiding irritants.",
    "What are the symptoms of psoriasis?": "Symptoms of psoriasis include red patches of skin covered with thick, silvery scales, dry and cracked skin, and itching.",
    "What should I do if I have a rash?": "If you have a rash, keep the area clean and dry, avoid scratching, and consider over-the-counter treatments. Consult a doctor if it worsens.",
    "How can I prevent skin infections?": "To prevent skin infections, keep your skin clean and dry, avoid sharing personal items, and treat cuts or wounds promptly.",
    "What are the signs of skin cancer?": "Signs of skin cancer include changes in moles, growths that bleed or don’t heal, and new spots on the skin. Consult a dermatologist for any concerns.",
    "How can I treat dry skin?": "Dry skin can be treated with regular moisturizing, using gentle cleansers, and avoiding hot showers."
};


questions.forEach(question => {
question.addEventListener('click', () => {
const selectedQuestion = question.getAttribute('data-question');
const response = responses[selectedQuestion];
addMessage(`You: ${selectedQuestion}`, 'user-message');
addMessage(`Bot: ${response}`, 'bot-message');
});
});

function addMessage(message, className) {
const messageDiv = document.createElement('div');
messageDiv.className = `message ${className}`;
messageDiv.textContent = message;
chatbotMessages.appendChild(messageDiv);
chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to the bottom
}

let isChatbotOpen = false;

chatbotButton.addEventListener('click', () => {
if (!isChatbotOpen) {
chatbotContainer.style.display = 'flex';
chatbotContainer.style.animation = 'slideIn 0.5s forwards';
isChatbotOpen = true;
}
});

closeBtn.addEventListener('click', () => {
chatbotContainer.style.animation = 'slideOut 0.5s forwards';
chatbotContainer.addEventListener('animationend', () => {
chatbotContainer.style.display = 'none';
isChatbotOpen = false; // Update the state when closed
}, { once: true }); // Ensure this runs only once
});

