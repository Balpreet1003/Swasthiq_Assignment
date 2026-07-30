const formatCurrency = (value) =>
  `₹${(value / 100).toFixed(2)}`;

export default function TracedFigures({
  report,
  analytics,
}) {
  const topRevenueMedicine =
    analytics.top_medicines_by_revenue[0];

  const rows = [
    {
      value: formatCurrency(report.total_billed_paise),
      label: "total_billed",
    },
    {
      value: formatCurrency(report.total_collected_paise),
      label: "total_collected",
    },
    {
      value: formatCurrency(report.outstanding_paise),
      label: "outstanding",
    },
    {
      value: formatCurrency(report.total_refund_paise),
      label: "refunds",
      danger: true,
    },
    {
      value: 
        analytics.peak_hour.hour === "N/A"
          ? "N/A"
          : `${analytics.peak_hour.hour}-${parseInt(
              analytics.peak_hour.hour.split(":")[0],
              10
            ) + 1}:00 / ${formatCurrency(
              analytics.peak_hour.revenue_paise
            )}`
      ,
      label: "revenue_by_hour[max]",
    },
    {
      value: `${
        topRevenueMedicine?.drug_name ? 
          topRevenueMedicine.drug_name : 
          "N/A"
      }`,
      label: "top_drug_by_revenue",
    },
    {
      value: topRevenueMedicine?.revenue_paise ? 
        formatCurrency(topRevenueMedicine.revenue_paise) : 
        "N/A",
      label: "top_drug_revenue",
    },
  ];

  return (
    <div
      className="rounded-xl border p-6"
      style={{
        background: "#FCFDFE",
        borderColor: "#D6E6F8",
        boxShadow: "0 2px 8px rgba(15,23,42,.04)",
      }}
    >
      <h2
        className="text-3xl font-bold"
        style={{
          color: "#1F2937",
        }}
      >
        Traced Figures
      </h2>

      <p
        className="mt-2 mb-8"
        style={{
          color: "#94A3B8",
          fontSize: "14px",
          lineHeight: "22px",
        }}
      >
        Every number above maps to the deterministic
        report — this is what gets auto-checked.
      </p>

      <div className="space-y-6">
        {rows.map((row) => (
          <div
            key={row.label}
            className="grid grid-cols-[1.5fr_1fr] items-center"
          >
            <div
              className="text-lg font-bold"
              style={{
                color: row.danger
                  ? "#EF4444"
                  : "#1F2937",
              }}
            >
              {row.value}
            </div>

            <div
              className="text-right text-sm font-medium"
              style={{
                color: "#A78BFA",
                letterSpacing: "0.2px",
              }}
            >
              {row.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}