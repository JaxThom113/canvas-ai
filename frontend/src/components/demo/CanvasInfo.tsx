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
    and returns account data accessible in Canvas session cookies
*/  

function CanvasInfo() {
  const [baseURL, setBaseURL] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [courses, setCourses] = useState<CanvasCourse[]>([]);

  // load the last-used Canvas base URL
  useEffect(() => {
    chrome.storage.local.get(["canvasBaseUrl"], (result: { canvasBaseUrl?: string }) => {
      if (result.canvasBaseUrl) {
        setBaseURL(result.canvasBaseUrl);
      }
    });
  }, []);
  
  async function getCanvasData(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    // get the base URL from the currently open Canvas tab
    const [tab] = await chrome.tabs.query({
      active: true,
      lastFocusedWindow: true,
    });

    if (!tab.url) {
      setStatus("Base URL could not be accessed.");
      return;
    }

    // access base URL of open Canvas instance (i.e. https://schoolname.instructure.com)
    setBaseURL(new URL(tab.url).origin);

    setLoading(true);
    setCourses([]);
    setStatus("Fetching...");

    chrome.storage.local.set({ canvasBaseUrl: baseURL });

    /*
        Other endpoints can be:

        `${rawBase}/api/v1/users/self/profile`
        `${rawBase}/api/v1/users/self/todo`
        `${rawBase}/api/v1/courses/${courseId}/assignments`
        `${rawBase}/api/v1/courses/${courseId}/modules`
        `${rawBase}/api/v1/calendar_events?type=event`
    */

    const endpoint = `${baseURL}/api/v1/courses?enrollment_state=active&per_page=100`;

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
                Click to access course info:
            </label>
            
            <div className="mt-6">
                <button
                    type="submit"
                    disabled={loading}
                    className="block rounded-md bg-orange-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
                    >
                    {loading ? 'Getting courses...' : 'Get courses'}
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
