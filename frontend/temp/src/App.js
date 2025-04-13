// src/App.js
import React, { useState } from "react";
import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false); // State to track loading

  const handleSend = async (text) => {
    // Add user's message
    setMessages((prev) => [...prev, { sender: "user", text }]);
    setLoading(true); // Set loading to true when message is sent

    // Send the message to the backend (Flask) and get the response
    try {
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();

      // Add CodeMate's response
      setMessages((prev) => [
        ...prev,
        { sender: "codemate", text: data.reply },
      ]);
    } catch (error) {
      console.error("Error communicating with backend:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "codemate", text: "Sorry, something went wrong." },
      ]);
    } finally {
      setLoading(false); // Set loading to false after the response is received
    }
  };

  return (
    <div className="app">
      <Header />
      <ChatWindow messages={messages} loading={loading} />{" "}
      {/* Pass loading state */}
      <InputBox onSend={handleSend} />
    </div>
  );
}

export default App;
