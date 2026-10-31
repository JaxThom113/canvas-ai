import { useState } from 'react'

/*
    Login page, can be opened by picking the profile icon in top right 
    of normal view
*/

type LoginProps = {
  onCreateAccount: () => void
}

function Login({ onCreateAccount }: LoginProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    console.log("Login submitted for", username);
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
            className="mt-2.5 block min-h-12 w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
          />
        </div>

        <button
          type="submit"
          className="block w-full rounded-2xl bg-indigo-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
        >
          Log in
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
