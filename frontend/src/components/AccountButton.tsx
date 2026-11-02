import type { User } from '../auth'

/*
    Account button on top right of extension, turns into logout button when
    user is currently logged in
*/

type AccountButtonProps = {
  user: User | null
  view: 'chat' | 'login' | 'signup'
  onToggleLogin: () => void
  onLogout: () => void
}

function AccountButton({ user, view, onToggleLogin, onLogout }: AccountButtonProps) {
  return (
    <div className="absolute right-4 top-4 flex items-center gap-3">
        {user ? (
            <>
            <span className="max-w-40 truncate text-sm/6 font-semibold text-gray-900" title={user.username}>
                {user.username}
            </span>

            <button
                type="button"
                onClick={onLogout}
                aria-label="Log out"
                title="Log out"
                className="flex size-10 items-center justify-center rounded-full bg-white text-gray-900 shadow-xs outline-1 -outline-offset-1 outline-gray-300 transition-colors hover:bg-gray-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
                {/* logout icon svg */}
                <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="size-5">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <path d="m16 17 5-5-5-5" />
                <path d="M21 12H9" />
                </svg>
            </button>
            </>
        ) : (
            <button
            type="button"
            onClick={onToggleLogin}
            aria-label={view === 'chat' ? 'Open login panel' : 'Close login panel'}
            className={`flex size-10 items-center justify-center rounded-full shadow-xs outline-1 -outline-offset-1 transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 ${
                view === 'chat'
                ? 'bg-white text-gray-900 outline-gray-300 hover:bg-gray-200 focus-visible:outline-indigo-500'
                : 'bg-red-500 text-white outline-red-500 hover:bg-red-700 focus-visible:outline-indigo-500'
            }`}
            >
            {view === 'chat' ? (
                // profile icon svg
                <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="size-5">
                <circle cx="12" cy="8" r="4" />
                <path d="M4 21a8 8 0 0 1 16 0" />
                </svg>
            ) : (
                // x icon svg
                <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="size-5">
                <path d="M18 6 6 18" />
                <path d="m6 6 12 12" />
                </svg>
            )}
            </button>
        )}
    </div>
  )
}

export default AccountButton
