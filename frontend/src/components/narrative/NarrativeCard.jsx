export default function NarrativeCard({ narrative }) {
  return (
    <div
      className="rounded-xl border p-6"
      style={{
        background: "#EAF7E9",
        borderColor: "#D6E6F8",
        boxShadow: "0 2px 8px rgba(15,23,42,.04)",
      }}
    >
      <div className="mb-5">

        <span
          className="inline-block rounded-full px-3 py-1 text-xs font-bold"
          style={{
            background: "#D8F2D6",
            color: "#4C7B52",
          }}
        >
          Sent to: Dr. Anand Mehta · WhatsApp
        </span>

      </div>

      <div
        className="leading-8 whitespace-pre-wrap"
        style={{
          color: "#4B5563",
          fontSize: "17px",
        }}
      >
        {narrative}
      </div>

      <div className="mt-8">

        <span
          className="rounded-full px-4 py-2 text-xs font-bold"
          style={{
            background: "#D8F2D6",
            color: "#2E8B57",
          }}
        >
          SUCCESS
        </span>

      </div>
    </div>
  );
}