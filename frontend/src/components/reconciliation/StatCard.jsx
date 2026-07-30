export default function StatCard({
  title,
  value,
  subtitle,
  subtitleColor = "text-slate-500",
}) {
  return (
    <div
      className="rounded-2xl border border-slate-200 bg-white
                 p-6 shadow-sm"
    >
      <p
        className="text-xs font-semibold uppercase
                   tracking-wide text-slate-400"
      >
        {title}
      </p>

      <h2 className="mt-2 text-4xl font-bold">
        {value}
      </h2>

      <p
        className={`mt-3 text-sm ${subtitleColor}`}
      >
        {subtitle}
      </p>
    </div>
  );
}