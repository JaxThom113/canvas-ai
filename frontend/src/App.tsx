/// <reference types="chrome" />
import { useEffect, useState } from 'react'
import './App.css'

interface CanvasCourse {
  id: number;
  name?: string;
  course_code?: string;
}

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage(event: React.FormEvent<HTMLFormElement>) 
  {
    event.preventDefault();
    setLoading(true);

    try 
    {
      const res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({
              message: message
          })
      });

      const data = await res.json();
      setResponse(data.response);
    } 
    catch (error) 
    {
      console.error(error);
      setResponse("Failed to contact backend.");
    } 
    finally 
    {
      setLoading(false);
    }
  }

  const [cdMessage, setCdMessage] = useState("");
  const [cdStatus, setCdStatus] = useState("");
  const [cdLoading, setCdLoading] = useState(false);
  const [courses, setCourses] = useState<CanvasCourse[]>([]);

  // load the last-used Canvas base URL
  useEffect(() => {
    chrome.storage.local.get(["canvasBaseUrl"], (result: { canvasBaseUrl?: string }) => {
      if (result.canvasBaseUrl) {
        setCdMessage(result.canvasBaseUrl);
      }
    });
  }, []);
  
  async function getCanvasData(event: React.FormEvent<HTMLFormElement>) 
  {
    event.preventDefault();

    const rawBase = cdMessage.trim().replace(/\/+$/, "");
    if (!rawBase) {
      setCdStatus("Enter your Canvas base URL first.");
      return; 
    }

    setCdLoading(true);
    setCourses([]);
    setCdStatus("Fetching...");

    chrome.storage.local.set({ canvasBaseUrl: rawBase });

    const endpoint =
      `${rawBase}/api/v1/courses?enrollment_state=active&per_page=100`;

    // const endpoint = 
    //   `${rawBase}/api/v1/users/self/profile`

    try 
    {
      const res = await fetch(endpoint, {
        method: "GET",
        credentials: "include", // sends your existing Canvas session cookie
        headers: {
          Accept: "application/json",
        },
      });
 
      if (res.status === 401 || res.status === 403) 
      {
        setCdStatus("Not authenticated. Make sure you're logged into Canvas in this browser, then try again.");
        return;
      }
 
      if (!res.ok) 
      {
        setCdStatus(`Request failed: ${res.status} ${res.statusText}`);
        return;
      }
 
      const data: CanvasCourse[] = await res.json();
      console.log("Canvas courses:", data);
 
      if (!Array.isArray(data) || data.length === 0) 
      {
        setCdStatus("No active courses found.");
        return;
      }
 
      setCdStatus(`${data.length} course(s) found.`);
      setCourses(data);
    } 
    catch (err) 
    {
      const message = err instanceof Error ? err.message : String(err);
      setCdStatus("Error: " + message);
      console.error(err);
    } 
    finally 
    {
      setCdLoading(false);
    }
  }

  return (
    <>
      <div className="flex flex-col items-center justify-center isolate p-6 bg-gray-900 sm:py-10 lg:px-30">
        <div
          aria-hidden="true"
          className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
        >
          <div
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
            className="relative left-1/2 -z-10 aspect-1155/678 w-144.5 max-w-none -translate-x-1/2 rotate-30 bg-linear-to-tr from-[#ff80b5] to-[#9089fc] opacity-20 sm:left-[calc(50%-40rem)] sm:w-288.75"
          />
        </div>

        <h1 className="block text-4xl font-semibold text-white py-4">
          CanvasAI
        </h1>

        <form onSubmit={sendMessage} className="flex flex-col items-center">
          <label htmlFor="prompt" className="block text-sm/6 font-semibold text-white">
            Ask a question!
          </label>
          <div className="mt-2.5">
            <input
              id="prompt"
              name="prompt"
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
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

          {/* {error && <p className="mt-4 text-sm text-red-300">{error}</p>} */}
          {response && (
            <div className="mt-6 max-w-2xl whitespace-pre-wrap rounded-md bg-white/10 p-4 text-left text-white">
              {response}
            </div>
          )}
        </form>


        <form onSubmit={getCanvasData} className="flex flex-col items-center">
          <label htmlFor="prompt" className="block text-sm/6 font-semibold text-white">
            Input your Canvas base URL:
          </label>
          <div className="mt-2.5">
            <input
              id="prompt"
              name="prompt"
              type="text"
              value={cdMessage}
              onChange={(e) => setCdMessage(e.target.value)}
              placeholder="https://ufl.instructure.com"
              autoComplete="off"
              className="block w-100 rounded-md bg-white/5 px-3.5 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
            />
          </div>
          
          <div className="mt-6">
          <button
            type="submit"
            disabled={cdLoading}
            className="block rounded-md bg-orange-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
          >
            {cdLoading ? 'Submitting...' : 'Submit'}
          </button>
          </div>

          
          {cdStatus && <p className="mt-4 text-sm text-red-300">{cdStatus}</p>}
 
          {courses.length > 0 && (
            <ul className="mt-6 max-w-2xl w-full rounded-md bg-white/10 p-4 text-left text-white">
              {courses.map((course) => (
                <li key={course.id} className="border-b border-white/10 py-2 last:border-none">
                  {course.name || course.course_code || `Course ${course.id}`}
                  {course.course_code && (
                    <div className="text-xs text-gray-400">{course.course_code}</div>
                  )}
                </li>
              ))}
            </ul>
          )}

        </form>

      </div>
    </>
  )
}

export default App
