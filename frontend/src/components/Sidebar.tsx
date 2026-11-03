import { useEffect, useState } from 'react'
import { fetchSessions, LoginExpiredError, type HistoryChat, type HistorySession } from '../utils/history'

/*
    Side bar on the left of the extension, only shown when logged in
*/

type SidebarProps = {
  token: string
  refreshKey: number
  activeChatId: number | null
  onSelectChat: (chat: HistoryChat) => void
  onNewChat: () => void
  onLoginExpired: () => void
}

function Sidebar({ token, refreshKey, activeChatId, onSelectChat, onNewChat, onLoginExpired }: SidebarProps) {
  const [sessions, setSessions] = useState<HistorySession[] | null>(null);
  const [error, setError] = useState("");
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  // reload the history on login and whenever a new chat is saved
  useEffect(() => {
    let ignore = false;

    fetchSessions(token)
      .then((data) => {
        if (ignore) {
          return;
        }
        setSessions(data);
        setError("");
      })
      .catch((error) => {
        if (ignore) {
          return;
        }
        if (error instanceof LoginExpiredError) {
          onLoginExpired();
          return;
        }
        setError((error as Error).message);
      });

    return () => {
      ignore = true;
    };
  }, [token, refreshKey, onLoginExpired]);

  function toggleSession(sessionId: number) {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(sessionId)) {
        next.delete(sessionId);
      }
      else {
        next.add(sessionId);
      }
      return next;
    });
  }

  return (
    <aside className="sticky top-0 z-10 flex max-h-150 w-56 shrink-0 flex-col border-r border-gray-200 bg-white/70 p-3">
      <button
        type="button"
        onClick={onNewChat}
        className="flex w-full items-center justify-center gap-2 rounded-2xl bg-indigo-500 px-3.5 py-2.5 text-sm font-semibold text-white shadow-xs hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
      >
        {/* plus icon svg */}
        <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="size-4">
          <path d="M12 5v14" />
          <path d="M5 12h14" />
        </svg>
        New Chat
      </button>

      <h2 className="mt-5 px-2 text-xs/6 font-semibold text-gray-500">
        History
      </h2>

      <div className="mt-1 min-h-0 flex-1 overflow-y-auto">
        {sessions === null && !error && (
          <p className="px-2 text-sm/6 text-gray-500">Loading...</p>
        )}
        {error && (
          <p className="px-2 text-sm/6 text-red-600">{error}</p>
        )}
        {sessions?.length === 0 && (
          <p className="px-2 text-sm/6 text-gray-500">No previous chats yet.</p>
        )}

        <ul className="flex flex-col gap-1">
          {sessions?.map((session) => {
            const isOpen = expanded.has(session.session_id);
            return (
              <li key={session.session_id}>
                <button
                  type="button"
                  onClick={() => toggleSession(session.session_id)}
                  aria-expanded={isOpen}
                  title={session.session_title}
                  className="flex w-full items-center gap-1.5 rounded-xl px-2 py-1.5 text-left text-sm/6 font-semibold text-gray-900 transition-colors hover:bg-gray-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
                >
                  {/* dropdown arrow svg */}
                  <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={`size-4 shrink-0 text-gray-500 transition-transform ${isOpen ? 'rotate-90' : ''}`}>
                    <path d="m9 18 6-6-6-6" />
                  </svg>
                  <span className="min-w-0 truncate">{session.session_title}</span>
                </button>

                {isOpen && (
                  <ul className="mt-1 ml-4 flex flex-col gap-1 border-l border-gray-200 pl-2">
                    {session.chats.length === 0 && (
                      <li className="px-2 py-1.5 text-sm/6 text-gray-500">No chats in this session.</li>
                    )}
                    {session.chats.map((chat) => (
                      <li key={chat.chat_id}>
                        <button
                          type="button"
                          onClick={() => onSelectChat(chat)}
                          title={chat.message}
                          className={`block w-full truncate rounded-xl px-2 py-1.5 text-left text-sm/6 transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 ${
                            chat.chat_id === activeChatId
                              ? 'bg-indigo-50 font-semibold text-indigo-600'
                              : 'text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {chat.message}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      </div>
    </aside>
  )
}

export default Sidebar
