import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

// Define API endpoints
const REDACT_API_URL = "http://127.0.0.1:8000/redact/";
const QUERY_API_URL = "http://127.0.0.1:8001/query/";

const headers = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*'
};

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { 
      text: userMessage, 
      isUser: true,
      timestamp: new Date().toISOString()
    }]);
    
    setIsLoading(true);

    try {
      console.log('Sending to redaction API:', userMessage);
      
      // First API call - Redaction
      const redactResponse = await axios.post(REDACT_API_URL, {
        text: userMessage
      }, { headers });

      console.log('Redaction response:', redactResponse.data);

      if (!redactResponse.data.redacted_text) {
        throw new Error('Redaction API returned no text');
      }

      console.log('Sending to query API:', redactResponse.data.redacted_text);

      // Second API call - Query with redacted text
      const queryResponse = await axios.post(QUERY_API_URL, {
        text: redactResponse.data.redacted_text
      }, { headers });

      console.log('Query response:', queryResponse.data);

      if (!queryResponse.data.response_text) {
        throw new Error('Query API returned no text');
      }

      // Add bot response to chat
      setMessages(prev => [...prev, { 
        text: queryResponse.data.response_text,
        isUser: false,
        timestamp: new Date().toISOString()
      }]);
    } catch (error) {
      console.error('API Error Details:', error);
      setMessages(prev => [...prev, {
        text: `Error: ${error.message}`,
        isUser: false,
        error: true,
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickReply = (message) => {
    setInput(message);
    handleSubmit(new Event('submit'));
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900">
      {/* Chat Header */}
      <div className="bg-gray-800 p-4 shadow-md">
        <h1 className="text-xl font-semibold text-white">REDACTOR Assistant</h1>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900">
        {messages.map((message, index) => (
          <div
            key={`${message.timestamp}-${index}`}
            className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                message.isUser
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : message.error 
                    ? 'bg-red-600 text-white rounded-bl-none'
                    : 'bg-gray-700 text-gray-100 rounded-bl-none'
              }`}
            >
              {message.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 rounded-2xl px-4 py-2 text-gray-100">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="border-t border-gray-700 p-4 bg-gray-800">
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 p-2 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            Send
          </button>
        </form>
      </div>

      {/* Quick Reply Buttons */}
      {/* <div className="p-4 bg-gray-800 border-t border-gray-700">
        <div className="flex flex-wrap gap-2">
          <button 
            onClick={() => handleQuickReply("Hello!")}
            className="px-3 py-1 bg-gray-700 text-gray-200 rounded-full hover:bg-gray-600 transition-colors"
          >
            👋 Say Hello
          </button>
          <button 
            onClick={() => handleQuickReply("What can you do?")}
            className="px-3 py-1 bg-gray-700 text-gray-200 rounded-full hover:bg-gray-600 transition-colors"
          >
            ❓ Help
          </button>
          <button 
            onClick={() => handleQuickReply("Tell me a joke")}
            className="px-3 py-1 bg-gray-700 text-gray-200 rounded-full hover:bg-gray-600 transition-colors"
          >
            😄 Fun
          </button>
        </div>
      </div> */}
    </div>
  );
};

export default Chat; 