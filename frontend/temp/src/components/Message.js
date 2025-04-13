import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { coldarkDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import "./Message.css";

const Message = ({ sender, text }) => {
  const [copiedCodeBlockIndex, setCopiedCodeBlockIndex] = useState(null);

  // Function to copy the code content to the clipboard
  const copyToClipboard = (codeContent, index) => {
    navigator.clipboard.writeText(codeContent);
    setCopiedCodeBlockIndex(index);
    setTimeout(() => setCopiedCodeBlockIndex(null), 1000); // Reset after 1 second
  };

  return (
    <div className={`message ${sender === "user" ? "user" : "codemate"}`}>
      <div className="message-sender">
        {sender === "user" ? "You" : "CodeMate"}
      </div>

      <div className="message-text">
        <ReactMarkdown
          components={{
            code({ inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || "");
              const codeContent = String(children).replace(/\n$/, "");
              const index = props.node.position.start.offset;

              return !inline && match ? (
                <div className="code-container">
                  <SyntaxHighlighter
                    style={coldarkDark}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {codeContent}
                  </SyntaxHighlighter>
                  <button
                    className="copy-button"
                    onClick={() => copyToClipboard(codeContent, index)}
                  >
                    {copiedCodeBlockIndex === index ? "Copied!" : "Copy"}
                  </button>
                </div>
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
          }}
        >
          {text}
        </ReactMarkdown>
      </div>
    </div>
  );
};

export default Message;
