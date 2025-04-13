// src/components/ChatWindow.js
import React from 'react';
import Message from './Message';
import './ChatWindow.css';

const ChatWindow = ({ messages, loading }) => {
  return (
    <div className="chat-window">
      {messages.map((message, index) => (
        <Message key={index} sender={message.sender} text={message.text} />
      ))}
      {loading && <div className="loading">CodeMate is typing...</div>} {/* Display loading state */}
    </div>
  );
};

export default ChatWindow;
