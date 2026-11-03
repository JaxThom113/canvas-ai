/*
    Helpers for the logged in user's chat history, shown in Sidebar
*/

export type HistoryChat = {
  chat_id: number
  message: string
  response: string
}

export type HistorySession = {
  session_id: number
  session_title: string
  chats: HistoryChat[]
}

export class LoginExpiredError extends Error {}

export async function fetchSessions(token: string): Promise<HistorySession[]> {
  // call /sessions to get the user's sessions and associated chats
  let res: Response;
  try {
    res = await fetch("http://localhost:8000/sessions", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });
  }
  catch {
    throw new Error("Failed to contact backend.");
  }

  const data = await res.json();
  if (res.status === 401) {
    throw new LoginExpiredError(data.detail);
  }
  if (!res.ok) {
    throw new Error(data.detail ?? "Could not load your chat history.");
  }

  return data as HistorySession[];
}
