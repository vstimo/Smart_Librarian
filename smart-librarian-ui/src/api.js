// const BASE =
//   import.meta.env.VITE_API_BASE_URL ||
//   (typeof window !== "undefined" ? window.location.origin : "http://localhost:8000");

const BASE = import.meta.env.VITE_API_BASE_URL;

export async function askChat(query) {
  const res = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json(); // { ok, message, title?, candidates? }
}
