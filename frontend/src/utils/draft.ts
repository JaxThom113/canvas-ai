/*
    Helpers for the unsent chat message kept in localstorage
*/

const DRAFT_KEY = 'canvy_draft';

export function saveDraft(message: string) {
  // keep whatever is typed in the <textarea> so it survives the extension closing
  if (message) {
    localStorage.setItem(DRAFT_KEY, message);
  }
  else {
    localStorage.removeItem(DRAFT_KEY);
  }
}

export function clearDraft() {
  // remove the saved draft from local storage
  localStorage.removeItem(DRAFT_KEY);
}

export function loadDraft(): string {
  // recall what was typed in the chat box from localstorage
  return localStorage.getItem(DRAFT_KEY) ?? "";
}
