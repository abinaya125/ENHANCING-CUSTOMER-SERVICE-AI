const apiUrl = "http://127.0.0.1:5000/chat";  // Ensure Flask is running at this URL

document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();

    if (message === "") return;

    // Display user message in chat box
    addMessage("You", message);
    userInput.value = "";

    // Show a loading message
    addMessage("Bot", "Thinking...");

    // Send message to API
    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        removeLastMessage();

        if (data.response) {
            addMessage("Bot", data.response);
        } else {
            addMessage("Bot", "Error: No response from server.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        removeLastMessage();
        addMessage("Bot", "Error connecting to server.");
    });
}

function addMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLastMessage() {
    const chatBox = document.getElementById("chat-box");
    if (chatBox.lastChild) {
        chatBox.removeChild(chatBox.lastChild);
    }
}
