/*
    Logout confirmation window, asks user if they are sure
    they want to log out
*/

type LogoutProps = {
  onConfirm: () => void
  onCancel: () => void
}

function Logout({ onConfirm, onCancel }: LogoutProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/40 p-6" onClick={onCancel}>
        <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="logout-title"
            onClick={(event) => event.stopPropagation()}
            className="w-80 max-w-full rounded-2xl bg-white p-6 shadow-lg outline-1 -outline-offset-1 outline-gray-300"
        >
            <h2 id="logout-title" className="text-center text-lg/7 font-semibold text-gray-900">
                Confirm log out?
            </h2>

            <div className="mt-6 flex gap-3">
                <button
                type="button"
                onClick={onConfirm}
                className="block w-full rounded-2xl bg-red-500 px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-xs hover:bg-red-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
                Log out
            </button>

            <button
                type="button"
                autoFocus
                onClick={onCancel}
                className="block w-full rounded-2xl bg-white px-3.5 py-2.5 text-center text-sm font-semibold text-gray-900 shadow-xs outline-1 -outline-offset-1 outline-gray-300 hover:bg-gray-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
                Cancel
            </button>
            
            </div>
        </div>
    </div>
  )
}

export default Logout
