import { useState } from 'react'
import '../../App.css'

/*
    Dev-only test-data seeding panel. Each section inserts one row
    directly into login / session / chat via the backend's /db/* routes.
*/

const API_BASE = 'http://localhost:8000'

async function readErrorDetail(res: Response): Promise<string> {
  try {
    const body = await res.json()
    const detail = body?.detail

    // FastAPI's own validation errors (422) send `detail` as a list of
    // { loc, msg, type } objects rather than a plain string.
    if (Array.isArray(detail)) {
      return detail
        .map((item) => (typeof item === 'string' ? item : item?.msg ?? JSON.stringify(item)))
        .join('; ')
    }

    if (typeof detail === 'string') {
      return detail
    }

    return `Request failed: ${res.status} ${res.statusText}`
  } 
  catch {
    return `Request failed: ${res.status} ${res.statusText}`
  }
}

function LoginSeedForm() {
  const [accountId, setAccountId] = useState('')
  const [status, setStatus] = useState('')
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const parsedAccountId = parseInt(accountId, 10)
    if (Number.isNaN(parsedAccountId)) {
      setStatus('account_id must be a number.')
      setError(true)
      return
    }

    setLoading(true)
    setStatus('')
    setError(false)

    try {
      const res = await fetch(`${API_BASE}/db/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ account_id: parsedAccountId }),
      })

      if (!res.ok) {
        setStatus(await readErrorDetail(res))
        setError(true)
        return
      }

      setStatus('Account created.')
      setError(false)
    } 
    catch (err) {
      const message = err instanceof Error ? err.message : String(err)
      setStatus('Error: ' + message)
      setError(true)
    } 
    finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-6 flex w-100 max-w-full flex-col items-center">
      <label htmlFor="prompt" className="block text-sm/6 font-semibold text-gray-900">
        Login
      </label>

      <div className="mt-2.5 w-full">
        <label htmlFor="login-account-id" className="block text-sm/6 font-semibold text-gray-900">
          account_id
        </label>
        <input
          id="login-account-id"
          type="number"
          value={accountId}
          onChange={(e) => setAccountId(e.target.value)}
          placeholder="12345"
          className="mt-1 block w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
        />
      </div>

      <div className="mt-4">
        <button
          type="submit"
          disabled={loading}
          className="block rounded-md bg-indigo-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Saving...' : 'Save'}
        </button>
      </div>

      {error && status && <p className="mt-3 text-sm text-red-600">{status}</p>}
      {!error && status && <p className="mt-3 text-sm text-gray-700">{status}</p>}
    </form>
  )
}

function SessionSeedForm() {
  const [accountId, setAccountId] = useState('')
  const [sessionId, setSessionId] = useState('')
  const [sessionTitle, setSessionTitle] = useState('')
  const [status, setStatus] = useState('')
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const parsedAccountId = parseInt(accountId, 10)
    if (Number.isNaN(parsedAccountId)) {
      setStatus('account_id must be a number.')
      setError(true)
      return
    }

    if (!sessionTitle.trim()) {
      setStatus('session_title is required.')
      setError(true)
      return
    }

    let parsedSessionId: number | undefined
    if (sessionId.trim()) {
      parsedSessionId = parseInt(sessionId, 10)
      if (Number.isNaN(parsedSessionId)) {
        setStatus('session_id must be a number, or left blank.')
        setError(true)
        return
      }
    }

    setLoading(true)
    setStatus('')
    setError(false)

    try {
      const res = await fetch(`${API_BASE}/db/session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: parsedAccountId,
          session_title: sessionTitle,
          session_id: parsedSessionId,
        }),
      })

      if (!res.ok) {
        setStatus(await readErrorDetail(res))
        setError(true)
        return
      }

      const data = await res.json()
      setStatus(`Session created (session_id=${data.session_id}).`)
      setError(false)
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err)
      setStatus('Error: ' + message)
      setError(true)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-8 flex w-100 max-w-full flex-col items-center">
      <label htmlFor="prompt" className="block text-sm/6 font-semibold text-gray-900">
        Session
      </label>

      <div className="mt-2.5 w-full">
        <label htmlFor="session-account-id" className="block text-sm/6 font-semibold text-gray-900">
          account_id
        </label>
        <input
          id="session-account-id"
          type="number"
          value={accountId}
          onChange={(e) => setAccountId(e.target.value)}
          placeholder="12345"
          className="mt-1 block w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
        />
      </div>

      <div className="mt-2.5 w-full">
        <label htmlFor="session-id" className="block text-sm/6 font-semibold text-gray-900">
          session_id
        </label>
        <input
          id="session-id"
          type="number"
          value={sessionId}
          onChange={(e) => setSessionId(e.target.value)}
          placeholder="auto"
          className="mt-1 block w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
        />
      </div>

      <div className="mt-2.5 w-full">
        <label htmlFor="session-title" className="block text-sm/6 font-semibold text-gray-900">
          session_title
        </label>
        <input
          id="session-title"
          type="text"
          value={sessionTitle}
          onChange={(e) => setSessionTitle(e.target.value)}
          placeholder="12345"
          className="mt-1 block w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
        />
      </div>

      <div className="mt-4">
        <button
          type="submit"
          disabled={loading}
          className="block rounded-md bg-indigo-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Saving...' : 'Save'}
        </button>
      </div>

      {error && status && <p className="mt-3 text-sm text-red-600">{status}</p>}
      {!error && status && <p className="mt-3 text-sm text-gray-700">{status}</p>}
    </form>
  )
}

function ChatSeedForm() {
  const [sessionId, setSessionId] = useState('')
  const [chatId, setChatId] = useState('')
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState('')
  const [status, setStatus] = useState('')
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const parsedSessionId = parseInt(sessionId, 10)
    if (Number.isNaN(parsedSessionId)) {
      setStatus('session_id must be a number.')
      setError(true)
      return
    }

    let parsedChatId: number | undefined
    if (chatId.trim()) {
      parsedChatId = parseInt(chatId, 10)
      if (Number.isNaN(parsedChatId)) {
        setStatus('chat_id must be a number, or left blank.')
        setError(true)
        return
      }
    }

    let parsedMessage: unknown
    try {
      parsedMessage = JSON.parse(message)
    } 
    catch {
      setStatus('Invalid JSON in message field.')
      setError(true)
      return
    }

    let parsedResponse: unknown
    if (response.trim()) {
      try {
        parsedResponse = JSON.parse(response)
      } 
      catch {
        setStatus('Invalid JSON in response field.')
        setError(true)
        return
      }
    }

    setLoading(true)
    setStatus('')
    setError(false)

    try {
      const res = await fetch(`${API_BASE}/db/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: parsedSessionId,
          chat_id: parsedChatId,
          message: parsedMessage,
          response: parsedResponse,
        }),
      })

      if (!res.ok) {
        setStatus(await readErrorDetail(res))
        setError(true)
        return
      }

      const data = await res.json()
      setStatus(`Chat created (chat_id=${data.chat_id}).`)
      setError(false)
    } 
    catch (err) {
      const message = err instanceof Error ? err.message : String(err)
      setStatus('Error: ' + message)
      setError(true)
    } 
    finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-8 flex w-100 max-w-full flex-col items-center">
      <label htmlFor="prompt" className="block text-sm/6 font-semibold text-gray-900">
        Chat
      </label>

      <div className="mt-2.5 w-full">
        <label htmlFor="chat-session-id" className="block text-sm/6 font-semibold text-gray-900">
          session_id
        </label>
        <input
          id="chat-session-id"
          type="number"
          value={sessionId}
          onChange={(e) => setSessionId(e.target.value)}
          placeholder="12345"
          className="mt-1 block w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
        />
      </div>

      <div className="mt-2.5 w-full">
        <label htmlFor="chat-id" className="block text-sm/6 font-semibold text-gray-900">
          chat_id
        </label>
        <input
          id="chat-id"
          type="number"
          value={chatId}
          onChange={(e) => setChatId(e.target.value)}
          placeholder="auto"
          className="mt-1 block w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
        />
      </div>

      <div className="mt-2.5 w-full">
        <label htmlFor="chat-message" className="block text-sm/6 font-semibold text-gray-900">
          message (JSON)
        </label>
        <textarea
          id="chat-message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder='{"text": "hello"}'
          rows={3}
          className="mt-1 block w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
        />
      </div>

      <div className="mt-2.5 w-full">
        <label htmlFor="chat-response" className="block text-sm/6 font-semibold text-gray-900">
          response (JSON, optional)
        </label>
        <textarea
          id="chat-response"
          value={response}
          onChange={(e) => setResponse(e.target.value)}
          placeholder='{"text": "hi there"}'
          rows={3}
          className="mt-1 block w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
        />
      </div>

      <div className="mt-4">
        <button
          type="submit"
          disabled={loading}
          className="block rounded-md bg-indigo-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Saving...' : 'Save'}
        </button>
      </div>

      {error && status && <p className="mt-3 text-sm text-red-600">{status}</p>}
      {!error && status && <p className="mt-3 text-sm text-gray-700">{status}</p>}
    </form>
  )
}

function DBInterface() {
  return (
    <div className="mt-6 flex w-full max-w-2xl flex-col items-center rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h3 className="text-2xl font-semibold text-gray-900">
        Test DB Interface
      </h3>

      <LoginSeedForm />
      <SessionSeedForm />
      <ChatSeedForm />
    </div>
  )
}

export default DBInterface
