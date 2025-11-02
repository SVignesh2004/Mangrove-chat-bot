import { useState } from "react";
import axios from "axios";
import home from "../assets/home.jpg";

function Home() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "👋 Welcome! I’m your Mangrove Info Assistant. Ask me anything about mangrove forests — flora, fauna, economy, tourism, or ecology.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("https://mangrove-chat-bot.onrender.com/chat", { message: input });
      const botReply = res.data.reply || "Sorry, no response from the bot.";
      setMessages((prev) => [...prev, { sender: "bot", text: botReply }]);
    } catch (err) {
      console.log(err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Server error. Please try again later." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-1">
      {/* 🌿 Left: Image Section */}
      <div className="w-2/5 hidden md:flex items-center justify-center bg-gray-100">
        <img
          src={home}
          alt="Mangrove Forest"
          className="object-cover w-full h-full rounded-r-3xl shadow-lg"
        />
      </div>

      {/* 💬 Right: Chat Section */}
      <div className="w-full md:w-3/5 flex flex-col justify-center items-center p-4">
        <div className="w-full md:w-4/5 bg-white rounded-3xl shadow-xl flex flex-col h-[80vh]">
          {/* Chat Header */}
          <header className="bg-green-600 text-white text-center py-3 text-xl font-semibold rounded-t-3xl">
            🐚 Mangrove Forest Chatbot
          </header>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${
                  msg.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-xs px-4 py-2 rounded-2xl shadow text-white ${
                    msg.sender === "user"
                      ? "bg-green-500 text-right"
                      : "bg-gray-600 text-left"
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            {loading && (
              <p className="text-center text-sm text-gray-500">Bot is typing...</p>
            )}
          </div>

          {/* Input */}
          <form
            onSubmit={handleSend}
            className="flex items-center gap-2 p-3 bg-gray-50 rounded-b-3xl border-t"
          >
            <input
              type="text"
              className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-400"
              placeholder="Ask about Mangrove forests..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button
              type="submit"
              className="bg-green-600 text-white px-5 py-2 rounded-full hover:bg-green-700"
              disabled={loading}
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Home;
