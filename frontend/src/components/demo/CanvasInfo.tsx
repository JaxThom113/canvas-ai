/// <reference types="chrome" />

import { useState } from 'react'
import '../../App.css'

/*
    This component accepts a Canvas API endpoint (such as 
    https://ufl.instructure.com/api/v1/users/self/profile)
    and returns acessible data in Canvas session cookies
*/

function CanvasInfo() {
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

    // infer base URL from the currently open Canvas tab (i.e. https://ufl.instructure.com)
    const baseURL = new URL(tab.url).origin;
    setEndpoint(endpoint.trim());

    // combine the base URL and the endpoint (i.e. "https://ufl.instructure.com" + "/api/v1/users/self/courses")
    // endpoint first, then base URL: new URL("/api/v1/users/self/courses", "https://ufl.instructure.com")
    const fullURL = new URL(endpoint, baseURL).href;

    setLoading(true);
    setResponse('');
    setStatus('Fetching...');

    // access changes in Chrome from the open Canvas tab
    chrome.storage.local.set({ 
        canvasBaseUrl: baseURL, 
        canvasEndpoint: fullURL 
    });

    try {
      if (!chrome?.cookies || typeof chrome.cookies.getAll !== 'function') {
        setStatus('This extension is missing the Chrome cookies permission. Reload the extension in chrome://extensions and try again.');
        setError(true);
        return;
      }

      // access cookies from the base URL of the currently opened Canvas tab
      const cookies = await chrome.cookies.getAll({ url: fullURL });
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
          endpoint: fullURL,
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
      <div className="mt-6 flex w-full max-w-2xl flex-col items-center rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <form onSubmit={getCanvasData} className="flex flex-col items-center">
          <label htmlFor="prompt" className="block text-sm/6 font-semibold text-gray-900">
            Canvas API endpoint
          </label>
          <div className="relative mt-2.5 w-100 max-w-full">
            <input
              id="prompt"
              name="prompt"
              type="text"
              value={endpoint}
              onChange={(e) => setEndpoint(e.target.value)}
              placeholder="api/v1/users/self/courses"
              className="block min-h-12 w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
            />
          </div>
          
          <div className="mt-6">
            <button
              type="submit"
              disabled={loading}
              className="block rounded-md bg-indigo-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? 'Getting endpoint data...' : 'Access API Endpoint'}
            </button>
          </div>

          {error && status && <p className="mt-4 text-sm text-red-600">{status}</p>}
          {!error && status && <p className="mt-4 text-sm text-gray-700">{status}</p>}

          {response && (
            <pre className="mt-6 w-full max-w-2xl overflow-auto whitespace-pre-wrap wrap-break-word rounded-md border border-gray-200 bg-white p-4 text-left text-xs text-gray-900">
              {response}
            </pre>
          )}
        </form>
      </div>
    </>
  );
}

export default CanvasInfo
