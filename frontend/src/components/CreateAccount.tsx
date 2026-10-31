import { useState } from 'react'

/*
    Create account page, can be opened by clicking thee "Create account" 
    link on the login page
*/

function CreateAccount() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const mismatch = confirm !== "" && password !== confirm;

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (mismatch) return;
    console.log("Create account submitted for", username);
  }

  return (
    <div className="mt-6 w-100 max-w-full rounded-2xl bg-white p-6 shadow-xs outline-1 -outline-offset-1 outline-gray-300">
      <h2 className="text-center text-lg/7 font-semibold text-gray-900">
        Create account
      </h2>

      <form onSubmit={handleSubmit} className="mt-4 flex flex-col gap-4">
        <div>
          <label htmlFor="new-username" className="block text-sm/6 font-semibold text-gray-900">
            Username
          </label>
          <input
            id="new-username"
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
          <label htmlFor="new-password" className="block text-sm/6 font-semibold text-gray-900">
            Password
          </label>
          <input
            id="new-password"
            name="password"
            type="password"
            autoComplete="new-password"
            required
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="mt-2.5 block min-h-12 w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
          />
        </div>

        <div>
          <label htmlFor="confirm-password" className="block text-sm/6 font-semibold text-gray-900">
            Confirm password
          </label>
          <input
            id="confirm-password"
            name="confirm-password"
            type="password"
            autoComplete="new-password"
            required
            value={confirm}
            onChange={(event) => setConfirm(event.target.value)}
            className="mt-2.5 block min-h-12 w-full rounded-2xl bg-white px-3.5 py-2 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500"
          />
          {mismatch && (
            <p className="mt-2 text-sm/6 text-red-600">Passwords do not match.</p>
          )}
        </div>

        <button
          type="submit"
          className="block w-full rounded-2xl bg-indigo-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
        >
          Create account
        </button>
      </form>

    </div>
  )
}

export default CreateAccount
