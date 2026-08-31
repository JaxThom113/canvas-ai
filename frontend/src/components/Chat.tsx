import { useState } from 'react'
import '../App.css'

/*
    This component accepts is a main chat used in the extension
    to interface with Gemini
*/  

function Chat() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage(event: React.FormEvent<HTMLFormElement>) 
  {
    event.preventDefault();
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({
              input: input
          })
      });

      const data = await res.json();
      setResponse(data.response);
    } 
    catch (error) {
      console.error(error);
      setResponse("Failed to contact backend.");
    } 
    finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="mt-6">
        <form onSubmit={sendMessage} className="flex flex-col items-center">
          <label htmlFor="prompt" className="block text-sm/6 font-semibold text-white">
            Ask a question!
          </label>
          <div className="mt-2.5">
            <input
              id="prompt"
              name="prompt"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="What would you like to know?"
              autoComplete="off"
              className="block w-100 rounded-md bg-white/5 px-3.5 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
            />
          </div>

          <div className="mt-6">
            <button
              type="submit"
              disabled={loading}
              className="block rounded-md bg-indigo-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
              {loading ? 'Submitting...' : 'Submit'}
            </button>
          </div>

          {response && (
            <div className="mt-6 max-w-2xl whitespace-pre-wrap rounded-md bg-white/10 p-4 text-left text-white">
              {response}
            </div>
          )}
        </form>
      </div>
    </>
  )
}

export default Chat
