/// <reference types="chrome" />

import { useState } from 'react'
import '../../App.css'

/*
    This component accepts a Canvas API endpoint (such as 
    https://ufl.instructure.com/api/v1/users/self/profile)
    and returns acessible data in Canvas session cookies
*/

function CanvasInfo() {
  const [baseURL, setBaseURL] = useState('');
  const [endpoint, setEndpoint] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState('');

  async function getCanvasData(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const [tab] = await chrome.tabs.query({
      active: true,
      lastFocusedWindow: true,
    });

    if (!tab?.url) {
      setStatus('Base URL could not be accessed.');
      setError(true);
      return;
    }

    const currentOrigin = new URL(tab.url).origin;
    const nextEndpoint = endpoint.trim();

    setBaseURL(currentOrigin);
    setEndpoint(nextEndpoint);
    setLoading(true);
    setResponse('');
    setStatus('Fetching...');

    chrome.storage.local.set({ 
        canvasBaseUrl: currentOrigin, 
        canvasEndpoint: nextEndpoint 
    });

    try {
      if (!chrome?.cookies || typeof chrome.cookies.getAll !== 'function') {
        setStatus('This extension is missing the Chrome cookies permission. Reload the extension in chrome://extensions and try again.');
        setError(true);
        return;
      }

      // access cookies from the base URL of the currently opened Canvas tab
      const cookies = await chrome.cookies.getAll({ url: nextEndpoint });
      const cookieMap = Object.fromEntries(
        cookies.map((cookie) => [cookie.name, cookie.value])
      );

      // call canvas/ backend API endpoint
      const res = await fetch('http://localhost:8000/canvas', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          endpoint: nextEndpoint,
          cookies: cookieMap,
        }),
      });

      if (res.status === 401 || res.status === 403) {
        setStatus('Not authenticated. Make sure you are logged into Canvas in this browser, then try again.');
        setError(true);
        return;
      }

      if (!res.ok) {
        setStatus(`Request failed: ${res.status} ${res.statusText}`);
        setError(true);
        return;
      }

      // get JSON data and format it
      const data = await res.json();
      const payload = data?.response ?? data;
      let formatted;
      if (typeof payload === 'string') {
        formatted = payload;
      }
      else {
        formatted = JSON.stringify(payload, null, 2);
      }

      setResponse(formatted);

      if (!payload) {
        setStatus('No response body returned.');
        setError(true);
        return;
      }

      setStatus('Raw JSON received.');
    } 
    catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setStatus('Error: ' + message);
      setError(true);
      console.error(err);
    } 
    finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="mt-6">
        <form onSubmit={getCanvasData} className="flex flex-col items-center">
          <label htmlFor="prompt" className="block text-sm/6 font-semibold text-white">
            Canvas API endpoint
          </label>
          <div className="mt-2.5">
            <input
              id="prompt"
              name="prompt"
              type="url"
              value={endpoint}
              onChange={(e) => setEndpoint(e.target.value)}
              placeholder="https://schoolname.instructure.com/api/v1/"
              className="block w-100 rounded-md bg-white/5 px-3.5 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
            />
          </div>
          
          <div className="mt-6">
            <button
              type="submit"
              disabled={loading}
              className="block rounded-md bg-orange-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
              {loading ? 'Getting endpoint data...' : 'Access API Endpoint'}
            </button>
          </div>

          {baseURL && (
            <p className="mt-3 text-xs text-gray-300">Current Canvas origin: {baseURL}</p>
          )}

          {error && status && <p className="mt-4 text-sm text-red-500">{status}</p>}
          {!error && status && <p className="mt-4 text-sm text-white">{status}</p>}

          {response && (
            <pre className="mt-6 max-w-2xl w-full rounded-md bg-white/10 p-4 text-left text-xs text-white overflow-auto whitespace-pre-wrap">
              {response}
            </pre>
          )}
        </form>
      </div>
    </>
  );
}

export default CanvasInfo
