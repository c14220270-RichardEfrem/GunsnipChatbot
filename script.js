const chatInput = document.querySelector(".chat-input textarea");
const sendChatbtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");

const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? `<p></p>` : `<img src="gunsnip_chat.jpg" alt=""><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
}

const handleChat = () => {
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append user's message to the chatbox
    const userChatLi = createChatLi(userMessage, "outgoing");
    chatbox.appendChild(userChatLi);

     // Send user message to backend
    fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response in the chatbox
        chatbox.appendChild(createChatLi(data.answer, "incoming"));
        chatbox.scrollTo(0, chatbox.scrollHeight);
    })
    .catch(error => console.error("Error:", error));

    // chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    // chatbox.scrollTo(0, chatbox.scrollHeight);
}

chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatbtn.addEventListener("click", handleChat);
