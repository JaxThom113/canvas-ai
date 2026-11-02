/*
    Helpers for the logged in user kept in localstorage
*/

export type User = {
  account_id: number
  username: string
  token: string
}

const STORAGE_KEY = 'canvy_user';

export function saveUser(user: User) {
  // save the currently logged in user to local storage
  // that way we know who is logged in when extension is closed
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
}

export function clearUser() {
  // remove the currently logged in user from local storage
  localStorage.removeItem(STORAGE_KEY);
}

export function loadUser(): User | null {
  // recall what user is logged in from localstorage 
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) {
    return null;
  }

  try {
    return JSON.parse(saved) as User;
  }
  catch {
    localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

export async function authenticate(endpoint: 'login' | 'signup', username: string, password: string): Promise<User> {
  // call /auth/login or /auth/signup to log in or create a new user
  let res: Response;
  try {
    res = await fetch(`http://localhost:8000/auth/${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    });
  }
  catch {
    throw new Error("Failed to contact backend.");
  }

  // get json user data
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail ?? "Something went wrong. Please try again.");
  }

  return data as User;
}
