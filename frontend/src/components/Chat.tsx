/// <reference types="chrome" />

import { useState } from 'react'
import Response from './Response'
import '../App.css'

/*
    This component is the main chat used in the extension
    to interface with NaviGator
*/  

function Chat() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  // list of prompts that can be displayed above the text field
  const prompts = [
    'Ask a question!',
    'What can I help you find?',
    'What would you like to know?',
    'Need help looking for something?',
    'What are you looking for today?',
  ]
  const [prompt] = useState(
    () => prompts[Math.floor(Math.random() * prompts.length)]
  );

  async function sendMessage(event: React.FormEvent<HTMLFormElement>) 
  {
    event.preventDefault();
    setLoading(true);

    try {
      // infer the Canvas base URL from the currently open Canvas tab
      const [tab] = await chrome.tabs.query({
        active: true,
        lastFocusedWindow: true,
      });

      // get base URL
      let baseURL;
      if (tab?.url) {
        baseURL = new URL(tab.url).origin
      }
      else {
        baseURL = "";
      }

      let cookieMap: Record<string, string> = {};
      if (baseURL && chrome?.cookies?.getAll) {
        // grab the active Canvas session cookies
        const cookies = await chrome.cookies.getAll({ url: baseURL });

        cookieMap = Object.fromEntries(
          cookies.map((cookie) => [cookie.name, cookie.value])
        );
      }

      // call chat/ backend endpoint, pass in message, base URL, and Canvas session cookies
      const res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({
              message: message,
              base_url: baseURL,
              cookies: cookieMap
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
          
          <label htmlFor="prompt" className="block text-sm/6 font-semibold text-gray-900">
            {prompt}
          </label>

          <div className="relative mt-2.5 w-100 max-w-full">

            <textarea
              id="prompt"
              name="prompt"
              rows={1}
              onKeyDown={(event) => {
                if (
                  event.key === 'Enter' &&
                  !event.shiftKey &&
                  !event.nativeEvent.isComposing
                ) {
                  event.preventDefault();
                  event.currentTarget.form?.requestSubmit();
                }
              }}
              value={message}
              onChange={(event) => {
                setMessage(event.target.value);
                event.target.style.height = '0px';
                event.target.style.height = `${event.target.scrollHeight}px`;
              }}
              placeholder="Type your message..."
              autoComplete="off"
              className="block min-h-12 w-full resize-none overflow-hidden rounded-2xl bg-white py-2 pl-3.5 pr-14 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
            />

            <button
              type="submit"
              disabled={loading}
              aria-label={loading ? 'Waiting for response' : 'Send message'}
              className="absolute bottom-2 right-2 flex size-8 items-center justify-center rounded-full bg-indigo-500 text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" className="size-5 animate-spin">
                  <circle cx="12" cy="12" r="9" stroke="currentColor" strokeOpacity="0.3" strokeWidth="3" />
                  <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeLinecap="round" strokeWidth="3" />
                </svg>
              ) : (
                <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="size-5">
                  <path d="M12 19V5" />
                  <path d="m5 12 7-7 7 7" />
                </svg>
              )}
            </button>

          </div>

          {/* Pass in the response variable as a prop for the Response component to display */}
          <Response response={response} />

        </form>
      </div>
    </>
  )
}

export default Chat
