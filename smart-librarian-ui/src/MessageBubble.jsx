export default function MessageBubble({ role, content, time }) {
  const date = time ? new Date(time) : new Date();
  const hh = String(date.getHours()).padStart(2, "0");
  const mm = String(date.getMinutes()).padStart(2, "0");

  return (
    <div className={`bubble ${role}`}>
      <div className="meta">
        <b>{role === "user" ? "Tu" : "Asistent"}</b> · {hh}:{mm}
      </div>
      <div>{content}</div>
    </div>
  );
}