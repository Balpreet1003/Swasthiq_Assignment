export default function Header({
  title,
  subtitle,
}) {
  return (
    <div className="mb-10 flex items-start justify-between">

      <div>

        <h1 className="text-5xl font-bold text-slate-900">
          {title}
        </h1>

        <p className="mt-2 text-lg text-slate-500">
          {subtitle}
        </p>

      </div>

      <button
        className="
          rounded-lg
          border
          border-slate-300
          bg-white
          px-4
          py-2
          text-sm
          font-semibold
          shadow-sm
        "
      >
        27 Jul 2026
      </button>

    </div>
  );
}