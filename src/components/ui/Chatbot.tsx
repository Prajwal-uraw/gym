// // src/components/ui/Chatbot.tsx
// import React, { useState } from 'react';
// import { apiClient } from '@/lib/api';
// import { toast } from 'sonner';

// interface Message {
//   from: 'user' | 'bot';
//   text: string;
// }

// const Chatbot: React.FC = () => {
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [input, setInput] = useState('');
//   const [loading, setLoading] = useState(false);

//   const sendMessage = async () => {
//     if (!input.trim()) return;

//     const userMessage: Message = { from: 'user', text: input };
//     setMessages(prev => [...prev, userMessage]);
//     setInput('');
//     setLoading(true);

//     try {
//       // Send to backend (replace with your actual chatbot endpoint)
//       const response = await apiClient.request<{ reply: string }>('/chatbot', {
//         method: 'POST',
//         body: JSON.stringify({ message: userMessage.text }),
//       });

//       const botMessage: Message = { from: 'bot', text: response.reply };
//       setMessages(prev => [...prev, botMessage]);
//     } catch (error: any) {
//       toast.error('Chatbot error: ' + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="bg-white shadow-lg rounded-lg w-full p-4 flex flex-col h-96">
//       <div className="flex-1 overflow-y-auto space-y-2 mb-2">
//         {messages.map((msg, i) => (
//           <div
//             key={i}
//             className={`p-2 rounded-md ${msg.from === 'user' ? 'bg-blue-100 self-end' : 'bg-gray-100 self-start'}`}
//           >
//             {msg.text}
//           </div>
//         ))}
//       </div>
//       <div className="flex">
//         <input
//           className="flex-1 border rounded-l-md p-2"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
//           placeholder="Ask something..."
//         />
//         <button
//           className="bg-blue-500 text-white px-4 rounded-r-md"
//           onClick={sendMessage}
//           disabled={loading}
//         >
//           {loading ? '...' : 'Send'}
//         </button>
//       </div>
//     </div>
//   );
// };

// export default Chatbot;
import React, { useState } from 'react';
import { apiClient } from '@/lib/api';
import { toast } from 'sonner';

interface Message {
  from: 'user' | 'bot';
  text: string;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false); // <--- toggle chat window

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { from: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await apiClient.request<{ reply: string }>('/chatbot', {
        method: 'POST',
        body: JSON.stringify({ message: userMessage.text }),
      });

      const botMessage: Message = { from: 'bot', text: response.reply };
      setMessages(prev => [...prev, botMessage]);
    } catch (error: any) {
      toast.error('Chatbot error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-5 right-5 z-50 flex flex-col items-end">
      {/* Chat toggle button */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-full shadow-lg hover:bg-blue-700"
        >
          Chat with us
        </button>
      )}

      {/* Chat window */}
      {open && (
        <div className="bg-white shadow-lg rounded-lg w-80 h-96 flex flex-col">
          <div className="flex justify-between items-center p-2 border-b">
            <span className="font-medium">Chatbot</span>
            <button
              onClick={() => setOpen(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          <div className="flex-1 p-2 overflow-y-auto space-y-2">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`p-2 rounded-md ${
                  msg.from === 'user'
                    ? 'bg-blue-100 self-end'
                    : 'bg-gray-100 self-start'
                }`}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <div className="flex border-t p-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Type your message..."
              className="flex-1 border rounded-l-md p-2"
            />
            <button
              onClick={sendMessage}
              className="bg-blue-500 text-white px-4 rounded-r-md"
              disabled={loading}
            >
              {loading ? '...' : 'Send'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
