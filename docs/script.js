document.getElementById('chat-icon').addEventListener('click', () => {
  document.getElementById('chat-container').classList.toggle('hidden');
});

// Invia con bottone o Enter
document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') sendMessage();
});

// Messaggio di benvenuto
window.addEventListener('load', () => {
  setTimeout(() => {
    appendMessage("Hey! Do you need some help with anything?", 'bot');
  }, 1000);
});

function appendMessage(text, sender = 'user') {
  const div = document.createElement('div');
  div.textContent = text;
  div.className = sender === 'user' ? 'user-msg' : 'bot-msg';
  document.getElementById('chat-box').appendChild(div);
  document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message) return;
  appendMessage(message, 'user');
  input.value = '';

  // Mostra "is typing..."
  const loadingMsg = document.createElement('div');
  loadingMsg.textContent = "Assistant is typing...";
  loadingMsg.className = 'bot-msg typing-msg';
  document.getElementById('chat-box').appendChild(loadingMsg);

  try {
    const response = await fetch('https://chatbot-backend-646865677192.europe-west1.run.app/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    loadingMsg.remove();
    appendMessage(data.response, 'bot');
  } catch (err) {
    loadingMsg.remove();
    appendMessage("Server communication error 😵", 'bot');
  }
}
