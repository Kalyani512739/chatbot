async function sendMessage() {
    let input = document.getElementById("message");
    let chatbox = document.getElementById("chatbox");

    let userText = input.value.trim();

    if (!userText) return;

    chatbox.innerHTML += `<div class="user-msg">You: ${userText}</div>`;

    input.value = "";

    try {
        let response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userText })
        });

        let data = await response.json();

        chatbox.innerHTML += `<div class="bot-msg">Bot: ${data.reply}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;

    } catch (error) {
        chatbox.innerHTML += `<div class="bot-msg">Error connecting to server 😑</div>`;
    }
}