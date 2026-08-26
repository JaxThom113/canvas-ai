/// <reference types="chrome" />

import { useEffect, useState } from 'react'
import '../../App.css'

interface CanvasCourse {
  id: number;
  name?: string;
  course_code?: string;
}

/*
    This component accepts a Canvas base URL (such as https://ufl.instructure.com)
    and returns account data accessible in cookies
*/  

function CanvasInfo() {
  const [input, setInput] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [courses, setCourses] = useState<CanvasCourse[]>([]);

  // load the last-used Canvas base URL
  useEffect(() => {
    chrome.storage.local.get(["canvasBaseUrl"], (result: { canvasBaseUrl?: string }) => {
      if (result.canvasBaseUrl) {
        setInput(result.canvasBaseUrl);
      }
    });
  }, []);
  
  async function getCanvasData(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const rawBase = input.trim().replace(/\/+$/, "");
    if (!rawBase) {
      setStatus("Enter your Canvas base URL first.");
      return; 
    }

    setLoading(true);
    setCourses([]);
    setStatus("Fetching...");

    chrome.storage.local.set({ canvasBaseUrl: rawBase });

    /*
        Other endpoints can be:

        `${rawBase}/api/v1/users/self/profile`
        `${rawBase}/api/v1/users/self/todo`
        `${rawBase}/api/v1/courses/${courseId}/assignments`
        `${rawBase}/api/v1/courses/${courseId}/modules`
        `${rawBase}/api/v1/calendar_events?type=event`
    */

    const endpoint =
      `${rawBase}/api/v1/courses?enrollment_state=active&per_page=100`;

    try {
      const res = await fetch(endpoint, {
        method: "GET",
        credentials: "include", // sends your existing Canvas session cookie
        headers: {
          Accept: "application/json",
        },
      });
 
      if (res.status === 401 || res.status === 403) {
        setStatus("Not authenticated. Make sure you're logged into Canvas in this browser, then try again.");
        return;
      }
 
      if (!res.ok) {
        setStatus(`Request failed: ${res.status} ${res.statusText}`);
        return;
      }
 
      const data: CanvasCourse[] = await res.json();
      console.log("Canvas courses:", data);
 
      if (!Array.isArray(data) || data.length === 0) {
        setStatus("No active courses found.");
        return;
      }
 
      setStatus(`${data.length} course(s) found.`);
      setCourses(data);
    } 
    catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      setStatus("Error: " + message);
      console.error(err);
    } 
    finally {
      setLoading(false);
    }
  }

  return (
    <>
        <form onSubmit={getCanvasData} className="flex flex-col items-center">
            <label htmlFor="prompt" className="block text-sm/6 font-semibold text-white">
            Input your Canvas base URL:
            </label>
            <div className="mt-2.5">
            <input
                id="prompt"
                name="prompt"
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="https://ufl.instructure.com"
                autoComplete="off"
                className="block w-100 rounded-md bg-white/5 px-3.5 py-2 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
            />
            </div>
            
            <div className="mt-6">
            <button
            type="submit"
            disabled={loading}
            className="block rounded-md bg-orange-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
            {loading ? 'Submitting...' : 'Submit'}
            </button>
            </div>

            
            {status && <p className="mt-4 text-sm text-red-300">{status}</p>}

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
    </>
  )
}

export default CanvasInfo
