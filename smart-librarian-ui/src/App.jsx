import { useEffect, useRef, useState } from "react";
import { askChat } from "./api";
import MessageBubble from "./MessageBubble";
import "./styles.css";

export default function App() {
  const [history, setHistory] = useState([]); // [{role:'user'|'assistant', content, time}]
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [voiceMode, setVoiceMode] = useState(false); // placeholder
  const threadRef = useRef(null);

  // autoscroll la final
  useEffect(() => {
    if (threadRef.current) {
      threadRef.current.scrollTop = threadRef.current.scrollHeight;
    }
  }, [history, loading]);

  async function sendQuery(e) {
    e?.preventDefault();
    const q = query.trim();
    if (!q || loading) return;

    setError("");
    const now = Date.now();
    setHistory((h) => [...h, { role: "user", content: q, time: now }]);
    setQuery("");
    setLoading(true);

    try {
      const data = await askChat(q);
      const reply = data?.message || "(no content)";
      setHistory((h) => [...h, { role: "assistant", content: reply, time: Date.now() }]);
    } catch (err) {
      setError(err.message || String(err));
      setHistory((h) => [...h, { role: "assistant", content: "A apărut o eroare. Încearcă din nou.", time: Date.now() }]);
    } finally {
      setLoading(false);
    }
  }

  // ENTER pentru trimitere
  function onKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendQuery(e);
    }
  }

  // Placeholder TTS
  function onTTS() {
    const last = [...history].reverse().find((m) => m.role === "assistant");
    if (!last) return;
    // TODO: integrare TTS (ex. POST /tts) și redare
    console.log("[TTS] would play:", last.content);
    alert("TTS (placeholder): ar reda audio pentru ultimul răspuns al asistentului.");
  }

  // Placeholder Voice Mode
  function toggleVoiceMode() {
    const on = !voiceMode;
    setVoiceMode(on);
    if (on) {
      // TODO: pornește recunoaștere vocală (Web Speech API / backend)
      alert("Voice Mode ON (placeholder): ar asculta microfonul și ar trimite transcriptul.");
    } else {
      alert("Voice Mode OFF");
    }
  }

  // Placeholder Image Generation
  function onGenerateImage() {
    const last = [...history].reverse().find((m) => m.role === "assistant");
    if (!last) return;
    // TODO: POST /image-generate + afișare img
    console.log("[IMG] would generate from:", last.content);
    alert("Image Generation (placeholder): ar genera o imagine reprezentativă.");
  }

  const hasAssistant = history.some((m) => m.role === "assistant");

  return (
    <div className="app">
      <div className="header">
        <h1>Smart Librarian</h1>
      </div>

      <div className="thread" ref={threadRef}>
        {history.length === 0 && (
          <div className="bubble assistant">
            <div className="meta"><b>Asistent</b></div>
            Ask a question (eg. <i>What is a good book about friendship and magic?</i>)
          </div>
        )}
        {history.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} time={m.time} />
        ))}
        {loading && (
          <div className="bubble assistant">
            <div className="meta"><b>Asistent</b></div>
            ...thinking
          </div>
        )}
      </div>

      <div className="toolbar">
        <button className="btn" onClick={onTTS} disabled={!hasAssistant}>
          🔊 Generate Audio (TTS)
        </button>
        <button className="btn" onClick={toggleVoiceMode}>
          {voiceMode ? "🎙️ Voice Mode: ON" : "🎙️ Voice Mode: OFF"}
        </button>
        <button className="btn" onClick={onGenerateImage} disabled={!hasAssistant}>
          🖼️ Generate Image
        </button>
        <div style={{ marginLeft: "auto", color: "var(--muted)" }}>
          {error ? <span style={{ color: "crimson" }}>Eroare: {error}</span> : "Conectat la backend"}
        </div>
      </div>

      <form className="composer" onSubmit={sendQuery}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="type your prompt here..."
          aria-label="Mesaj"
        />
        <button disabled={loading}>{loading ? "..." : "SEND"}</button>
      </form>
    </div>
  );
}