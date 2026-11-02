import { useState } from 'react'
import { authenticate, type User } from '../auth'

/*
    Login page, can be opened by picking the profile icon in top right 
    of normal view
*/

type LoginProps = {
  onLogin: (user: User) => void
  onCreateAccount: () => void
}

function Login({ onLogin, onCreateAccount }: LoginProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      onLogin(await authenticate('login', username, password));
    }
    catch (error) {
      setError((error as Error).message);
    }
    finally {
      setLoading(false);
    }
  }

  return (
    <div className="mt-6 w-100 max-w-full rounded-2xl bg-white p-6 shadow-xs outline-1 -outline-offset-1 outline-gray-300">
      <h2 className="text-center text-lg/7 font-semibold text-gray-900">
        Login
      </h2>

      <form onSubmit={handleSubmit} className="mt-4 flex flex-col gap-4">
        <div>
          <label htmlFor="username" className="block text-sm/6 font-semibold text-gray-900">
            Username
          </label>
          <input
            id="username"
            name="username"
            type="text"
            autoComplete="username"
            required
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            placeholder="Username"
            className="mt-2.5 block min-h-12 w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm/6 font-semibold text-gray-900">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Password"
            className="mt-2.5 block min-h-12 w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
          />
        </div>

        {error && (
          <p className="text-sm/6 text-red-600">{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="block w-full rounded-2xl bg-indigo-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Logging in...' : 'Log in'}
        </button>
      </form>

      <p className="mt-4 text-center text-sm/6 text-gray-500">
        Don't have an account?{' '}
        <button
          type="button"
          onClick={onCreateAccount}
          className="font-semibold text-indigo-500 hover:text-indigo-400"
        >
          Create account
        </button>
      </p>

    </div>
  )
}

export default Login
